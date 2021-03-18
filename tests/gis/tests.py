from shapely.geometry import Point, LineString, Polygon
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from fiona.crs import from_epsg
from geopandas.tools import geocode

cle_api = 'AIzaSyBke6w6E7-WK-Qwx7MCEgXYfWua2qQbqHc'

# Juste pour tout afficher
pd.set_option('max_columns', None)

fp = "Data\\DAMSELFISH_distributions.shp"
data = gpd.read_file(fp)

fp = "addresses.txt"
data2 = pd.read_csv(fp, sep=";")

def test7():
    fp = "Data2\\Helsinki_borders.shp"
    hel = gpd.read_file(fp)
    fp = "Data2\\TravelTimes_to_5975375_RailwayStation.shp"
    grid = gpd.read_file(fp)

    basemap = hel.plot(linewidth=0.02, alpha=0.5)
    grid.plot(ax=basemap, linewidth=0.02, color="r", alpha=0.5)

    plt.tight_layout()
    plt.show()

    result = gpd.overlay(grid, hel, how='intersection')
    result.plot(color='y', alpha=0.2)
    plt.show()

    result_aggregated = result.dissolve(by="car_r_t")
    base = result_aggregated.loc[0:10].plot(color="b")
    print("len", result_aggregated.shape[0])
    result_aggregated.loc[10:20].plot(ax=base, color="r")
    result_aggregated.loc[20:30].plot(ax=base, color="y")
    result_aggregated.loc[30:40].plot(ax=base, color="m")
    result_aggregated.loc[40:50].plot(ax=base, color="k")
    plt.show(linewidth=0.2)


def test6():
    # Pour que ça marche faut payer xd
    geo = geocode(data2['address'], api_key=cle_api)
    print(geo.head())

def test5():
    print(data.columns)
    grouped = data.groupby('BINOMIAL')
    print(grouped)

    for key, values in grouped:
        print("\n\n===========")
        print("Key", key)
        print(values)
        print(values.columns)

def test4():
    newdata = gpd.GeoDataFrame()
    newdata['geometry'] = None
    newdata['Location'] = None

    coordinates = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]
    polygon = Polygon(coordinates)

    newdata.loc[0] = [polygon, "Senate"]

    print(newdata)

    newdata.crs = from_epsg(4326)
    print(newdata.crs)

    out = "Data\\Senate.shp"
    newdata.to_file(out)


def test3():
    selection = data[0:5]
    for index, row in selection.iterrows():
        # index represents the number of the row
        # row is the entire row
        # to get an element of the row (ie a row intersected with a column), do row['geometry']
        area = row['geometry'].area
        print("At row n", index, ", we have area=", area)

    # Creation of an empty column
    data['area'] = None

    for index, row in selection.iterrows():
        data.loc[index, 'area'] = row['geometry'].area

    print("Mean : ", data['area'].mean())

def test2():
    # Displaying
    print(data.head())
    data.plot()
    plt.show()
    print(data.crs)

    # Exporting
    out = "Data\\DAMSELFISH_distributions_SELECTION.shp"
    selection = data[0:50]
    selection.to_file(out)

def test1():
    # Les trois objets principaux sont Point, LineString et Polygon

    point1 = Point(2, 5)
    point2 = Point(1, 6)
    point3 = Point(3, 4)

    line = LineString([point1, point2, point3])

    # Toutes les abscisses
    print(line.xy[0])

    # Centre de masse
    print(line.centroid)

    poly2 = Polygon([[p.x, p.y] for p in [point1, point2, point3]])

    print(poly2.centroid)




test7()