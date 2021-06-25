import geopandas as gpd
import folium

DICT_ZONES_IDF = {
    0 : "IDF_zone_est",
    1 : "IDF_zone_nord_ouest",
    2 : "IDF_zone_nord",
    3 : "IDF_zone_Paris_ouest",
    4 : "IDF_zone_sud",
}


gdf = gpd.read_file("IDF_without_water.shp")

map = folium.Map(
    location=[48.844952, 2.339193],
    zoom_start=10,
    tiles="OpenStreetMap"
)

print(gdf.head())
