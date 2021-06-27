from functools import reduce
from pprint import pprint
import geopandas as gpd
import math
import pandas as pd
import numpy as np
from pandas import Series
from shapely.geometry import Polygon, MultiPoint, Point, LineString, GeometryCollection
from shapely.geometry.multipolygon import MultiPolygon
from . import concave_hull_utils

COLUMN_DEFAULT_GEOMETRY_NAME = "geometry"
COLUMN_CLUSTER_INDEX_NAME = "cluster"
COLUMN_HULLS_NAME = "hulls"
COLUMN_CENTROIDS_NAME = "centroids"
COLUMN_CLUSTER_SIZE_NAME = "taille"
COLUMN_CLUSTER_MASS_NAME = "poids"



PARIS_CENTER_COORDS = Point(2.348523, 48.853345)

# =====================
# Fonctions principales
# =====================


def get_infos_clusters_poids(df, column_naf_code):
    """
    Fonction permettant de récupérer des infos sur les clusters (poids).

    :param df: La DataFrame où l'on a déjà ajouté le numéro des clusters (laissée intacte).
    :param column_naf_code: La colonne où se situent les codes NAF.
    :return: Une nouvelle GeoDataFrame associant à chaque numéro de cluster le poids de celui-ci
     (assez arbitraire pour l'instant)
    """

    series_poids = df.groupby(COLUMN_CLUSTER_INDEX_NAME).apply(calculer_poids_cluster_wrapper(column_naf_code))
    return pd.DataFrame(Series(series_poids), columns=[COLUMN_CLUSTER_MASS_NAME])


def get_infos_clusters_taille(df):
    """
    Fonction permettant de récupérer des infos sur les clusters (tailles).

    :param df: La DataFrame où l'on a déjà ajouté le numéro des clusters (laissée intacte).
    :return: Une nouvelle GeoDataFrame associant à chaque numéro de cluster la taille de celui-ci
     (nombre d'établissements)
    """
    return pd.DataFrame(df.groupby(COLUMN_CLUSTER_INDEX_NAME).size(), columns=[COLUMN_CLUSTER_SIZE_NAME])

def get_infos_clusters_enveloppes_convexes(k, df, column_geometry=COLUMN_DEFAULT_GEOMETRY_NAME):
    """
    Fonction permettant de récupérer des infos sur les clusters (enveloppes convexes).

    :param k: Nombre de clusters
    :param df: La DataFrame où l'on a déjà ajouté le numéro des clusters (laissée intacte).
    :param column_geometry: Le nom de la colonne où se situent les données géometriques (par défaut, "geometry").
    :return: Une GeoDataFrame associant à chaque numéro de cluster son enveloppe convexe.
    """
    # Tableau numpy temporaire. Il ne sert qu'à la création de la GeoDataFrame avec les enveloppes convexes
    temp_hulls = np.empty(k, dtype=Polygon)

    for n in range(k):
        # Cette DataFrame contient les points du cluster numéro n
        minidf = df.loc[df[COLUMN_CLUSTER_INDEX_NAME] == n]

        # On calcule l'enveloppe convexe
        points = minidf.loc[:, column_geometry]
        if dict:
            points = gpd.points_from_xy(points.apply(lambda p: p["coordinates"][0]),
                                        points.apply(lambda p: p["coordinates"][1]))

            multi_point = MultiPoint(np.array(points, dtype=Point))
        else:
            multi_point = MultiPoint(points.array)

        # hull = multi_point.convex_hull
        # temp_hulls[n] = Polygon(Polygon(multi_point).boundary.coords)
        hull = list(Polygon(multi_point).boundary.coords)
        # pprint(hull)
        # raise Exception("")

        # center = reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]), hull, (0, 0))
        # center = (center[0] / len(hull), (center[1] / len(hull)))

        # hull.sort(key = lambda a: math.atan2(a[1] - center[1], a[0] - center[0]))

        # temp_hulls[n] = Polygon(hull)

        # pprint(concave_hull_utils.alpha_shape(hull))

        alpha = Polygon(hull).area
        # print(n, Polygon(hull).area)
        # if Polygon(hull).area > 0.001: # hardcodé, d'après les résultats du print au-dessus
        #     temp_hulls[n] = concave_hull_utils.alpha_shape(hull, alpha=0.02)[0]
        # else:
        #     temp_hulls[n] = concave_hull_utils.alpha_shape(hull, alpha=0.01)[0]
        result_hull = concave_hull_utils.alpha_shape(hull, alpha=alpha)[0]
        n_iter = 0
        while n_iter<5 and ((type(result_hull) == MultiPolygon and len(result_hull) > 3) or result_hull.area < 10*Polygon(hull).area):
            # print(alpha)
            alpha *= 2
            result_hull = concave_hull_utils.alpha_shape(hull, alpha=alpha)[0]
            n_iter += 1

        temp_hulls[n] = result_hull
        # raise Exception("")

        # if type(hull) == Point or type(hull) == LineString or type(hull) == GeometryCollection:
        #     # S'il n'y a qu'un point dans le cluster, on ne peut pas créer de Polygon
        #     temp_hulls[n] = hull
        # else:
        # try:
        #     temp_hulls[n] = Polygon(hull)
        # except Exception as e:
        #     print(e)
        #     temp_hulls[n] = hull

    return gpd.GeoDataFrame(gpd.GeoSeries(temp_hulls), columns=[COLUMN_HULLS_NAME])

# =====================
# Fonctions utilitaires
# =====================

def calculer_poids_code_NAF(code_naf):
    """
    Calcule le poids d'un code NAF.
    Assez arbitraire pour le moment.

    :param code_naf: Le code NAF à calculer (avec ou sans point).
    :return: Le poids du code NAF (entier).
    """
    debut = int(str(code_naf)[0:2])

    if 49 <= debut <= 56:
        return 4

    return 1


vectorized_calculer_poids_code_NAF = np.vectorize(calculer_poids_code_NAF, otypes=[int])


def calculer_poids_cluster(df, column_naf_code):
    """
    Calcule le poids d'un ensemble d'établissements.

    :param df: La DataFrame contenant tous les établissements.
     Rien n'est requis, à part avoir une colonne où sont situés les codes NAF.
    :param column_naf_code: Le nom de la colonne contenant les codes NAF.
    :returns: Le poids (entier) du cluster.
    """
    return np.sum(vectorized_calculer_poids_code_NAF(df[column_naf_code]))


def calculer_poids_cluster_wrapper(column_naf_code):
    """
    Wrappe calculer_poids_cluster pour pouvoir l'utiliser dans un groupby.
    :param column_naf_code: La colonne où se situent les codes NAF.
    :return: cf. la fonction calculer_poids_cluster.
    """

    def fct(df):
        return calculer_poids_cluster(df, column_naf_code)

    return fct

def swap_xy(geom):
    """
    Inverse les coordonnées de l'objet shapely.geometry.
    Utile pour passer objets shapely dans folium (la convention est inversée).

    :param geom: L'objet dont on veut inverser les coordonnées (Point, Polygon, MultiPolygon, etc.)
    :return: l'objet inversé
    """
    if geom.is_empty:
        return geom

    if geom.has_z:
        def swap_xy_coords(coords):
            for x, y, z in coords:
                yield (y, x, z)
    else:
        def swap_xy_coords(coords):
            for x, y in coords:
                yield (y, x)

    # Process coordinates from each supported geometry type
    if geom.type in ('Point', 'LineString', 'LinearRing'):
        return type(geom)(list(swap_xy_coords(geom.coords)))

    elif geom.type == 'Polygon':
        ring = geom.exterior
        shell = type(ring)(list(swap_xy_coords(ring.coords)))
        holes = list(geom.interiors)

        for pos, ring in enumerate(holes):
            holes[pos] = type(ring)(list(swap_xy_coords(ring.coords)))

        return type(geom)(shell, holes)

    elif geom.type.startswith('Multi') or geom.type == 'GeometryCollection':
        # Recursive call
        return type(geom)([swap_xy(part) for part in geom.geoms])

    else:
        raise ValueError('Type %r not recognized' % geom.type)


def filter_nearby_paris(df, radius, column_geometry=COLUMN_DEFAULT_GEOMETRY_NAME, dict=False):
    """
    Filtre les données proches du centre de Paris.
   
    :param df: la DataFrame à filtrer
    :param radius: le rayon (en kilomètres)
    :param column_geometry: la colonne où se trouvent les données géométriques (par défaut : 'geometry')
    :return: la DataFrame filtrée
    """
    X = get_coords_from_object(df, column_geometry, dict)

    l1 = np.pi/180*PARIS_CENTER_COORDS.y
    L1 = np.pi/180*PARIS_CENTER_COORDS.x
    l2 = np.pi/180*X[:,1]
    L2 = np.pi/180*X[:,0]

    distances = 20000/np.pi * (np.arccos(np.sin(l1)*np.sin(l2) + np.cos(l1)*np.cos(l2)*np.cos(L1-L2)))
    masque = distances <= radius
    return df[masque].reset_index()


def get_coords_from_object(df, column_geometry=COLUMN_DEFAULT_GEOMETRY_NAME, dict=False):
    """
    Récupère les coordonnées des points de la DataFrame.

    :param df: la DataFrame.
    :param column_geometry: la colonne contenant les données géométriques.
    :param dict: les données sont-elles en dictionnaire ?
    :return: les coordonnées sous la forme d'une matrice de deux colonnes (et d'autant de lignes qu'il y a de points)
    """
    if dict:
        a = pd.Series(df[column_geometry].apply(lambda p: p["coordinates"][0]))
        b = pd.Series(df[column_geometry].apply(lambda p: p["coordinates"][1]))

        X = np.column_stack((a, b))
    else:
        a = pd.Series(df[column_geometry].apply(lambda p: p.x))
        b = pd.Series(df[column_geometry].apply(lambda p: p.y))

        X = np.column_stack((a, b))

    return X