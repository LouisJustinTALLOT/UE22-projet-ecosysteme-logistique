import geopandas as gpd
import folium

from shapely.geometry import Point, Polygon


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

for i in [0]:
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

list_points = [
    (48.5, 2.97),
    (48.4, 2.3),
    (48.38826945754673, 2.958737528893516),
]

for coord in list_points:
    print("within : ", Point(coord[1], coord[0]).within(gdf['geometry'][0]), end=" / ")
    print("contains : ", gdf['geometry'][0].contains(Point(coord[1], coord[0])))
    folium.Marker(
        location=coord, popup=f"{Point(coord[1], coord[0]).within(gdf['geometry'][0])}"
        # location=coord, popup=f"Contains {gdf['geometry'][0].contains(Point(coord[1], coord[0]))}"
    ).add_to(map)

# print([a for a in gdf["geometry"]][0])

# gpd.GeoSeries.

map.save("test_point_in_zone.html")

print(gdf.head())
# gdf = gpd.read_file(DIR_SHP_FILES + DICT_ZONES_IDF[0] + ".shp")
# # print(gdf.head())
# print(gdf["geometry"])
# print(Point(48.5, 2.97) in gdf["geometry"])