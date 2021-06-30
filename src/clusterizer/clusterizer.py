"""Fichier principal s'occupant de la clusterisation
à partir de la base de données et des paramètres choisis par l'utilisateur.

Le module : 
    - ouvre le fichier :code:`json` contenant la base SIRENE réduite aux données utiles
    - sélectionne les établissements correspondants aux codes NAF rentrés par l'utilisateur
    - garde tous les établissements dans une certain rayon autour du centre de Paris (rayon choisi par l'utilisateur)
    - si demandé, sépare les ponits en zones en fonction des cours d'eau d'Île-de-France avec le module :code:`utils/seine_data_utils`
    - regroupe les points en clusters avec l'algorithme :code:`MiniBatchKMeans` de :code:`scikit-learn`
    - exporte le résultat sous forme de carte (dans un fichier `HTML`) à l'aide du module :code:`folium` 

"""
from pprint import pformat, pprint
from typing import Dict, List, Tuple
import geopandas as gpd
import pandas as pd
import numpy as np
import folium
import matplotlib.pyplot as plt
import time
from multiprocessing import Pool, Process, Array, RawArray

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
from src.clusterizer.utils.seine_data_utils import DICT_GDF_ZONES, NB_ZONES, rapport_a_la_seine_multiprocessing

"""
Clusterise en utilisant l'algorithme des k-moyennes.
"""

DEBUG_PLOT = False # pour afficher les points et frontières (debugging)


def nettoyer(df: pd.DataFrame, reduce: bool = False, threshold: int = 1000, column_geometry: str = COLUMN_DEFAULT_GEOMETRY_NAME) -> pd.DataFrame:
    """
    Nettoie la DataFrame. Enlève les na.
    Si spécifié, ne retient que les premières données de la DataFrame.

    :param df: La DataFrame.
    :param reduce: Si True, ne prend que les premières données.
    :param threshold: Dans le cas où reduce=True, nombre de données à sélectionner.
    :param column_geometry: A spécifier si la colonne contenant les points n'est pas la colonne par défaut ("geometry")
    :return: Une DataFrame nettoyée.
    """

    if reduce and df.size >= threshold:
        df = df[:threshold]

    return df.dropna(subset=[column_geometry]).reset_index(drop=True)


def clusterize(df: pd.DataFrame, k: int, column_geometry: str = COLUMN_DEFAULT_GEOMETRY_NAME, is_dict: bool = False, weight: bool = True) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Clusterise à l'aide de l'algorithme des k-moyennes. Attention, fait du en-place.

    :param df: La (Geo)DataFrame contenant les points à clusteriser.
    :param k: Le nombre de clusters à calculer.
    :param column_geometry: A spécifier si la colonne contenant les points n'est pas la colonne par défaut ("geometry")
    :param is_dict: Indiquer True si jamais la colonne contenant les points ne contient pas d'objets
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


    mbk = MiniBatchKMeans(n_clusters=k, random_state=0, batch_size=2048)  # ça va plus vite

    # Ceci contient des coordonnées (x, y) des points
    X = clusterizer_utils.get_coords_from_object(df, column_geometry, is_dict)
    if len(X) < 1:
        raise ValueError("Table vide")
    Y = clusterizer_utils.vectorized_calculer_poids_code_NAF(df["apet700"]) if weight else None

    # On ajoute à la DataFrame originale les numéros de cluster pour chaque point.
    df_point_cluster = gpd.GeoDataFrame(mbk.fit_predict(X, sample_weight=Y), columns=[COLUMN_CLUSTER_INDEX_NAME], dtype=int)

    df = df.join(df_point_cluster)

    # La DataFrame "df_infos_clusters" associe à chaque numéro de cluster les 
    # informations correspondantes.
    # En détails : une colonne "centroids" (centres de masse), 
    # une colonne "hulls" (enveloppes convexes),
    # une colonne "taille" (nombre d'établissements)
    df_infos_clusters = pd.DataFrame(gpd.points_from_xy(mbk.cluster_centers_[:, 0],
                                                        mbk.cluster_centers_[:, 1]),
                                     columns=[COLUMN_CENTROIDS_NAME]
                                     )
    df_infos_clusters = df_infos_clusters.join(clusterizer_utils.get_infos_clusters_taille(df))
    df_infos_clusters = df_infos_clusters.join(
        clusterizer_utils.get_infos_clusters_enveloppes_convexes(k, df, column_geometry, is_dict)
    )
    df_infos_clusters = df_infos_clusters.join(clusterizer_utils.get_infos_clusters_poids(df, "apet700"))

    return df, df_infos_clusters


def save_to_map(df_clusters: pd.DataFrame, map: folium.folium.Map = None, nb_avant=0) -> folium.folium.Map:
    """
    Sauvegarde les informations des clusters dans une carte Leaflet.
    Retourne la carte

    :param df_clusters: La DataFrame contenant les informations de chaque cluster
     (cf. deuxième sortie de la fonction clusterize)
    :param map: la carte à utiliser
     si un paramètre est spécifié : réecrit par dessus.
     si rien n'est spécifié, génère une nouvelle carte
    :param nb_avant: nombre de clusters déjà réalisés dans le cas où plusieurs zones sont clusterisées à la suite
    :return: une carte complétée.
    """

    if map is None:
        map = folium.Map(
            location=[48.844952, 2.339193],
            zoom_start=10,
            tiles="Stamen Terrain"
        )

    couleurs = ['darkslateblue', 'orange', 'darkred', 'black',
                'purple', 'chocolate', 'darkgreen', 'seagreen',
                'darkblue', 'blue', 'red']

    centroids = df_clusters.loc[:, COLUMN_CENTROIDS_NAME]
    hulls = df_clusters.loc[:, COLUMN_HULLS_NAME]
    sizes = df_clusters.loc[:, COLUMN_CLUSTER_SIZE_NAME]
    poids = df_clusters.loc[:, COLUMN_CLUSTER_MASS_NAME]

    for k, point in enumerate(centroids):
        if point is not None:
            title = f"Centre de masse du cluster {k + nb_avant} : {sizes[k]} etablissements. Poids : {poids[k]}"
            folium.CircleMarker(
                location=[point.y, point.x],
                popup=title,
                radius=3,
                color ='purple'
                # icon=folium.Icon(color=couleurs[k % len(couleurs)], icon='info-sign')
            ).add_to(map)

    for k, polygon in enumerate(hulls):
        title = f"Cluster {k + nb_avant}"
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
    """
    Fonction interne (utilisée pour vérifier le bon fonctionnement de la clusterisation).
    """
    df = nettoyer(gpd.read_file("../../essais/gis/input/reducted.geojson"))
    df, df_clusters = clusterize(df, 10, is_dict=False)
    save_to_map(df_clusters).save("output/INSERT_NAME.html")

def calcule_nb_clusters_par_zone(liste_df, nb_clusters):
    """
    Calcule le nombre de clusters à mettre dans chaque zone pour équilibrer les poids des clusters entre les zones

    :param liste_df: la liste des Dataframe correspondant aux différentes zones
    :param nb_clusters: le nombre de clusters total voulu
    :return: la liste des nombres de clusters par zones
    """

    poids_par_zone: np.ndarray = np.zeros(len(liste_df))
    for i in range(len(liste_df)):
        poids_par_zone[i] = clusterizer_utils.calculer_poids_cluster(liste_df[i], "apet700")
    poids_total = np.sum(poids_par_zone)
    nb_par_zone = np.rint((poids_par_zone / poids_total * nb_clusters)).astype(int)
    nb_par_zone = np.maximum(nb_par_zone, np.ones(len(liste_df), dtype=int))  # il faut au moins un cluster par zone considérée
    return nb_par_zone

def main_json(rayon: int = 8, secteur_NAF: List[str] = [''], nb_clusters: int = 50, adresse_map: str = "output/clusterized_map_seine.html",
              seine_divide: bool = True,
              reduce: bool = False,
              threshold: int = 1000) -> None:
    """
    Fonction principale à exécuter pour successivement ouvrir la DataFrame contenant les données,
    nettoyer la DataFrame, filtrer par secteurs NAF, ne garder que les magasins proche du centre de Paris,
    séparer par la Seine, clusteriser et sauvegarder dans une carte.
    La répartition entre les secteurs de la Seine est calculée automatiquement.

    :param rayon: le rayon (à partir du centre de Paris).
    :param secteur_NAF: les secteurs NAF à sélectionner.
    :param nb_clusters: le nombre de clusters à calculer.
    :param adresse_map: l'adresse de la carte en sortie.
    :param seine_divide: mettre `True` pour séparer les clusters par la Seine
    :param reduce: mettre :code:`True` pour n'utiliser qu'une version allégée des données (plus rapide).
    :param threshold: nombre de données utilisées si reduce= :code:`True` 

    :return: :code:`None` 
    
    """
    t1 = time.time()
    print("Ouverture de la DataFrame...", end="    ")

    df = nettoyer(pd.read_json("../../data/base_sirene_shortened.json"), reduce=reduce, threshold=threshold)

    if secteur_NAF != [''] :
        list_section = []
        for secteur in secteur_NAF :
            list_section = list_section + NAF_utils.get_NAFs_by_section(secteur).tolist()

        df = NAF_utils.filter_by_naf(df, list_section, "apet700")

    t2 = time.time()
    print(f"{t2-t1:2.3f} s")
    t1 = time.time()
    print("On ne garde que les données du centre...", end="    ")

    df = clusterizer_utils.filter_nearby_paris(df, radius=rayon, is_dict=True)

    t2 = time.time()
    print(f"{t2-t1:2.3f} s")
    t1 = time.time()

    if seine_divide:
        print("On sépare par la Seine...", end="    ")
        masque = rapport_a_la_seine_multiprocessing(df.copy()["geometry"].apply(lambda x: x['coordinates']))

        liste_df = []
        for no_zone in DICT_GDF_ZONES.keys():
            liste_df.append(df[no_zone == masque].reset_index(drop=True))

        t2 = time.time()
        print(f"{t2-t1:2.3f} s")
        t1 = time.time()

        print("Clusterisation...", end="    ")

        liste_df_clusters = []

        nb_clusters_par_zone = calcule_nb_clusters_par_zone(liste_df, nb_clusters)

        for no_zone in range(NB_ZONES):
            try:
                liste_df_clusters.append(
                    clusterize(liste_df[no_zone], nb_clusters_par_zone[no_zone], is_dict=True, weight=True)
                )
            except ValueError:
                liste_df_clusters.append(None)
                nb_clusters_par_zone[no_zone] = 0  # il n'y a pas d'établissements dans cette zone

        t2 = time.time()
        print(f"{t2-t1:2.3f} s")
        t1 = time.time()

    else :
        print("Clusterisation...", end="    ")

        liste_df_clusters = []
        
        liste_df_clusters.append(
            clusterize(df, nb_clusters, is_dict=True, weight=True)
        )

        t2 = time.time()
        print(f"{t2-t1:2.3f} s")
        t1 = time.time()
        
    print("Génération de la carte et sauvegarde...", end="    ")

    nb_deja_faits = 0
    map = save_to_map(liste_df_clusters[0][1])

    for no_zone in range(1, len(liste_df_clusters)):
        nb_deja_faits += nb_clusters_par_zone[no_zone-1]
        if liste_df_clusters[no_zone] != None:
            map = save_to_map(liste_df_clusters[no_zone][1], map=map, nb_avant=nb_deja_faits)

    map.save(adresse_map)

    t2 = time.time()
    print(f"{t2-t1:2.3f} s")
    t1 = time.time()
    print("Terminé !")




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
        # with PyCallGraph(output=GraphvizOutput()):
        #     main_json(rayon=100, adresse_map="output/clusterized_map_with_shapefile_no_convex.html", reduce=True, threshold=10_000)
        main_json(rayon=100, nb_clusters=50,adresse_map="output/clusterized_map_mutiprocessing_shp_full.html")#, reduce=True, threshold=100_000)
        # with PyCallGraph(output=GraphvizOutput()):
        #     main_json(rayon=100, adresse_map="output/clusterized_map_with_shapefile_no_convex.html", reduce=True, threshold=10_000)
        # cProfile.run('main_json(rayon=100, adresse_map="output/clusterized_map_with_shapefile_no_convex.html", reduce=True, threshold=100_000)')

#### au maximum : 
# avant multiprocessing
# $ python clusterizer.py 
# Ouverture de la DataFrame...    6.922 s
# On ne garde que les données du centre...    1.110 s
# On sépare par la Seine...    424.805 s
# Clusterisation...    7.739 s
# Génération de la carte et sauvegarde...    0.108 s
# Terminé !
# -> 440 secondes = 7 minutes 20

# après multiprocessing
# $ python clusterizer.py 
# Ouverture de la DataFrame...    5.678 s
# On ne garde que les données du centre...    0.806 s
# On sépare par la Seine...    322.618 s
# Clusterisation...    14.862 s
# Génération de la carte et sauvegarde...    0.152 s
# Terminé !
