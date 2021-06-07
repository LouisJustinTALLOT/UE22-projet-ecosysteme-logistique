import webbrowser
import os


"""
Affichage du html depuis python
il faut être dans le répertoire ihm pour le lancer
"""
def open_html(adresse) :
    # récupérer le chemin du répertoire courant
    path = os.getcwd()


    adresse_totale = "file://"+path+"\\" + adresse
    adresse_navig = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    webbrowser.get(adresse_navig).open(adresse_totale)
