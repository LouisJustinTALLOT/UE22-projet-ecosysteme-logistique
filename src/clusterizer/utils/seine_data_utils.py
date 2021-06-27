from pathlib import Path
from typing import Dict
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon
from shapely.strtree import STRtree

FILE_PATH = Path(__file__).resolve()
BASE_DIR = FILE_PATH.parent.parent.parent.parent

DICT_ZONES_IDF = {
    0 : "IDF_zone_est",
    1 : "IDF_zone_nord_ouest",
    2 : "IDF_zone_nord",
    3 : "IDF_zone_Paris_ouest",
    4 : "IDF_zone_sud",
}

DIR_SHP_FILES = BASE_DIR/"data/IDF_5_zones/"

DICT_GDF_ZONES: Dict[int, Polygon] = {}

for i in DICT_ZONES_IDF.keys():
    DICT_GDF_ZONES[i] = gpd.read_file(DIR_SHP_FILES/( DICT_ZONES_IDF[i] + ".shp"))['geometry'][0]

# pprint(DICT_GDF_ZONES[0].contains(Point(2.3, 48.4)))

# pprint([(i, pformat(DICT_GDF_ZONES[i])) for i in DICT_ZONES_IDF.keys()])

# raise BaseException

NB_ZONES = len(DICT_ZONES_IDF)

@np.vectorize
def rapport_a_la_seine(xy):
    coord = (xy[0], xy[1])

    for no_zone, gdf in DICT_GDF_ZONES.items():
        if Point(*coord).within(gdf):
            # print(coord, no_zone)
            return no_zone

    # print(coord, "out of all zones")
    return NB_ZONES

def rapport_a_la_seine_spatial_index(array_coords: np.ndarray):
    """
    
    """
    # on crée d'abord des shapely.geometry.Point 
    # pour tous les points de la base de données


    # with np.printoptions(threshold=np.inf):
    #     print(repr(array_coords))
    # array_coords.tofile("points", ",")

    list_points_array_coords = list(map(lambda x: Point(*x), list(array_coords)))

    # un R-Tree
    points_tree = STRtree(list_points_array_coords)

    # pprint(points_tree)
    
    dict_res_appartenance = {}
    # puis on va faire l'intersection de tous ces points avec nos polygones
    # en utilisant des R-Trees  
    for no_zone, polygon in DICT_GDF_ZONES.items():
        # print(len([o for o in points_tree.query(polygon) if o.intersects(polygon)]))
        dict_res_appartenance[no_zone] = [o for o in points_tree.query(polygon) if o.intersects(polygon)]
        print(len(dict_res_appartenance[no_zone]))
    
    res = -1 * np.ones(array_coords.shape[0], dtype=int)
    # print(res)
    # return
    for i in range(len(res)):
        for no_zone, list_appartenance in dict_res_appartenance.items():
            if list_points_array_coords[i] in list_appartenance:
                res[i] = int(no_zone)
                break
        # print(res[i])
        if res[i] == -1:
            res[i] = NB_ZONES
 
    return res
    
