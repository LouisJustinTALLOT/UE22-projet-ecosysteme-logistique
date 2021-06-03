from pathlib import Path, PurePath
import re
from typing import List, Tuple

if __name__== "__main__":
    # pas besoin de ça si utilisé comme module
    import pprint
    import numpy as np
    import matplotlib.pyplot as plt

"""On va utiliser des expressions régulières pour récupérer
les coordonnées des points sur la Seine 

https://regex101.com/r/4Dnyfh/1
"""

FILE_PATH = Path(__file__).resolve()
BASE_DIR = FILE_PATH.parent.parent.parent.parent

REGEX_COORDINATES = re.compile(r"(?<=(<coordinates>)).*(?=(,0<\/coordinates>))")

def get_KML_data(kml_filename="data/trace_seine.kml"):
    
    # with open("../../../data/trace_seine.kml", "r", encoding="utf8") as file:
    with open(BASE_DIR/kml_filename, "r", encoding="utf8") as file:
        seine_KML = file.readlines()
    return seine_KML

def get_coords(seine_KML=get_KML_data()):
    liste_coordonnees = [] # coordonnées des points décrivant la Seine sous la forme (long, lat)

    for ligne in seine_KML:
        match = REGEX_COORDINATES.search(ligne)

        if match:
            str_coords = match.group(0)
            coords = tuple(map(float, str_coords.split(",")))
            liste_coordonnees.append(coords)

    if __name__ == "__main__":
        print("liste_coordonnees: ")
        pprint.pprint(liste_coordonnees)

    return liste_coordonnees

def calcul_droites(liste_coordonnees=get_coords()):

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

    if __name__ == "__main__":
        print("liste_droites_Seine :")
        pprint.pprint(liste_droites_Seine)
        print("liste_droites_Marne :")
        pprint.pprint(liste_droites_Marne)

    return liste_droites_Seine, liste_droites_Marne

class Point:
    def __init__(self, long, lat) -> None:
        self.x = long
        self.y = lat

    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"

class Segment:
    def __init__(self, point_1: Point, point_2: Point) -> None:
        self.point_1 = point_1
        self.point_2 = point_2
if __name__ == "__main__":
    liste_coordonnees = get_coords()
    liste_droites_Seine, liste_droites_Marne = calcul_droites(liste_coordonnees)

    # on trace tout ça pour vérifier
    x = np.linspace(2.2, 2.45, 100)

    for a, b in liste_droites_Seine + liste_droites_Marne:
        plt.plot(x, a*x+b, "b", linewidth=0.2)

    for x, y in liste_coordonnees:
        plt.scatter(x,y, color="black", marker=".")
    plt.axis("equal")

    plt.xlim(2.2, 2.45)
    plt.ylim(48.75, 49)
    plt.show()