"""
Premier ihm :utilisation d'un tableau csv pour récupérer les infos données par l'utilisateur
Paramètres modifiables dans la fonction de clusterize : le nombre de cluster
Paramètres modifiables souhaités en plus : encadrement du nombre de cluster, taille des cluster 
"""
import csv

# Lecture du tableau csv et récupération des données
fichier = open(r"src/ihm/table_choix.csv")
myreader = csv.reader(fichier, delimiter =';')

# Pn récupére les lignes du fichier sous forme de liste de ligne
lignes = list(myreader)

fichier.close()

# Les données sont sur la troisième ligne du fichier
donnees = lignes[2]

