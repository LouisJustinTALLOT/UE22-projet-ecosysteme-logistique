import os
import sys

from PyQt5.QtCore import QUrl
sys.path.append("../../")


from src.ihm import ihm_pyqt
from src.ihm import qt_web

from src.clusterizer import clusterizer


from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow
from PyQt5 import QtWebEngineWidgets

class Wind(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.IHM = ihm_pyqt.Fenetre()

        self.IHM.bouton.clicked.connect(self.appui_bouton_OK)

        self.setCentralWidget(self.IHM)
        self.setWindowTitle("IHM PyQT5")
        self.resize(500, 500)


    def appui_bouton_OK(self):

        # Récupération des données de l'interface 
        nb_cluster_min = self.IHM.champ_nb_cluster_min.text()
        nb_cluster_max = self.IHM.champ_nb_cluster_max.text()
        secteur = self.IHM.champ_secteur.text()
        rayon = self.IHM.champ_rayon.text()

        # On suppose pour l'instant que l'utilisateur n'est pas stupide
        self.IHM._donnees[0] = int(nb_cluster_min)
        self.IHM._donnees[1] = int(nb_cluster_max)
        self.IHM._donnees[3] = int(rayon)

        # La liste des secteurs NAFs
        list_secteur = ['']

        if secteur != '' :
            if self.IHM.NAF_voulu.isChecked() :
                list_secteur = secteur.split()

            else :
                list_secteur = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U']
                to_remove = secteur.split()

                for lettre in to_remove :
                    list_secteur.remove(lettre)

        self.IHM._donnees[2] = list_secteur

        self.lancement_clustering()
    


        


    def lancement_clustering(self) :
        
        nb_cluster_min = self.IHM._donnees[0]
        nb_cluster_max = self.IHM._donnees[1]
        rayon = self.IHM._donnees[3]
        secteur_NAF = self.IHM._donnees[2]

        for nb_clust in range(nb_cluster_min, nb_cluster_max + 1) :
            print("Nombre de cluster =", nb_clust)
            print("Rayon = ", rayon)
            print("Sélection NAF : ", secteur_NAF)

            adresse = "output_ihm/" +str(nb_clust) +"_clusterized_ihm.html"

            """
            Clusterization avec les données utlisateurs
            """

            if __name__ == "__main__":

                # On exécute le programme avec la base SIRENE :

                clusterizer.main_json(rayon, secteur_NAF, nb_clust, adresse)

                # On ouvre le fichier dans PyQt


                view = QtWebEngineWidgets.QWebEngineView()

                view.setHtml(open(adresse, 'r').read())

                
                self.takeCentralWidget()
                self.setCentralWidget(view)
                self.setWindowTitle("Carte avec "+str(nb_clust)+" clusters")
                self.move(0,0)
                self.showMaximized()

                


app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)
    
fen = Wind()
fen.show()

app.exec_()