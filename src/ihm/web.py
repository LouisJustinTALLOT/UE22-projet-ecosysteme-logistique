import webbrowser
import os

# récupérer le chemin du répertoire courant
path = os.getcwd()


"""
Affichage du html depuis python
il faut être dans le répertoire ihm pour le lancer
"""
adresse = "file://"+path+"\output_ihm\clusterized_ihm.html"
adresse_navig = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
webbrowser.get(adresse_navig).open(adresse)
