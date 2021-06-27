from pprint import pprint
import numpy as np
import shapely
import fiona
import shapely.geometry as geometry
from shapely.geometry import Polygon
from shapely.geometry.multipolygon import MultiPolygon
from shapely.ops import cascaded_union, polygonize, unary_union
from scipy.spatial import Delaunay
from shapely.geometry import mapping
import math

def alpha_shape(points, alpha=0.01, buffer=0):
    """
    Basé sur https://gis.stackexchange.com/a/289972/187654
    """

    # if len(points) < 20:
    #     print("AAAAAAHHH UNE ENVELOPPE CONVEXE")
    #     return geometry.MultiPoint(points).convex_hull, None

    def add_edge(edges, edge_points, coords, i, j):
        """
        Add a line between the i-th and j-th points,
        if not in the list already
        """
        if (i, j) in edges or (j, i) in edges:
            # already added
            return
        edges.add( (i, j) )
        edge_points.append(coords[ [i, j] ])

    coords = np.array(points)

    try:
        tri = Delaunay(coords)
    except Exception as e :
        print(e)
        return None, None

    edges = set()
    edge_points = []
    # loop over triangles:
    # ia, ib, ic = indices of corner points of the
    # triangle
    for ia, ib, ic in tri.vertices:
        pa = coords[ia]
        pb = coords[ib]
        pc = coords[ic]
        # Lengths of sides of triangle
        a = math.sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)
        b = math.sqrt((pb[0]-pc[0])**2 + (pb[1]-pc[1])**2)
        c = math.sqrt((pc[0]-pa[0])**2 + (pc[1]-pa[1])**2)
        # Semiperimeter of triangle
        s = (a + b + c)/2.0
        try:
            # Area of triangle by Heron's formula
            area = math.sqrt(s*(s-a)*(s-b)*(s-c))
        except ValueError:
            area = 0
        # print(ia, ib, ic, area)
        circum_r = a*b*c/(4.0*area+10**-5)
        # print(circum_r)
        # Here's the radius filter.
        if circum_r < alpha:
            add_edge(edges, edge_points, coords, ia, ib)
            add_edge(edges, edge_points, coords, ib, ic)
            add_edge(edges, edge_points, coords, ic, ia)
    try:
        m = geometry.MultiLineString(edge_points)
        triangles = list(polygonize(m))
        concave_hull = cascaded_union(triangles)
        concave_hull = concave_hull.buffer(buffer)

    except Exception as e:
        print(e)
        print("ici")
        return None, None

    # Lets check, if the resulting polygon contains at least 90% of the points.
    # If not, we return the convex hull.

    # points_total = len(points)
    # points_inside = 0

    # for p in shapely.geometry.MultiPoint(points):
    #     points_inside += concave_hull.contains(p)

    
    if not concave_hull.is_empty:
        # pprint(concave_hull)
        # if type(concave_hull) == MultiPolygon:
        #     pprint(list(concave_hull))
        #     pprint(unary_union(concave_hull))
        #     return polygonize(unary_union(concave_hull)), edge_points
        return concave_hull, edge_points
    # elif points_inside/points_total<0.9:
    else:
        raise Exception("Convex")
        return geometry.MultiPoint(points).convex_hull, None
    # else:
    #     return None, None





# def produce_alpha_polygons(features, alpha, buffer=0):
#     alpha_polygons = []

#     for i, f in enumerate(features):
#         #print("{}/{}".format(i+1, len(features)))
#         #select certain features
#         current_points = points[points[:,-1]==f][:,:2]
#         alpha_poly, _ = alpha_shape(current_points, alpha, buffer)
#         alpha_polygons += [alpha_poly]

#     return alpha_polygons