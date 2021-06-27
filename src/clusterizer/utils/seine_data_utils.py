from pathlib import Path
from typing import Dict
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon

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