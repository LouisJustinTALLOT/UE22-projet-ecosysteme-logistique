import geopandas as gpd
import pandas as pd
import numpy as np
import folium
from sklearn.cluster import KMeans
from shapely.geometry import Point, MultiPoint, Polygon

"""
Ce fichier permet de faire du clustering :
- formation des clusters
- calcul des centres de gravité pour chaque cluster
- calcul des enveloppes convexes de chaque cluster
- sauvegarde dans une carte Leaflet

Le fichier ne prend pas encore ne compte le poids.

Requis :
- la GeoDataFrame doit contenir une colonne avec les points (par défaut, 'geometry')

Exemple d'utilisation :
# Ouverture de la GeoDataFrame
data = ouvrir(reducted_name)
# Je calcule les clusters, et les centres de gravité
data, centroids = clusterize(data, 5)
# Je calcule les enveloppes convexes
data, hulls = do_convex_hull(data)
# Je sauvegarde sur une carte
save_to_map(centroids, hulls)
"""

reducted_name = "input\\reducted.geojson"

clusterized_path = "output\\clusterized.html"

# Fonction utilitaire

def swap_xy(geom):
    """
    Inverse les coordonnées de l'objet shapely.geometry.
    Utile pour passer objets shapely dans folium (la convention est inversée)
    :param geom: l'objet dont on veut inverser les coordonnées (Point, Polygon, MultiPolygon, etc.)
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



def ouvrir(path, column_points='geometry', reduce=False, do_filter=True):
    """
    Ouvre la GeoDataFrame du chemin spécifié.

    :param path: chemin du fichier
    :param column_points: la colonne où se trouvent les points
    :param reduce: si True, extrait uniquement 1000 lignes de la GeoDataFrame (pour accélérer le temps de calcul)
    :param do_filter: si True, ne garde que la colonne contenant les points (allège)
    :return: Retourne une GeoDataFrame. Elle ne contient pas de na. Si do_filter est True, l'unique colonne porte le nom 'geometry'.
    """
    return filter(gpd.read_file(path), column_points, reduce, do_filter)

def filter(df, column_points='geometry', reduce=False, do_filter=True):
    """
    Filtre la GeoDataFrame : enlève les na.
    Si do_filter=True, ne garde que la colonne contenant les points (allège)

    :param df: la GeoDataFrame
    :param column_points: la colonne où se trouvent les points
    :param reduce: si True, extrait uniquement 1000 lignes de la GeoDataFrame (pour accélérer le temps de calcul)
    :param do_filter: si True, ne garde que la colonne contenant les points (allège)
    :return: Retourne une GeoDataFrame. Elle ne contient pas de na. Si do_filter est True, l'unique colonne porte le nom 'geometry'.
    """
    if not do_filter:
        return df.dropna()

    df = df.loc[:, column_points]
    if reduce:
        return gpd.GeoDataFrame(df.dropna()[0:1000])
    else:
        return gpd.GeoDataFrame(df.dropna())


def clusterize(df, k):
    """
    Clusterise la GeoDataFrame à l'aide de la méthode des k-moyennes.
    La colonne contenant les points doit s'appeler 'geometry'.
    La GeoDataFrame peut contenir d'autres colonnes.

    :param df: la GeoDataFrame à clusteriser (les données doivent se trouver dans la colonne 'geometry')
    :param k: le nombre de clusters
    :return:
    Retourne un tuple.
    En premier : une GeoDataFrame identique, à ceci près que l'on a ajouté les colonnes 'cluster' et 'centroids'.
    (correspondant au numéro du cluster, et à son centre de gravité)
    En deuxième, une GeoDataFrame plus simple avec une unique colonne 'centroids'
    (la ligne est le numéro de cluster, et contient le centre de gravité)
    """

    # On commence par transformer la GeoDataFrame en tableau numpy
    # C'est les lat / lon
    a = pd.Series(df['geometry'].apply(lambda p: p.x))
    b = pd.Series(df['geometry'].apply(lambda p: p.y))
    X = np.column_stack((a, b))

    kmeans = KMeans(n_clusters=k, init='k-means++')
    y_kmeans = kmeans.fit_predict(X)
    k = pd.DataFrame(y_kmeans, columns=['cluster'], dtype=int)

    cluster_centers = kmeans.cluster_centers_
    centers =gpd.points_from_xy(cluster_centers[:,0], cluster_centers[:,1])
    centroids = pd.DataFrame(centers, columns=['centroids'])

    k = k.join(centroids, how="left", on="cluster")
    df = df.join(k)
    return df, centroids


def do_convex_hull(df):
    """
    A partir de données clusterisées (le premier élément retourné par la fonction clusterize)
    (cf. doc de la fonction clusterize), fabrique les enveloppes convexes.

    :param df: la GeoDataFrame où les clusters ont déjà été calculés par la fonction clusterize
    :return:
    Retourne un tuple.
    En premier : une GeoDataFrame identique, à ceci près que l'on a ajouté la colonne 'hulls'.
    (correspondant à un Polygon, enveloppe convexe du cluster)
    (il se peut que ce soit un Point, si le cluster ne contient qu'un point, car les Polygons à un point sont interdits)
    En deuxième, une GeoDataFrame plus simple avec une unique colonne 'hulls'
    (la ligne est le numéro de cluster, et contient les enveloppes convexes)
    """

    # Nombre de clusters
    k = int(np.max(df['cluster']) + 1)

    hulls = np.empty(k, dtype=Polygon)

    for n in range(k):
        # df du cluster correspondant
        minidf = df.loc[df['cluster'] == n]

        points = minidf.loc[:, 'geometry']

        multi_point = MultiPoint(points.array)

        hull = multi_point.convex_hull

        if type(hull) == Point:
            hulls[n] = hull
        else:
            hulls[n] = Polygon(hull)

    pre_df = gpd.GeoDataFrame(gpd.GeoSeries(hulls), columns=['hulls'])

    df = df.join(pre_df, how='left', on='cluster')

    return df, pre_df


def save_to_map(centroids, hulls, path=clusterized_path):
    """
    Sauvegarde les centres de gravité des clusters, ainsi que les enveloppes convexes, dans une carte Leaflet
    :param centroids: les centres de gravité (cf. deuxième sortie de la fonction clusterize)
    :param hulls: les enveloppes convesxes (cf. deuxième sortie de la fonction do_convex_hull)
    :param path: le chemin
    """

    init_location = centroids.loc[0, 'centroids']
    map = folium.Map(location=[init_location.y, init_location.x], zoom_start=10, tiles="OpenStreetMap")

    centroids = centroids.loc[:, 'centroids']
    hulls = hulls.loc[:, 'hulls']

    k = 0
    for point in centroids:
        if point is not None:
            title = "Centre de masse cluster", k
            folium.Marker(location=[point.y, point.x], popup=title,
                          icon=folium.Icon(color='red', icon='info-sign')).add_to(map)
        k+=1

    for polygon in hulls:
        if(type(polygon) == Point):
            # on est face à un cluster d'un seul point...
            title = "Cluster", k
            folium.Marker(location=[polygon.y, polygon.x], popup=title,
                          icon=folium.Icon(color='red', icon='info-sign')).add_to(map)
        else:
            polygon = swap_xy(polygon)
            coords = polygon.exterior.coords
            folium.Polygon(locations=coords, popup="Cluster").add_to(map)

    map.save(clusterized_path)