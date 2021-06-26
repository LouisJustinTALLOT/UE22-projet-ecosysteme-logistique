"""
Première interface Homme-machine : utilisation d'un tableau `CSV` pour récupérer les informations données par l'utilisateur

Paramètres modifiables dans la fonction :code:`clusterize` : le nombre de clusters

TODO : Paramètres modifiables souhaités en plus : encadrement du nombre de clusters, taille des clusters
"""
import csv

import geopandas as gpd
import pandas as pd
import numpy as np
import folium

import sys
sys.path.append("../../")


from src.clusterizer import clusterizer
from src.ihm import web

if __name__ == "__main__":


    print("Lecture des données...")
    # Lecture du tableau csv et récupération des données
    fichier = open(r"table_choix.csv")
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

    adresse = "output_ihm/clusterized_ihm.html"

    """
    Clusterization avec les données utlisateurs
    """


    # On exécute le programme avec la base SIRENE :

    clusterizer.main_json(rayon, secteur_NAF, nb_cluster, adresse)

    # On ouvre le fichier dans le navigateur (actuellement chrome)
    web.open_html(adresse)