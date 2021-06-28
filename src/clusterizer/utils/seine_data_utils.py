from pathlib import Path
from pprint import pprint
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
def rapport_a_la_seine(xy) -> int:
    """
    Trouve la zone dans laquelle le point situé aux coordonnées considérées est situé


    :param xy: Un tuple contenant les deux coordonnées (longitude, latitude) du point
    :return: Le numéro de la zone dans laquelle le point est situé
    """
    coord = (xy[0], xy[1])

    for no_zone, gdf in DICT_GDF_ZONES.items():
        if Point(*coord).within(gdf):
            # print(coord, no_zone)
            return no_zone

    # print(coord, "out of all zones")
    return NB_ZONES


def rapport_a_la_seine_spatial_index(array_coords: np.ndarray) -> np.ndarray:
    """
    Trouve les zones où se situent les points de l':code:`array` fournie.
    Utilise un *R-Tree* pour ce faire pour accélérer le calcul.

    :param array_coords: Array (nb_points, 2) contenant les coordonnées des points
    :return: une array "masque" qui a chaque point associe son numéro de zone
    """
    # on crée d'abord des shapely.geometry.Point 
    # pour tous les points de la base de données


    # with np.printoptions(threshold=np.inf):
    #     print(repr(array_coords))
    # array_coords.tofile("points", ",")

    list_points_array_coords = list(map(lambda x: Point(*x), list(array_coords)))

    index_by_id = dict((id(pt), i) for i, pt in enumerate(list_points_array_coords))

    # un R-Tree
    points_tree = STRtree(list_points_array_coords)

    dict_res_appartenance = {}
    # puis on va faire l'intersection de tous ces points avec nos polygones
    # en utilisant des R-Trees  
    for no_zone, polygon in DICT_GDF_ZONES.items():
        # print(len([o for o in points_tree.query(polygon) if o.intersects(polygon)]))
        dict_res_appartenance[no_zone] = [o for o in points_tree.query(polygon) if o.intersects(polygon)]
        print(len(dict_res_appartenance[no_zone]))
    
    # res = -1 * np.ones(array_coords.shape[0], dtype=int)
    # # print(res)
    # # return
    # for i in range(len(res)):
    #     for no_zone, list_appartenance in dict_res_appartenance.items():
    #         if list_points_array_coords[i] in list_appartenance:
    #             res[i] = int(no_zone)
    #             break
    #     # print(res[i])
    #     if res[i] == -1:
    #         res[i] = NB_ZONES

    res = -1 * np.ones(array_coords.shape[0], dtype=int)
    for no_zone in DICT_GDF_ZONES.keys():
        for pt in dict_res_appartenance[no_zone]:
            res[index_by_id[id(pt)]] = no_zone

    for i, no_zone in enumerate(res):
        if res[i] == -1:
            res[i] = NB_ZONES
    # pprint(res)
    return res


def rapport_a_la_seine_spatial_index_point(array_coords: np.ndarray) -> np.ndarray:

    list_points_array_coords = list(map(lambda x: Point(*x), list(array_coords)))

    index_poly_by_id = dict((id(po), i) for i, po in enumerate(DICT_GDF_ZONES.values()))

    polygons_tree = STRtree(DICT_GDF_ZONES.values())

    res = -1 * np.ones(array_coords.shape[0], dtype=int)
    for i, point in enumerate(list_points_array_coords):
        le_bon_poly = polygons_tree.nearest(point)
        res[i] = index_poly_by_id[id(le_bon_poly)]
        # if le_bon_poly.intersects(point):
        #     res[i] = index_poly_by_id[id(le_bon_poly)]
        # else:
        #     res[i] = NB_ZONES
    return res
    

if __name__ == "__main__":
    import time
    with open("points", 'r', encoding='utf8') as file:
        array = np.array(eval(file.read()))
    t1 = time.time()
    # pprint(rapport_a_la_seine_spatial_index(array))
    t2 = time.time()
    print(f"{t2-t1:3.3f} secondes avec index")
    # print(array)
    # print(tuple(array[0]))
    # print("\n\n\n\n")
    # print(np.array([tuple(x) for x in array])[:,0])

    array2 = np.array([tuple(x) for x in array])
    # rapport_a_la_seine(np.array([tuple(x) for x in array]))
    res = -1 * np.ones(len(array2), dtype=int)
    for i, coord in enumerate(zip(array2[:,0], array2[:,1])):
        # coord = (xy[0], xy[1])

        for no_zone, gdf in DICT_GDF_ZONES.items():
            if Point(*coord).within(gdf):
                # print(coord, no_zone)
                # return no_zone
                res[i] = no_zone
                pass

        # print(coord, "out of all zones")
        # return NB_ZONES
        if res[i] == -1:
            res[i] = NB_ZONES
    pprint(res)
    t3 = time.time()
    print(f"{t3-t2:3.3f} secondes sans index")
    pprint(rapport_a_la_seine_spatial_index_point(array))
    t4 = time.time()
    print(f"{t4-t3:3.3f} secondes avec index sur les polygones")



# $ python seine_data_utils.py 
# 30
# 0
# 1195
# 2359
# 1172
# array([3, 2, 3, ..., 4, 4, 3])
# 22.207 secondes avec index
# array([3, 2, 3, ..., 4, 4, 3])
# 20.819 secondes sans index
# array([3, 2, 3, ..., 4, 4, 3])
# 6.969 secondes avec index sur les polygones