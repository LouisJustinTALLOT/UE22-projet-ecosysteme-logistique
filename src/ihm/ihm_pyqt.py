import sys
sys.path.append("../../")


from src.clusterizer import clusterizer
from src.ihm import web

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
                            QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QRadioButton


class Fenetre(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # Variable des données à récupérer dans la fenêtre (sous forme de liste)

        # Valeurs par défaut
        # self._donnees = [nb_cluster_min, nb_cluster_max, secteur, rayon]
        self._donnees =[0, 0, '', 0]
        self._valid = False

        # création du champ de texte
        self.champ_nb_cluster_min = QLineEdit()
        self.champ_nb_cluster_min.setText("5")
        self.champ_nb_cluster_max = QLineEdit()
        self.champ_nb_cluster_max.setText("10")
        self.champ_secteur = QLineEdit()
        self.champ_rayon = QLineEdit()
        self.champ_rayon.setText("10")
        
        # création du bouton
        self.bouton = QPushButton("Clusterize !")
        # on connecte le signal "clicked" à la méthode "appui_bouton_copie"
        self.bouton.clicked.connect(self.appui_bouton_OK)
        self.NAF_voulu = QRadioButton("Sélectionner uniquement ces secteurs")
        self.NAF_compl = QRadioButton("Sélectionner toutes les secteurs sauf ceux-ci")
        self.NAF_compl.setChecked(True)
 
        # création des étiquettes
        self.label_cluster = QLabel("Nombre de clusters")
        self.label_cluster_min = QLabel("Min :")
        self.label_cluster_max = QLabel("Max :")

        self.label_secteur = QLabel("Secteur NAF :")

        self.label_rayon = QLabel("Rayon de la sélection :")
        self.label_unite = QLabel("km")
        
        # mise en place du gestionnaire de mise en forme
        # Création des layout
        layout_princip = QVBoxLayout()
        layout_cluster = QHBoxLayout()
        layout_rayon = QHBoxLayout()

        # Rangement des layouts
        layout_princip.addWidget(self.label_cluster)

        # Layout cluster
        layout_cluster.addWidget(self.label_cluster_min)
        layout_cluster.addWidget(self.champ_nb_cluster_min)
        layout_cluster.addWidget(self.label_cluster_max)
        layout_cluster.addWidget(self.champ_nb_cluster_max)

        layout_princip.addLayout(layout_cluster)

        # Layout Secteur
        layout_princip.addWidget(self.label_secteur)
        layout_princip.addWidget(self.champ_secteur)
        layout_princip.addWidget(self.NAF_compl)
        layout_princip.addWidget(self.NAF_voulu)

        # Layout rayon
        layout_rayon.addWidget(self.label_rayon)
        layout_rayon.addWidget(self.champ_rayon)
        layout_rayon.addWidget(self.label_unite)
        layout_princip.addLayout(layout_rayon)

        # Bouton
        layout_princip.addWidget(self.bouton)
        
        # Fenetre
        self.setLayout(layout_princip)
        
        self.setWindowTitle("IHM PyQT5")
        self.resize(500, 500)

    # on définit une méthode à connecter au signal envoyé
    def appui_bouton_OK(self):

        # Récupération des données de l'interface 
        nb_cluster_min = self.champ_nb_cluster_min.text()
        nb_cluster_max = self.champ_nb_cluster_max.text()
        secteur = self.champ_secteur.text()
        rayon = self.champ_rayon.text()

        # On suppose pour l'instant que l'utilisateur n'est pas stupide
        self._donnees[0] = int(nb_cluster_min)
        self._donnees[1] = int(nb_cluster_max)
        self._donnees[2] = secteur
        self._donnees[3] = int(rayon)

        


    def lancement_clustering(self) :
        
        nb_cluster_min = self._donnees[0]
        nb_cluster_max = self._donnees[1]
        secteur_NAF = self._donnees[2]
        rayon = self._donnees[3]
        print("Nombre de cluster =", nb_cluster_min)
        print("Rayon = ", rayon)
        print("Sélection NAF : ", secteur_NAF)

        adresse = "output_ihm/clusterized_ihm.html"

        """
        Clusterization avec les données utlisateurs
        """

        if __name__ == "__main__":

            # On exécute le programme avec la base SIRENE :

            clusterizer.main_json(rayon, secteur_NAF, nb_cluster_min, adresse)

            # On ouvre le fichier dans le navigateur (actuellement chrome)
            web.open_html(adresse)
        
        

app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)
    
fen = Fenetre()
fen.show()

app.exec_()