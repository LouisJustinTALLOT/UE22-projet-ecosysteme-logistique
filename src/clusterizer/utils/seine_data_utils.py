import re
import pprint

import numpy as np
import matplotlib.pyplot as plt

"""On va utiliser des expressions régulières pour récupérer
les coordonnées des points sur la Seine 

https://regex101.com/r/4Dnyfh/1
"""

with open("../../../data/trace_seine.kml", "r", encoding="utf8") as file:
    seine_kml = file.readlines()
