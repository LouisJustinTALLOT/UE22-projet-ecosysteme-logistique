from pprint import pformat, pprint
from typing import Dict, List, Tuple
import geopandas as gpd
import pandas as pd
import numpy as np
import folium
import matplotlib.pyplot as plt
import time
from multiprocessing import Pool, Process, Array, RawArray
import numba as nb
from numba import jit, vectorize, float64, int64
import cProfile

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

import sys
from shapely.geometry.multipolygon import MultiPolygon
sys.path.append("../../")

from sklearn.cluster import KMeans, MiniBatchKMeans

from shapely.geometry import Polygon, Point

from src.clusterizer.utils import NAF_utils
from src.clusterizer.utils import clusterizer_utils
from src.clusterizer.utils.clusterizer_utils import COLUMN_HULLS_NAME, \
    COLUMN_CLUSTER_INDEX_NAME, \
    COLUMN_CLUSTER_SIZE_NAME, \
    COLUMN_CENTROIDS_NAME, \
    COLUMN_DEFAULT_GEOMETRY_NAME, \
    COLUMN_CLUSTER_MASS_NAME

"""
Clusterise en utilisant l'algorithme des k-moyennes.

Pour avoir des exemples d'utilisation, aller à la toute fin où il y a les tests
"""

DEBUG_PLOT = False # pour afficher les points et frontières (debugging)

DICT_ZONES_IDF = {
    0 : "IDF_zone_est",
    1 : "IDF_zone_nord_ouest",
    2 : "IDF_zone_nord",
    3 : "IDF_zone_Paris_ouest",
    4 : "IDF_zone_sud",
}

DIR_SHP_FILES = "../../data/IDF_5_zones/"

DICT_GDF_ZONES: Dict[int, Polygon] = {}

for i in DICT_ZONES_IDF.keys():
    DICT_GDF_ZONES[i] = gpd.read_file(DIR_SHP_FILES + DICT_ZONES_IDF[i] + ".shp")['geometry'][0]

# pprint(DICT_GDF_ZONES[0].contains(Point(2.3, 48.4)))

# pprint([(i, pformat(DICT_GDF_ZONES[i])) for i in DICT_ZONES_IDF.keys()])

# raise BaseException

NB_ZONES = len(DICT_ZONES_IDF)

@np.vectorize
def rapport_a_la_seine(xy):
    coord = (xy[0], xy[1])

    for no_zone, gdf in DICT_GDF_ZONES.items():
        if Point(*coord).within(gdf):
            # print(coord, no_zone)
            return no_zone

    # print(coord, "out of all zones")
    return NB_ZONES


def process_rapport_a_la_seine(no_zone:int, df: pd.DataFrame, shared_array: Array) -> None:
    shared_array[no_zone] = df[no_zone == rapport_a_la_seine(np.array(df.copy()["geometry"].apply(lambda x: x['coordinates'])))].reset_index(drop=True)

def map_rapport_a_la_seine(args_tuple: Tuple[int, pd.DataFrame]) -> pd.DataFrame:
    no_zone, df = args_tuple
    return df[no_zone == rapport_a_la_seine(np.array(df.copy()["geometry"].apply(lambda x: x['coordinates'])))].reset_index(drop=True)

# @jit(nopython=True, parallel=True)
# def numba_rapport_a_la_seine(array, no_zone):

#     return no_zone == rapport_a_la_seine(array)


def nettoyer(df, reduce=False, threshold=1000, column_geometry=COLUMN_DEFAULT_GEOMETRY_NAME):
    """
    Nettoie la DataFrame. Enlève les na, et si spécifié, ne prend que les premières données de la (Geo)DataFrame.

    :param df: La DataFrame.
    :param reduce: Si True, ne prend que les premières données.
    :param threshold: Dans le cas où reduce=True, nombre de données à sélectionner.
    :param column_geometry: A spécifier si la colonne contenant les points n'est pas la colonne par défaut ("geometry")
    :return: Une DataFrame nettoyée.
    """
    if reduce and df.size >= threshold:
        df = df[:threshold]

    return df.dropna(subset=[column_geometry]).reset_index()

# @jit(parallel=True)
def clusterize(df, k, column_geometry=COLUMN_DEFAULT_GEOMETRY_NAME, dict=False, weight=True):
    """
    Clusterise à l'aide de l'algorithme des k-moyennes. Attention, fait du en-place.

    :param df: La (Geo)DataFrame contenant les points à clusteriser.
    :param k: Le nombre de clusters à calculer.
    :param column_geometry: A spécifier si la colonne contenant les points n'est pas la colonne par défaut ("geometry")
    :param dict: Indiquer True si jamais la colonne contenant les points ne contient pas d'objets
     shapely.geometry.Points, mais un dictionnaire (en général, lorsque le fichier provient d'un GeoJSON)
    :return: Deux GeoDataFrame.
     Une première GeoDataFrame entrée contenant une colonne en plus ("cluster") : celle-ci permet de savoir pour chaque
     point le numéro du cluster qui lui a été affecté.
     Une deuxième GeoDataFrame contenant les informations détaillées de chaque cluster : centre de masse ("centroids"),
     enveloppe convexe ("hulls") et nombre d'établissements dans le cluster ("taille")
    """

    # ===========================================================
    # Commençons par faire le clustering et récupérer les centres
    # ==========================================================

    # kmeans = KMeans(n_clusters=k, random_state=0)
    mbk = MiniBatchKMeans(n_clusters=k, random_state=0, batch_size=2048)  # ça va plus vite

    # Ceci contient des coordonnées (x, y) des points
    X = clusterizer_utils.get_coords_from_object(df, column_geometry, dict)
    if len(X) < 1:
        raise ValueError("Table vide")
    Y = clusterizer_utils.vectorized_calculer_poids_code_NAF(df["apet700"]) if weight else None

    # On ajoute à la DataFrame originale les numéros de cluster pour chaque point.
    df_point_cluster = gpd.GeoDataFrame(mbk.fit_predict(X, sample_weight=Y), columns=[COLUMN_CLUSTER_INDEX_NAME], dtype=int)

    df = df.join(df_point_cluster)

    # La DataFrame "df_infos_clusters" associe à chaque numéro de cluster les informations correspondantes.
    # En détails : une colonne "centroids" (centres de masse), une colonne "hulls" (enveloppes convexes),
    # une colonne "taille" (nombre d'établissements)
    df_infos_clusters = pd.DataFrame(gpd.points_from_xy(mbk.cluster_centers_[:, 0],
                                                        mbk.cluster_centers_[:, 1]),
                                     columns=[COLUMN_CENTROIDS_NAME]
                                     )
    df_infos_clusters = df_infos_clusters.join(clusterizer_utils.get_infos_clusters_taille(df))
    df_infos_clusters = df_infos_clusters.join(
        clusterizer_utils.get_infos_clusters_enveloppes_convexes(k, df, column_geometry))
    df_infos_clusters = df_infos_clusters.join(clusterizer_utils.get_infos_clusters_poids(df, "apet700"))

    return df, df_infos_clusters


def save_to_map(df_clusters, map=None):
    """
    Sauvegarde les informations des clusters dans une carte Leaflet.
    Ne retourne rien.

    :param df_clusters: La DataFrame contenant les informations de chaque cluster
     (cf. deuxième sortie de la fonction clusterize)
    :param path: Le chemin de sortie du fichier.
    """

    if map is None:
        map = folium.Map(location=[48.844952, 2.339193],
                        zoom_start=10,
                        tiles="OpenStreetMap"
                        )

    couleurs = ['cadetblue', 'orange', 'darkred', 'black',
                'purple', 'gray', 'darkgreen', 'lightgreen',
                'darkblue', 'blue', 'red']

    centroids = df_clusters.loc[:, COLUMN_CENTROIDS_NAME]
    hulls = df_clusters.loc[:, COLUMN_HULLS_NAME]
    sizes = df_clusters.loc[:, COLUMN_CLUSTER_SIZE_NAME]
    poids = df_clusters.loc[:, COLUMN_CLUSTER_MASS_NAME]

    for k, point in enumerate(centroids):
        if point is not None:
            title = f"Centre de masse du cluster {k} : {sizes[k]} établissements. Poids : {poids[k]}"
            folium.CircleMarker(location=[point.y, point.x],
                          popup=title,
                          radius=1
                         # icon=folium.Icon(color=couleurs[k % len(couleurs)], icon='info-sign')
                          ).add_to(map)

    for k, polygon in enumerate(hulls):
        title = f"Cluster {k}"
        if type(polygon) == Polygon:
            # Notre cluster a plus de trois points (autrement, le type serait Point ou LineString)
            # Donc c'est utile d'afficher l'enveloppe convexe
            polygon = clusterizer_utils.swap_xy(polygon)
            coords = polygon.exterior.coords
            folium.Polygon(locations=coords, popup=title, color=couleurs[k % len(couleurs)]).add_to(map)
        elif type(polygon) == MultiPolygon:
            for poly in polygon:
                poly = clusterizer_utils.swap_xy(poly)
                coords = poly.exterior.coords
                folium.Polygon(locations=coords, popup=title, color=couleurs[k % len(couleurs)]).add_to(map)

    map.get_root().html.add_child(
        folium.Element(str(
            "<title>" + str(len(hulls)) + " clusters</title>"))
    )

    return map

def test_geojson():
    df = nettoyer(gpd.read_file("../../essais/gis/input/reducted.geojson"))
    df, df_clusters = clusterize(df, 10, dict=False)
    save_to_map(df_clusters).save("output/INSERT_NAME.html")

def calcule_nb_clusters_par_zone(liste_df, nb_clusters):
    poids_par_zone: np.ndarray = np.zeros(len(liste_df))
    for i in range(len(liste_df)):
        poids_par_zone[i] = clusterizer_utils.calculer_poids_cluster(liste_df[i], "apet700") 
    poids_total = np.sum(poids_par_zone)
    return np.ceil((poids_par_zone / poids_total * nb_clusters)).astype(int)
    # nb_par_zone = np.rint((poids_par_zone / poids_total * nb_clusters)).astype(int)
    # nb_par_zone = list(np.maximum(nb_par_zone, np.ones(len(liste_df), dtype=int)))  # il faut au moins un cluster par zone considérée
    # return nb_par_zone


def main_json(rayon=8, secteur_NAF='', nb_clusters=50, adresse_map="output/clusterized_map_seine.html", reduce=False, threshold=1000):
    t1 = time.time()
    print("Ouverture de la DataFrame...", end="    ")

    df = nettoyer(pd.read_json("../../data/base_sirene_shortened.json"), reduce=reduce, threshold=threshold)
    if secteur_NAF != '' :
        df = NAF_utils.filter_by_naf(df, NAF_utils.get_NAFs_by_section(secteur_NAF), "apet700")

    t2 = time.time()
    print(f"{t2-t1:2.3f} s")
    t1 = time.time()
    print("On ne garde que les données du centre...", end="    ")


    df = clusterizer_utils.filter_nearby_paris(df, radius=rayon, dict=True)

    t2 = time.time()
    print(f"{t2-t1:2.3f} s")
    t1 = time.time()
    print("On sépare par la Seine...", end="    ")
    
    # on va avoir au moins 4 zones:
    # rive Gauche,
    # rive Droite,
    # Maisons-Alfort,
    # Courbevoie-Asnières

    masque = rapport_a_la_seine(np.array(df.copy()["geometry"].apply(lambda x: x['coordinates'])))

    liste_df = []
    for no_zone in DICT_GDF_ZONES.keys():
        # print("key ", no_zone)
        liste_df.append(
            # df[numba_rapport_a_la_seine(np.array(df.copy()["geometry"].apply(lambda x: x['coordinates'])), no_zone)]
            df[no_zone == masque].reset_index(drop=True)
        )

    # pprint(liste_df)

    t2 = time.time()
    print(f"{t2-t1:2.3f} s")
    t1 = time.time()
    print("Clusterisation...", end="    ")

    liste_df_clusters = []
    nb_clusters_par_zone = calcule_nb_clusters_par_zone(liste_df, nb_clusters)
    # nb_clusters_par_zone = [10]*NB_ZONES

    for no_zone in range(NB_ZONES):
        try:
            liste_df_clusters.append(
                clusterize(liste_df[no_zone], nb_clusters_par_zone[no_zone], dict=True, weight=True)
            )
        except ValueError as e:
            print(e, no_zone)
            pass

    t2 = time.time()
    print(f"{t2-t1:2.3f} s")
    t1 = time.time()
    print("Sauvegarde sur la carte...", end="    ")
    # print(liste_df_clusters)
    map = save_to_map(liste_df_clusters[0][1])

    for no_zone in range(1, len(liste_df_clusters)):
        map = save_to_map(liste_df_clusters[no_zone][1], map=map)

    map.save(adresse_map)

    t2 = time.time()
    print(f"{t2-t1:2.3f} s")
    t1 = time.time()
    print("Terminé !")


def test_naf():
    print(NAF_utils.get_NAFs_by_section("L"))

if __name__ == "__main__":

    # On exécute le programme avec la base SIRENE :

    if DEBUG_PLOT:    
        main_json(reduce=True)

    else:
        # main_json(reduce = True, adresse_map="output/clusterized_map_optim_de_cython.html")
        # main_json(adresse_map="output/clusterized_map_optim_de_cython.html")
        # cProfile.run('main_json(adresse_map="output/clusterized_map_with_shapefile.html", reduce=True, threshold=10000)')
        # cProfile.run('main_json(rayon=1000, adresse_map="output/clusterized_map_with_shapefile.html")')
        # main_json(rayon=100, adresse_map="output/clusterized_map_with_shapefile_no_convex.html", reduce=True, threshold=10_000)
        with PyCallGraph(output=GraphvizOutput()):
            main_json(rayon=100, adresse_map="output/clusterized_map_with_shapefile_no_convex.html", reduce=True, threshold=10_000)
