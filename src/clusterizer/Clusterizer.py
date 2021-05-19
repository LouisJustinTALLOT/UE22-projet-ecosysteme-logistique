import geopandas as gpd
import pandas as pd
import numpy as np
import folium

from sklearn.cluster import KMeans

from shapely.geometry import Point

from src.clusterizer import ClusterizerUtils
from src.clusterizer.ClusterizerUtils import COLUMN_HULLS_NAME,\
    COLUMN_CLUSTER_INDEX_NAME,\
    COLUMN_CLUSTER_SIZE_NAME,\
    COLUMN_CENTROIDS_NAME,\
    COLUMN_DEFAULT_GEOMETRY_NAME,\
    COLUMN_CLUSTER_MASS_NAME

"""
Clusterise proprement (k-moyennes)

Pour avoir des exemples d'utilisation, aller à la toute fin où il y a les tests
TODO : d'autres algorithmes
"""




def nettoyer(df, reduce=False, threshold=1000, column_geometry=COLUMN_DEFAULT_GEOMETRY_NAME):
    """
    Nettoie la DataFrame: enlève les na
    Si reduce=True, ne prend que les première données de la (Geo)DataFrame.
    La limite dans ce cas est fixée à threshold (qui vaut 1000 par défaut)
    Spécifier la colonne où se trouvent les données géographiques si ce n'est pas dans "geometry"
    """
    if reduce and df.size <= threshold:
        df = df[:threshold]

    return df.dropna(subset=[column_geometry]).reset_index()




def clusterize(df, k, column_geometry=COLUMN_DEFAULT_GEOMETRY_NAME, dict=False):
    """
    Clusterise à l'aide de l'algorithme des k-moyennes.

    A besoin d'une DataFrame contenant une colonne avec des Points (par défaut, son nom est geometry)
    Indiquer dict=True si jamais la colonne contenant les Points ne contient 
    pas l'objet Point (module shapely), mais un dictionnaire 
    (quand ça vient pas d'un GeoJSON en général)

    Attention, fait du en-place.
    Retourne deux choses :
    - la df rentrée, avec une seule colonne en plus:
            "cluster" (numéro du cluster).
            Ainsi, pour chaque point, on connaît le numéro du cluster qui lui a été affecté.
    - une nouvelle GeoDataFrame contenant plusieurs colonnes :
        l'index correspond au numéro du cluster
        "centroids" (le centre de masse)
        "hulls"     (les enveloppes convexes)
        "taille"    (le nombre d'établissements dans ce cluster, indépendant de la notion de masse)
        En quelque sorte, c'est la clé de lecture.
    """

    #===========================================================
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

    # La DataFrame "df_point_cluster" associe à chaque indice de ligne (ie à chaque point)
    # son numéro de cluster (dans la colonne "cluster").
    # Son utilité n'est que d'ajouter la colonne "clusters" sur la DataFrame originale.
    # La DataFrame originale contient désormais une colonne en plus, "cluster" contenant le numéro du cluster.
    df_point_cluster = gpd.GeoDataFrame(kmeans.fit_predict(X), columns=[COLUMN_CLUSTER_INDEX_NAME], dtype=int)
    df = df.join(df_point_cluster)

    # La DataFrame "df_infos_clusters" associe à chaque numéro de cluster les informations correspondantes.
    # En détails : une colonne "centroids" (centres de masse) et une colonne "hulls" (enveloppes convexes)
    df_infos_clusters = pd.DataFrame(gpd.points_from_xy(kmeans.cluster_centers_[:, 0],
                                                kmeans.cluster_centers_[:, 1]),
                             columns=[COLUMN_CENTROIDS_NAME]
                            )
    df_infos_clusters = df_infos_clusters.join(ClusterizerUtils.enveloppe_convexe(k, df, column_geometry))

    # ===================================================
    # RESULTATS
    # df contient une seule colonne en plus :
    #       "cluster" (n° cluster).
    # df_infos_clusters contient les détails de chaque cluster (numéro, enveloppe convexe, centre de masse, etc.)
    # En qqes sorte, c'est la clé de lecture
    # ==================================================

    return df, df_infos_clusters



def save_to_map(df_clusters, path):
    """
    Sauvegarde les centres de gravité des clusters, ainsi que les enveloppes convexes, dans une carte Leaflet
    :param df_clusters: les centres de gravité et les enveloppes convexes
    (cf. deuxième sortie de la fonction clusterize)
    :param path: le chemin
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

    for k, point in enumerate(centroids):
        if point is not None:
            title = f"Centre de masse du cluster {k}"
            folium.Marker(location=[point.y, point.x], 
                          popup=title,
                          icon=folium.Icon(color=couleurs[k%len(couleurs)], icon='info-sign')
            ).add_to(map)

    for k, polygon in enumerate(hulls):
        title = f"Cluster {k}"
        if type(polygon) == Point:
            # on est face à un cluster d'un seul point...
            folium.Marker(location=[polygon.y, polygon.x], popup=title,
                          icon=folium.Icon(color=couleurs[k%len(couleurs)], icon='info-sign')).add_to(map)
        else:
            polygon = ClusterizerUtils.swap_xy(polygon)
            coords = polygon.exterior.coords
            folium.Polygon(locations=coords, popup=title, color=couleurs[k%len(couleurs)]).add_to(map)

    map.save(path)


def informations(df, df_clusters):
    """ 
    Permet d'ajouter des informations sur les clusters.
    Pour l'instant, ajoute le nombre d'entreprises du cluster dans une colonne "taille".
    On pourra par exemple ajouter aussi le poids total de chaque cluster quand on aura défini cette notion
    """

    taille_cluster = pd.DataFrame(df.groupby(COLUMN_CLUSTER_INDEX_NAME).size(), columns=[COLUMN_CLUSTER_SIZE_NAME])
    df_clusters = df_clusters.join(taille_cluster)
    # print(df_cluster.head())


def test_geojson():
    df = nettoyer(gpd.read_file("../../tests/gis/input/reducted.geojson"))
    df, df_clusters = clusterize(df, 10, dict=False)
    save_to_map(df_clusters, "output/clusterized.html")


def test_json():
    df = nettoyer(pd.read_json("../../data/base_sirene_10000.json"))
    df, df_clusters = clusterize(df, 50, dict=True)
    save_to_map(df_clusters, "output/clusterized.html")
    # informations(df, df_clusters)


# On exécute le programme avec la base SIRENE : 

test_json()