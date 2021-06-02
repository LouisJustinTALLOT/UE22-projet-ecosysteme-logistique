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

regex_coordinates = re.compile(r"(?<=(<coordinates>)).*(?=(,0<\/coordinates>))")

liste_coordonnees = [] # coordonnés des points décrivant la Seine sous la forme (long, lat)

for ligne in seine_kml:
    match = regex_coordinates.search(ligne)
    # print(res) if res is not None else "pass"
    if match:
        str_coords = match.group(0)
        coords = tuple(map(float, str_coords.split(",")))
        liste_coordonnees.append(coords)

pprint.pprint(liste_coordonnees)
