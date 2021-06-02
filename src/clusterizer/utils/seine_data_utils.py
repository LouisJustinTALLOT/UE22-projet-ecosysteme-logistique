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

# on a obtenu toutes les coordonnees des points
# on va maintenant tracer des droites entre ces points

liste_droites_Seine = [] # droites décrivant la Seine sous forme (a, b) avec y=a*x + b
liste_droites_Marne = [] # droites décrivant la Marne sous forme (a, b) avec y=a*x + b

for no_coord in range(3, len(liste_coordonnees)-1):
    # pour la Seine : tous sauf les 3 premiers qui viennent de la Marne
    x_1, y_1 = liste_coordonnees[no_coord]
    x_2, y_2 = liste_coordonnees[no_coord + 1]

    a = (y_2 - y_1) / (x_2 - x_1)
    b = y_1 - a*x_1

    liste_droites_Seine.append((a,b))

for no_coord_1, no_coord_2 in zip([34, 0, 1], [0, 1, 2]):
    # on part d'abord du point Seine 31 + Marne 0, 
    # puis les 3 premiers points Marne 1 -> 3
    x_1, y_1 = liste_coordonnees[no_coord_1]
    x_2, y_2 = liste_coordonnees[no_coord_2]

    a = (y_2 - y_1) / (x_2 - x_1)
    b = y_1 - a*x_1

    liste_droites_Marne.append((a,b))

pprint.pprint(liste_droites_Seine)
pprint.pprint(liste_droites_Marne)
