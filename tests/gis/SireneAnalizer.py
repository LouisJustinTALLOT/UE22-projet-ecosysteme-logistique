import geopandas as gpd
import pandas as pd
import numpy as np
import folium
from sklearn.cluster import KMeans
from shapely.geometry import Point, MultiPoint, Polygon
from shapely.geometry.base import BaseGeometry
import matplotlib.pyplot as plt

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

reducted_name = "input\\base_sirene_shortened_json_cpp.json"

clusterized_path = "output\\clusterized_sirene.html"

# Fonction utilitaire

def swap_xy(geom:BaseGeometry):
    """
    Inverse les coordonnées de l'objet shapely.geometry.
    Utile pour passer objets shapely dans folium (la convention est inversée)
    :param geom: l'objet dont on veut inverser les coordonnées (Point, Polygon, MultiPolygon, etc.)
    :return: l'objet inversé
    """
    if geom.is_empty:
        return geom

    if geom.has_z:
        def swap_xy_coords(coords:tuple):
            for x, y, z in coords:
                yield (y, x, z)
    else:
        def swap_xy_coords(coords:tuple):
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


def range_hex_colors(nombre_couleurs:int):
    res = []
    # for i in range(nombre_couleurs):
    #     res.append(f"#AB{str(hex(i*255//nombre_couleurs))[2:].upper()}BA")
    tmp = 17
    for i in range(nombre_couleurs):
        res.append("#"
                 + str(hex(255-tmp//2)[2:].upper())
                 + str(hex(tmp)[2:].upper())
                 + str(hex(128-tmp//4)[2:].upper())
        )
        tmp += 255//nombre_couleurs

    return res

def ouvrir(path:str, column_points:str='geometry', reduce:bool=False, do_filter:bool=True):
    """
    Ouvre la GeoDataFrame du chemin spécifié.

    :param path: chemin du fichier
    :param column_points: la colonne où se trouvent les points
    :param reduce: si True, extrait uniquement 1000 lignes de la GeoDataFrame (pour accélérer le temps de calcul)
    :param do_filter: si True, ne garde que la colonne contenant les points (allège)
    :return: Retourne une GeoDataFrame. Elle ne contient pas de na. Si do_filter est True, l'unique colonne porte le nom 'geometry'.
    """
    return filter(pd.read_json(path), column_points, reduce, do_filter)

def filter(df:gpd.GeoDataFrame, column_points:str='geometry', reduce:bool=False, do_filter:bool=True):
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


def clusterize(df:gpd.GeoDataFrame, nb_clusters:int):
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
    # [[ 2.348872 48.863495]
    #   ...
    #  [ 2.396281 48.864938]]
    a = pd.Series(df['geometry'].apply(lambda p: p["coordinates"][0]))
    b = pd.Series(df['geometry'].apply(lambda p: p["coordinates"][1]))
    X = np.column_stack((a, b))

    # https://samdotson1992.github.io/SuperGIS/blog/k-means-clustering/
    # wcss = []
    # for i in range(1, 14):
    #     kmeans2 = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
    #     kmeans2.fit(X)
    #     wcss.append(kmeans2.inertia_)
    # plt.plot(range(1, 14), wcss)
    # plt.title('The Elbow Method')
    # plt.xlabel('Number of clusters')
    # plt.ylabel('WCSS')
    # plt.show()

    kmeans = KMeans(n_clusters=nb_clusters, random_state=0)
    y_kmeans = kmeans.fit_predict(X)
    k = pd.DataFrame(y_kmeans, columns=['cluster'], dtype=int)

    gdf = gpd.GeoDataFrame(df.join(k))

    lieux = np.array([np.array(gdf['geometry'], dtype=dict)[i]['coordinates'] for i in range(len(gdf['geometry']))])

    # plt.figure()
    # plt.scatter(np.array(lieux)[:,0],
    #          np.array(lieux)[:,1],
    #          c=gdf['cluster'],
    #          marker='.'
    # )

    # plt.figure()
    # plt.scatter(np.array(lieux)[:,0],
    #          np.array(lieux)[:,1],
    #          c=y_kmeans,
    #          marker='.'
    # )   


    plt.figure()
    plt.scatter(a,b,c=y_kmeans,marker='.')
    # plt.show()

    cluster_centers = kmeans.cluster_centers_
    # centers = gpd.points_from_xy(cluster_centers[:,0], cluster_centers[:,1])

    plt.scatter(cluster_centers[:,0], cluster_centers[:,1], color="red", marker='+')

    # centroids = pd.DataFrame(centers, columns=['centroids'])
    plt.savefig("output/clusterized_data_k_means_debug.pdf")

    plt.show()

    # with open("output/clusters.csv", 'w', encoding="utf8") as file:
    #     file.write(df.to_csv(sep=";"))

    return df, centroids


def do_convex_hull(df:gpd.GeoDataFrame):
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
        points = gpd.points_from_xy(points.apply(lambda p: p["coordinates"][0]), 
                                    points.apply(lambda p: p["coordinates"][1]))

        multi_point = MultiPoint(np.array(points))

        hull = multi_point.convex_hull
        if type(hull) == Point:
            hulls[n] = hull
        else:
            hulls[n] = Polygon(hull)

    pre_df = gpd.GeoDataFrame(gpd.GeoSeries(hulls), columns=['hulls'])

    df = df.join(pre_df, how='left', on='cluster')

    return df, pre_df


def save_to_map(centroids:gpd.GeoDataFrame, hulls:gpd.GeoDataFrame, path:str=clusterized_path, df:gpd.GeoDataFrame=None):
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

    list_colors = range_hex_colors(len(centroids))
    list_base_colors = ['purple', 'white', 'black', 'lightgray', 'lightgreen', 'green', 'beige', 'blue', 'lightblue', 'lightred', 'darkgreen', 'orange', 'darkred', 'pink', 'gray', 'darkpurple', 'red', 'darkblue', 'cadetblue']

    for k, point in enumerate(centroids):
        if point is not None:
            title = f"Centre de masse du cluster {k}"
            folium.Marker(location=[point.y, point.x], 
                          popup=title,
                          icon=folium.Icon(icon_color=list_colors[k], icon='info-sign')
            ).add_to(map)

    for k, polygon in enumerate(hulls):
        title = f"Cluster {k}"
        if(type(polygon) == Point):
            # on est face à un cluster d'un seul point...
            folium.Marker(location=[polygon.y, polygon.x],
                          popup=title,
                          icon=folium.Icon(color=list_base_colors[k%19], icon='info-sign')
            ).add_to(map)
        else:
            polygon = swap_xy(polygon)
            coords = polygon.exterior.coords
            folium.Polygon(locations=coords, 
                           popup=title, 
                           color=list_colors[k]
            ).add_to(map)

    if df is not None:
        points = df['geometry']

        for point in points:
            folium.Marker(location=(point['coordinates'][1], point['coordinates'][0]),
                          icon=folium.Icon(color="cadetblue", icon='info-sign')
            ).add_to(map)

    map.save(path)

# Ouverture de la GeoDataFrame
data = ouvrir(reducted_name, reduce=True)
data_0 = data.copy()
# Je calcule les clusters, et les centres de gravité
data, centroids = clusterize(data, 4)# 10)
# Je calcule les enveloppes convexes
data, hulls = do_convex_hull(data)
# Je sauvegarde sur une carte
save_to_map(centroids, hulls)#, df=data_0)
