from shapely.geometry import Point, LineString, Polygon
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from fiona.crs import from_epsg
from geopandas.tools import geocode

from bokeh.plotting import figure, save

cle_api = 'AIzaSyBke6w6E7-WK-Qwx7MCEgXYfWua2qQbqHc'

# Juste pour tout afficher
pd.set_option('max_columns', None)

fp = "Data\\DAMSELFISH_distributions.shp"
data = gpd.read_file(fp)

fp = "addresses.txt"
data2 = pd.read_csv(fp, sep=";")

def test10():
    def binaryClassifier(row, source_col, output_col, threshold):
        # If area of input geometry is lower that the threshold value
        if row[source_col] < threshold:
            # Update the output column with value 0
            row[output_col] = 0
        # If area of input geometry is higher than the threshold value update with value 1
        else:
            row[output_col] = 1
        # Return the updated row
        return row


    fp = "Data2\\Corine2012_Uusimaa.shp"
    data = gpd.read_file(fp)

    selected_cols = ['Level1', 'Level1Eng', 'Level2', 'Level2Eng', 'Level3', 'Level3Eng', 'Luokka3', 'geometry']

    data = data[selected_cols]

    lakes = data.loc[data['Level3Eng'] == 'Water bodies'].copy()
    lakes['area'] = lakes.area
    lakes['area_km2'] = lakes['area'] / 1000000
    l_mean_size = lakes['area_km2'].mean()

    lakes['small_big'] = None

    lakes = lakes.apply(binaryClassifier, source_col='area_km2', output_col='small_big', threshold=l_mean_size, axis=1)

    lakes.plot(column='small_big', linewidth=0.05, cmap="seismic")

    plt.tight_layout()
    plt.show()


def test9():
    p = figure(title="une figure")
    x_coords = [0, 1, 2, 3, 4]
    y_coords = [5, 4, 1, 2, 0]

    p.circle(x=x_coords, y=y_coords, size=10, color="red")

    outfp = "Data3\\interactive_plot.html"
    save(obj=p, filename=outfp)

def test8():
    # Filepaths
    grid_fp = "Data3\\TravelTimes_to_5975375_RailwayStation.shp"
    roads_fp = "Data3\\roads.shp"
    metro_fp = "Data3\\metro.shp"

    # Read files
    grid = gpd.read_file(grid_fp)
    roads = gpd.read_file(roads_fp)
    metro = gpd.read_file(metro_fp)

    roads.to_crs(grid.crs, inplace=True)
    metro.to_crs(grid.crs, inplace=True)

    print(grid.crs)
    print(roads.crs)
    print(metro.crs)

    # Visualize the travel times into 9 classes using "Quantiles" classification scheme
    # Add also a little bit of transparency with `alpha` parameter
    # (ranges from 0 to 1 where 0 is fully transparent and 1 has no transparency)
    my_map = grid.plot(column="car_r_t", linewidth=0.03, cmap="Reds", scheme="quantiles", k=9, alpha=0.9)

    # Add roads on top of the grid
    # (use ax parameter to define the map on top of which the second items are plotted)
    roads.plot(ax=my_map, color="grey", linewidth=1.5)

    # Add metro on top of the previous map
    metro.plot(ax=my_map, color="red", linewidth=2.5)

    # Remove the empty white-space around the axes
    plt.tight_layout()

    # Save the figure as png file with resolution of 300 dpi
    outfp = "Data3\\static_map.png"
    plt.savefig(outfp, dpi=300)

    plt.show()

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




test10()