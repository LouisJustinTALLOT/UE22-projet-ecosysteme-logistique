import webbrowser
import os



def open_html(adresse) :
    """
    Affichage du html depuis python. Il faut être dans le répertoire ihm pour le lancer.

    :param adresse: l'adresse du fichier à ouvrir

    """
    # récupérer le chemin du répertoire courant
    path = os.getcwd()


    adresse_totale = "file://"+path+"\\" + adresse
    adresse_navig = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    webbrowser.get(adresse_navig).open(adresse_totale)
