import geopandas as gpd
"""
Ce fichier ne sert qu'à réduire la base pour qu'elle soit manipulable en temps fini
"""
def reduct():
    print("Ouverture du fichier...")
    file = gpd.read_file("input\\base-adresse-75.geojson")
    print("Fichier ouvert !")
    print("En-tête du fichier :")
    print(file.head())

    print("Sauvegarde dans un fichier réduit...")
    new_file = file.loc[:10000]
    new_file.to_file("output\\reducted.geojson", driver="GeoJSON", encoding="UTF-8")
    print("Sauvegarde effectuée, dans \"reducted.geojson\"")

    print("Test d'ouverture...")
    file = gpd.read_file("input\\reducted.geojson")
    print(file.head())

    print("Fin...")

reduct()