from pathlib import Path
from pprint import pprint
from typing import Dict
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon
from shapely.strtree import STRtree
from multiprocessing import Pool

FILE_PATH = Path(__file__).resolve()
BASE_DIR = FILE_PATH.parent.parent.parent.parent

DICT_ZONES_IDF = {
    0 : "IDF_zone_est",
    1 : "IDF_zone_nord_Paris",
    2 : "IDF_zone_Paris_ouest",
    3 : "IDF_zone_sud",
}

DIR_SHP_FILES = BASE_DIR/"data/IDF_5_zones/"

DICT_GDF_ZONES: Dict[int, Polygon] = {}

for i in DICT_ZONES_IDF.keys():
    DICT_GDF_ZONES[i] = gpd.read_file(DIR_SHP_FILES/( DICT_ZONES_IDF[i] + ".shp"))['geometry'][0]

NB_ZONES = len(DICT_ZONES_IDF)



def rapport_a_la_seine_spatial_index_point(array_coords: np.ndarray) -> np.ndarray:
    """Trouve les zones où se situent les points de l':code:`array` fournie.
    Utilise un *R-Tree* pour ce faire pour accélérer le calcul.

    :param array_coords: Array (nb_points, 2) contenant les coordonnées des points
    :type array_coords: np.ndarray
    :return: Une array "masque" qui a chaque point associe son numéro de zone
    :rtype: np.ndarray
    """

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
    

def rapport_a_la_seine_multiprocessing(array_coords: np.ndarray, nb_split: int = 5) -> np.ndarray:
    
    list_chunks = np.array_split(array_coords, nb_split)

    with Pool(nb_split) as p:
        res = p.map(rapport_a_la_seine_spatial_index_point, list_chunks)

    return np.concatenate(res)


if __name__ == "__main__":
    import time
    with open("points", 'r', encoding='utf8') as file:
        array = np.array(eval(file.read()))

    t2 = time.time()
    array2 = np.array([tuple(x) for x in array])
    res = -1 * np.ones(len(array2), dtype=int)
    for i, coord in enumerate(zip(array2[:,0], array2[:,1])):
        for no_zone, gdf in DICT_GDF_ZONES.items():
            if Point(*coord).within(gdf):
                res[i] = no_zone
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