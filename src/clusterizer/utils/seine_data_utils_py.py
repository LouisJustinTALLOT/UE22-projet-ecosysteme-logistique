from pathlib import Path
import re
from typing import List, Tuple
import matplotlib.pyplot as plt
# from numba import jit
# from numba.experimental import jitclass
# import numba as nb

if __name__== "__main__":
    # pas besoin de ça si utilisé comme module
    import pprint
    import numpy as np

"""On va utiliser des expressions régulières pour récupérer
les coordonnées des points sur la Seine 

https://regex101.com/r/4Dnyfh/1
"""

FILE_PATH = Path(__file__).resolve()
BASE_DIR = FILE_PATH.parent.parent.parent.parent

REGEX_COORDINATES = re.compile(r"(?<=(<coordinates>)).*(?=(,0<\/coordinates>))")

def get_KML_data(kml_filename="data/trace_seine.kml") -> List[str]:
    
    # with open("../../../data/trace_seine.kml", "r", encoding="utf8") as file:
    with open(BASE_DIR/kml_filename, "r", encoding="utf8") as file:
        seine_KML = file.readlines()
    return seine_KML

def get_coords(seine_KML=get_KML_data()) -> List[Tuple[float]]:
    liste_coordonnees: List[Tuple[float]] = [] # coordonnées des points décrivant la Seine sous la forme (long, lat)

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

def calcul_droites(liste_coordonnees=get_coords()) -> Tuple[List[Tuple[float]]]:

    # on a obtenu toutes les coordonnees des points
    # on va maintenant tracer des droites entre ces points

    liste_droites_Seine: List[Tuple[float]] = [] # droites décrivant la Seine sous forme (a, b) avec y=a*x + b
    liste_droites_Marne: List[Tuple[float]] = [] # droites décrivant la Marne sous forme (a, b) avec y=a*x + b

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

# point_spec = [
#     ('x', nb.float64),
#     ('y', nb.float64)
# ]

# @jitclass(point_spec)
class Point:
    def __init__(self, long: float, lat: float) -> None:
        self.x = long
        self.y = lat

    def __repr__(self) -> str:
        return f"Point({self.x:2.5f}, {self.y:2.5f})"

    def plot(self, couleur="red"):
        plt.scatter(self.x, self.y, marker=".", color=couleur)

class Segment:
    def __init__(self, point_1: Point, point_2: Point) -> None:
        if point_1.x <= point_2.x:
            self.point_gauche = point_1
            self.point_droit = point_2
        else:
            self.point_gauche = point_2
            self.point_droit = point_1

        self.a, self.b = self.eq_droite()

    def eq_droite(self) -> Tuple[float]:
        """Trouve l'équation de la droite porteuse du segment
        Renvoie (a, b) avec y = a * x + b
        """
        x_1, y_1 = self.point_gauche.x, self.point_gauche.y
        x_2, y_2 = self.point_droit.x, self.point_droit.y

        a = (y_2 - y_1) / (x_2 - x_1)
        b = y_1 - a*x_1
        
        return a, b

    class DansLeSegmentNotError(Exception):
        def __init__(self, value: int) -> None:
            self.res = value

    def en_dessous(self, point: Point) -> int:
        """Détermine si le segment est en-dessous du point donné
           i.e si le point test au-dessus du segment
        """
        mini_x = min(self.point_gauche.x, self.point_droit.x)
        maxi_x = max(self.point_gauche.x, self.point_droit.x)

        if point.x < mini_x or maxi_x < point.x:
            # le point est en-dehors des bornes du segment
            return 0
            # raise self.HorsDuSegmentError

        else:
            if point.y > self.a * point.x + self.b: # le point est au-dessus
                # return 1
                raise Segment.DansLeSegmentNotError(1)
            else: 
                # return 0
                raise Segment.DansLeSegmentNotError(0)

    def __repr__(self) -> str:
        return f"Segment entre {self.point_gauche} et {self.point_droit}"

    def plot(self, couleur="darkblue"):
        plt.plot([self.point_gauche.x, self.point_droit.x],[self.point_gauche.y, self.point_droit.y], ".-", color=couleur)

def _not_in_frontiere():
    pass
def _dans_la_frontiere():
    pass

class Frontiere:
    def __init__(self, liste_segments: List[Segment]) -> None:
        self.liste_segments = liste_segments

    class HorsDeLaFrontiereError(Exception):
        pass
    class DansLaFrontiereNotError(Exception):
        def __init__(self, value: int) -> None:
            self.res = value

    def en_dessous(self, point: Point) -> bool:
        """Détermine si la frontière est en-dessous du point donné
           i.e si le point test au-dessus de la frontière
        """

        for segment in self.liste_segments:
            try:
                segment.en_dessous(point)
            except Segment.DansLeSegmentNotError as e:
                return e.res

                # _dans_la_frontiere()
                # raise self.DansLaFrontiereNotError(e.res)
        # _not_in_frontiere()
        raise self.HorsDeLaFrontiereError
        # return 0

    def plot(self, couleur="red"):
        for seg in self.liste_segments:
            seg.plot(couleur)

    def __repr__(self):
        return f"Frontière de {self.liste_segments[0]} à {self.liste_segments[-1]}" 

def get_frontieres_utiles():
    # on récupère les coordonnées
    liste_coordonnees = get_coords()
    # on crée les objects points associés
    liste_points = list(map(lambda p:Point(*p), liste_coordonnees))
    # on va ensuite créer les bons segments
    # tous ceux de la Seine puis ceux de la Marne
    liste_segments_Seine: List[Segment] = [] # droites décrivant la Seine sous forme (a, b) avec y=a*x + b
    liste_segments_Marne: List[Segment] = [] # droites décrivant la Marne sous forme (a, b) avec y=a*x + b

    for no_coord in range(3, len(liste_coordonnees)-1):
        # pour la Seine : tous sauf les 3 premiers qui viennent de la Marne
        liste_segments_Seine.append(Segment(liste_points[no_coord], liste_points[no_coord + 1]))
    # puis ceux de la Marne
    for no_coord_1, no_coord_2 in zip([34, 0, 1], [0, 1, 2]):
        # on part d'abord du point Seine 31 + Marne 0, 
        # puis les 3 premiers points Marne 1 -> 3
        liste_segments_Marne.append(Segment(liste_points[no_coord_1], liste_points[no_coord_2]))

    liste_frontieres = [
        Frontiere(liste_segments_Seine[:5]),
        Frontiere(liste_segments_Seine[5:15]),
        Frontiere(liste_segments_Seine[15:16]),
        Frontiere(liste_segments_Seine[16:17]),
        Frontiere(liste_segments_Seine[17:31]),
        Frontiere(liste_segments_Seine[31:32]),
        Frontiere(liste_segments_Seine[32:33]),
        Frontiere(liste_segments_Seine[33:34]),
        Frontiere(liste_segments_Marne)
    ]

    return liste_frontieres

if __name__ == "__main__":
    # on récupère les coordonnées
    liste_coordonnees = get_coords()
    # on crée les objects points associés
    liste_points = list(map(lambda p:Point(*p), liste_coordonnees))
    pprint.pprint(liste_points)
    # on va ensuite créer les bons segments
    # tous ceux de la Seine puis ceux de la Marne
    liste_segments_Seine: List[Segment] = [] # droites décrivant la Seine sous forme (a, b) avec y=a*x + b
    liste_segments_Marne: List[Segment] = [] # droites décrivant la Marne sous forme (a, b) avec y=a*x + b

    for no_coord in range(3, len(liste_coordonnees)-1):
        # pour la Seine : tous sauf les 3 premiers qui viennent de la Marne
        liste_segments_Seine.append(Segment(liste_points[no_coord], liste_points[no_coord + 1]))
    # puis ceux de la Marne
    for no_coord_1, no_coord_2 in zip([34, 0, 1], [0, 1, 2]):
        # on part d'abord du point Seine 31 + Marne 0, 
        # puis les 3 premiers points Marne 1 -> 3
        liste_segments_Marne.append(Segment(liste_points[no_coord_1], liste_points[no_coord_2]))

    # pprint.pprint(liste_segments_Seine)
    # pprint.pprint(liste_segments_Marne)

    # on va maintenant faire les frontières
    # on va faire en sorte que chaque frontière soit dans le bon sens 
    for seg in liste_segments_Marne + liste_segments_Seine:
        seg.plot()
    # plt.axis("equal")

    # plt.xlim(2.2, 2.45)
    plt.ylim(48.76, 48.97)
    plt.gca().set_aspect('equal')
    plt.tight_layout()

    # plt.show()

    # on va maintenant faire des frontières
    frontiere_nord = Frontiere(liste_segments_Seine[:5])
    frontiere_nord.plot()
    frontiere_ouest = Frontiere(liste_segments_Seine[5:15])
    frontiere_ouest.plot("green")
    frontiere_Marne = Frontiere(liste_segments_Marne)
    frontiere_Marne.plot("violet")
    Frontiere(liste_segments_Seine[15:16]).plot("red")
    Frontiere(liste_segments_Seine[16:17]).plot("darkred")
    Frontiere(liste_segments_Seine[17:31]).plot("red")
    Frontiere(liste_segments_Seine[31:32]).plot("orange")
    Frontiere(liste_segments_Seine[32:33]).plot("orange")
    Frontiere(liste_segments_Seine[33:34]).plot("orange")

    plt.ylim(48.76, 48.97)
    plt.gca().set_aspect('equal')
    plt.tight_layout()

    plt.show()


if __name__ == "piche":
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