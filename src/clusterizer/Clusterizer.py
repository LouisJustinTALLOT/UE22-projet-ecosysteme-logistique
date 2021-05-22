import geopandas as gpd
import pandas as pd
import numpy as np
import folium

from sklearn.cluster import KMeans

from shapely.geometry import Polygon

from src.clusterizer import NAFUtils
from src.clusterizer import ClusterizerUtils
from src.clusterizer.ClusterizerUtils import COLUMN_HULLS_NAME, \
    COLUMN_CLUSTER_INDEX_NAME, \
    COLUMN_CLUSTER_SIZE_NAME, \
    COLUMN_CENTROIDS_NAME, \
    COLUMN_DEFAULT_GEOMETRY_NAME, \
    COLUMN_CLUSTER_MASS_NAME

"""
Clusterise proprement.
Pour l'instant, n'utilise que l'algorithme des k-moyennes.

Pour avoir des exemples d'utilisation, aller à la toute fin où il y a les tests
TODO : d'autres algorithmes
"""


def nettoyer(df, reduce=False, threshold=1000, column_geometry=COLUMN_DEFAULT_GEOMETRY_NAME):
    """
    Nettoie la DataFrame. Enlève les na, et si spécifié, ne prend que les premières données de la (Geo)DataFrame.

    :param df: La DataFrame.
    :param reduce: Si True, ne prend que les premières données.
    :param threshold: Dans le cas où reduce=True, nombre de données à sélectionner.
    :param column_geometry: A spécifier si la colonne contenant les points n'est pas la colonne par défaut ("geometry")
    :return: Une DataFrame nettoyée.
    """
    if reduce and df.size <= threshold:
        df = df[:threshold]

    return df.dropna(subset=[column_geometry]).reset_index()


def clusterize(df, k, column_geometry=COLUMN_DEFAULT_GEOMETRY_NAME, dict=False):
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
    kmeans = KMeans(n_clusters=k, random_state=0)

    # Ceci contient des coordonnées (x, y) des points
    X = None

    if dict:
        a = pd.Series(df[column_geometry].apply(lambda p: p["coordinates"][0]))
        b = pd.Series(df[column_geometry].apply(lambda p: p["coordinates"][1]))

        X = np.column_stack((a, b))
    else:
        a = pd.Series(df[column_geometry].apply(lambda p: p.x))
        b = pd.Series(df[column_geometry].apply(lambda p: p.y))

        X = np.column_stack((a, b))

    # On ajoute à la DataFrame originale les numéros de cluster pour chaque point.
    df_point_cluster = gpd.GeoDataFrame(kmeans.fit_predict(X), columns=[COLUMN_CLUSTER_INDEX_NAME], dtype=int)
    df = df.join(df_point_cluster)

    # La DataFrame "df_infos_clusters" associe à chaque numéro de cluster les informations correspondantes.
    # En détails : une colonne "centroids" (centres de masse), une colonne "hulls" (enveloppes convexes),
    # une colonne "taille" (nombre d'établissements)
    df_infos_clusters = pd.DataFrame(gpd.points_from_xy(kmeans.cluster_centers_[:, 0],
                                                        kmeans.cluster_centers_[:, 1]),
                                     columns=[COLUMN_CENTROIDS_NAME]
                                     )
    df_infos_clusters = df_infos_clusters.join(ClusterizerUtils.get_infos_clusters_taille(df))
    df_infos_clusters = df_infos_clusters.join(
        ClusterizerUtils.get_infos_clusters_enveloppes_convexes(k, df, column_geometry))

    return df, df_infos_clusters


def save_to_map(df_clusters, path):
    """
    Sauvegarde les informations des clusters dans une carte Leaflet.
    Ne retourne rien.

    :param df_clusters: La DataFrame contenant les informations de chaque cluster
     (cf. deuxième sortie de la fonction clusterize)
    :param path: Le chemin de sortie du fichier.
    """

    map = folium.Map(location=[48.844952, 2.339193],
                     zoom_start=10,
                     tiles="OpenStreetMap"
                     )

    couleurs = ['cadetblue', 'lightblue', 'orange', 'darkred', 'black',
                'purple', 'gray', 'green', 'darkgreen', 'pink', 'lightgreen',
                'darkblue', 'white', 'blue', 'red']

    centroids = df_clusters.loc[:, COLUMN_CENTROIDS_NAME]
    hulls = df_clusters.loc[:, COLUMN_HULLS_NAME]
    sizes = df_clusters.loc[:, COLUMN_CLUSTER_SIZE_NAME]

    for k, point in enumerate(centroids):
        if point is not None:
            title = f"Centre de masse du cluster {k} : {sizes[k]} établissements"
            folium.Marker(location=[point.y, point.x],
                          popup=title,
                          icon=folium.Icon(color=couleurs[k % len(couleurs)], icon='info-sign')
                          ).add_to(map)

    for k, polygon in enumerate(hulls):
        title = f"Cluster {k}"
        if type(polygon) == Polygon:
            # Notre cluster a plus de trois points (autrement, le type serait Point ou LineString)
            # Donc c'est utile d'afficher l'enveloppe convexe
            polygon = ClusterizerUtils.swap_xy(polygon)
            coords = polygon.exterior.coords
            folium.Polygon(locations=coords, popup=title, color=couleurs[k % len(couleurs)]).add_to(map)

    map.save(path)


def test_geojson():
    df = nettoyer(gpd.read_file("../../tests/gis/input/reducted.geojson"))
    df, df_clusters = clusterize(df, 10, dict=False)
    save_to_map(df_clusters, "output/clusterized.html")


def test_json():
    df = nettoyer(pd.read_json("../../data/base_sirene_10000.json"))
    df = NAFUtils.filter_by_naf(df, NAFUtils.get_NAFs_by_section("L"), "apet700")
    df, df_clusters = clusterize(df, 50, dict=True)
    save_to_map(df_clusters, "output/clusterized.html")


def test_naf():
    print(NAFUtils.get_NAFs_by_section("L"))

# On exécute le programme avec la base SIRENE :

test_json()
