"""
Premier ihm :utilisation d'un tableau csv pour récupérer les infos données par l'utilisateur
Paramètres modifiables dans la fonction de clusterize : le nombre de cluster
Paramètres modifiables souhaités en plus : encadrement du nombre de cluster, taille des cluster 
"""
import csv

import geopandas as gpd
import pandas as pd
import numpy as np
import folium

import sys
sys.path.append("../../")

from sklearn.cluster import KMeans, MiniBatchKMeans

from shapely.geometry import Polygon

from src.clusterizer import Clusterizer
from src.clusterizer.utils import clusterizer_utils
from src.clusterizer.utils import NAF_utils
from src.clusterizer.utils import seine_data_utils


print("Lecture des données...")
# Lecture du tableau csv et récupération des données
fichier = open(r"src/ihm/table_choix.csv")
myreader = csv.reader(fichier, delimiter =';')

# Pn récupére les lignes du fichier sous forme de liste de ligne
lignes = list(myreader)

fichier.close()

# Les données sont sur la troisième ligne du fichier
donnees = lignes[2]
# Valeurs par défaut
nb_cluster = 150
rayon = 8

if donnees[1] != '' :
    nb_cluster = int(donnees[1])

if donnees[3] != '' :
    rayon = int(donnees[3])

secteur_NAF = donnees[2]
print("Nombre de cluster =", nb_cluster)
print("Rayon = ", rayon)
print("Sélection NAF : ", secteur_NAF)
"""
Clusterization avec les données utlisateurs
"""

print("Ouverture de la DataFrame...")
df = Clusterizer.nettoyer(pd.read_json("../../data/base_sirene_shortened.json"))

if secteur_NAF != '' :
    df = NAF_utils.filter_by_naf(df, NAF_utils.get_NAFs_by_section(secteur_NAF), "apet700")

print("On ne garde que les données du centre...")
df = clusterizer_utils.filter_nearby_paris(df, radius=rayon, dict=True)

print("On sépare par la Seine")
# on va avoir au moins 4 zones:
# rive Gauche,
# rive Droite,
# Maisons-Alfort,
# Courbevoie-Asnières

nb_zones = 2
liste_df = []
for no_zone in range(nb_zones):
    liste_df.append(
        df[no_zone == Clusterizer.rapport_a_la_seine(np.array(df.copy()["geometry"].apply(lambda x: x['coordinates'])))].reset_index(drop=True)
    )

print("Clusterisation...")

liste_df_clusters = []
nb_clusters_par_zone = [nb_cluster//2, nb_cluster//2]

for no_zone in range(nb_zones):
    liste_df_clusters.append(
        Clusterizer.clusterize(liste_df[no_zone], nb_clusters_par_zone[no_zone], dict=True, weight=True)
    )

print("Sauvegarde sur la carte...")

map = Clusterizer.save_to_map(liste_df_clusters[0][1])

for no_zone in range(1, nb_zones):
    map = Clusterizer.save_to_map(liste_df_clusters[no_zone][1], map=map)

map.save("output_ihm/clusterized_ihm.html")

print("Terminé !")
