import sys
sys.path.append("../../")


from src.ihm import clusterize_ihm
from src.ihm import web

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
                            QVBoxLayout, QLabel, QLineEdit

class Fenetre(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # Variable des données à récupérer dans la fenêtre (sous forme de liste)

        # Valeurs par défaut
        # self._donnees = [nb_cluster, secteur, rayon]
        self._donnees =[150, '', 8]
        self._valid = False

        # création du champ de texte
        self.champ_nb_cluster = QLineEdit()
        self.champ_secteur = QLineEdit()
        self.champ_rayon = QLineEdit()
        
        # création du bouton
        self.bouton = QPushButton("Clusterize !")
        # on connecte le signal "clicked" à la méthode "appui_bouton_copie"
        self.bouton.clicked.connect(self.appui_bouton_OK)
 
        # création de l'étiquette
        self.label_cluster = QLabel("Nombre de cluster :")
        self.label2_cluster = QLabel()

        self.label_secteur = QLabel("Secteur NAF :")
        self.label2_secteur = QLabel()

        self.label_rayon = QLabel("Rayon de la sélection :")
        self.label2_rayon = QLabel()
        
        # mise en place du gestionnaire de mise en forme
        layout = QVBoxLayout()
        layout.addWidget(self.label_cluster)
        layout.addWidget(self.champ_nb_cluster)
        layout.addWidget(self.label2_cluster)

        layout.addWidget(self.label_secteur)
        layout.addWidget(self.champ_secteur)
        layout.addWidget(self.label2_secteur)

        layout.addWidget(self.label_rayon)
        layout.addWidget(self.champ_rayon)
        layout.addWidget(self.label2_rayon)

        layout.addWidget(self.bouton)
        
        self.setLayout(layout)
        
        self.setWindowTitle("IHM PyQT5")
        self.resize(500, 500)

    # on définit une méthode à connecter au signal envoyé
    def appui_bouton_OK(self):

        # Récupération des données de l'interface 
        nb_cluster = self.champ_nb_cluster.text()
        secteur = self.champ_secteur.text()
        rayon = self.champ_rayon.text()

        # Vérification de la validité des valeurs
        verif_cluster = [str(k) for k in range(0, 150)]
        verif_secteur = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','']
        verif_rayon = [str(k) for k in range(1,20)]

        # Pour le nombre de cluster
        if nb_cluster not in verif_cluster :
            self.label2_cluster.setText("Valeur incorrecte : valeur par défaut")
            self._valid = True
        else :
            self._donnees[0] = int(nb_cluster)
            self.label2_cluster.setText("Valeur prise en compte")
            self._valid = True

        # Pour le secteur
        if secteur not in verif_secteur :
            self.label2_secteur.setText("Valeur incorrecte : valeur par défaut")
            self._valid = True
        else :
            self._donnees[1] = secteur
            self.label2_secteur.setText("Valeur prise en compte")
            self._valid = True

        # Pour le rayon
        if rayon not in verif_rayon :
            self.label2_rayon.setText("Valeur incorrecte : valeur par défaut")
            self._valid = True
        else :
            self._donnees[2] = int(rayon)
            self.label2_rayon.setText("Valeur prise en compte")
            self._valid = True

        if self._valid :
            # Toutes les données entrées sont valides
            return 1


    def lancement_clustering(self) :
        
        nb_cluster = self._donnees[0]
        secteur_NAF = self._donnees[1]
        rayon = self._donnees[2]
        print("Nombre de cluster =", nb_cluster)
        print("Rayon = ", rayon)
        print("Sélection NAF : ", secteur_NAF)

        adresse = "output_ihm/clusterized_ihm.html"

        """
        Clusterization avec les données utlisateurs
        """

        if __name__ == "__main__":

            # On exécute le programme avec la base SIRENE :

            clusterize_ihm.main_json(rayon, secteur_NAF, nb_cluster, adresse)

            # On ouvre le fichier dans le navigateur (actuellement chrome)
            web.open_html(adresse)
        
        

app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)
    
fen = Fenetre()
fen.show()

app.exec_()