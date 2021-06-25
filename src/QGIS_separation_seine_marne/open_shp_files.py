import geopandas as gpd
import folium

DICT_ZONES_IDF = {
    0 : "IDF_zone_est",
    1 : "IDF_zone_nord_ouest",
    2 : "IDF_zone_nord",
    3 : "IDF_zone_Paris_ouest",
    4 : "IDF_zone_sud",
}

DIR_SHP_FILES = "../../data/IDF_5_zones/"


map = folium.Map(
    location=[48.844952, 2.339193],
    zoom_start=10,
    tiles="OpenStreetMap"
)

for i in DICT_ZONES_IDF.keys():
    gdf = gpd.read_file(DIR_SHP_FILES + DICT_ZONES_IDF[i] + ".shp")
    for _, r in gdf.iterrows():
        #without simplifying the representation of each borough, the map might not be displayed
        #sim_geo = gpd.GeoSeries(r['geometry'])
        sim_geo = gpd.GeoSeries(r['geometry'])#.simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j,
                            style_function=lambda x: {'fillColor': 'orange'})
        # folium.Popup().add_to(geo_j)
        geo_j.add_to(map)

map.save("test_5_zones.html")

print(gdf.head())
