import geopandas as gpd
import pandas as pd
import numpy as np
from pandas import Series
from shapely.geometry import Polygon, MultiPoint, Point, LineString

COLUMN_DEFAULT_GEOMETRY_NAME = "geometry"
COLUMN_CLUSTER_INDEX_NAME = "cluster"
COLUMN_HULLS_NAME = "hulls"
COLUMN_CENTROIDS_NAME = "centroids"
COLUMN_CLUSTER_SIZE_NAME = "taille"
COLUMN_CLUSTER_MASS_NAME = "poids"

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

        hull = multi_point.convex_hull

        if type(hull) == Point or type(hull) == LineString:
            # S'il n'y a qu'un point dans le cluster, on ne peut pas créer de Polygon
            temp_hulls[n] = hull
        else:
            temp_hulls[n] = Polygon(hull)

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


vectorized_calculer_poids_code_NAF = np.vectorize(calculer_poids_code_NAF)


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

