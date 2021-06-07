import webbrowser

"""
Affichage du html depuis python, pour mon ordi
(changer l'adresse si vous voulez que ça fonctionne pour vous)
Je vais essayer de régler ce léger problème
"""

adresse = "file://C:/Users/verne/Documents/Cours/Mines/S2/Informatique/Projet/UE22-projet-ecosysteme-logistique/src/ihm/output_ihm/clusterized_ihm.html"
adresse_navig = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
webbrowser.get(adresse_navig).open(adresse)
