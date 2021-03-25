import geopandas as gpd
import folium
from folium.plugins import MarkerCluster

"""
Ce fichier permet d'analyser la BAN
"""

reducted_name = "input\\reducted.geojson"
name = "input\\base-adresse-75.geojson"

reducted_output_path = "output\\reducted_map.html"
output_path = "output\\map.html"

def ouvrir(reducted=True):
    print("Ouverture...")
    """
    Ouvre la GeoDataFrame de la base de donnée réduite
    :return: la GeoDataFrame correspondante
    """
    if(reducted):
        return gpd.read_file(reducted_name)
    else:
        return gpd.read_file(name)

def filter(df):
    print("Filtrage...")
    return df.loc[:, 'geometry']

def afficher(df, reducted=True):
    print("Affichage...")
    init_location = df[0]
    map = folium.Map(location=[init_location.y, init_location.x], zoom_start=10, tiles="OpenStreetMap")
    marker_cluster = MarkerCluster().add_to(map)

    for point in df:
        if point is not None:
            folium.Marker(location=[point.y, point.x], popup="Point à livrer", icon= folium.Icon(color='red', icon='info-sign')).add_to(marker_cluster)

    if reducted:
        map.save(reducted_output_path)
    else:
        map.save(output_path)


df = filter(ouvrir(reducted=True))
afficher(df, reducted=True)