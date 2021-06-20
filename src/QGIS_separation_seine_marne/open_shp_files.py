import geopandas as gpd
import folium

gdf = gpd.read_file("IDF_without_water.shp")

map = folium.Map(
    location=[48.844952, 2.339193],
    zoom_start=10,
    tiles="OpenStreetMap"
)

print(gdf.head())
