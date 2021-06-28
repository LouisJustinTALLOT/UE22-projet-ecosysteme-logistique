import sys
sys.path.append("../../")

from PyQt5.QtWidgets import QCheckBox, QWidget, QPushButton, QVBoxLayout, QLabel, \
                            QLineEdit, QHBoxLayout, QRadioButton


class InputFenetre(QWidget):
    """
    Le widget qui permet à l'utilisateur de rentrer les paramètres de clustering
    """
    def __init__(self):
        QWidget.__init__(self)
        # Variable des données à récupérer dans la fenêtre (sous forme de liste)

        # Valeurs par défaut
        # self._donnees = [nb_cluster_min, nb_cluster_max, secteur, rayon]
        self._donnees =[0, 0, '', 0]
        self._valid = False

        # création du champ de texte
        self.champ_nb_cluster_min = QLineEdit()
        self.champ_nb_cluster_min.setText("12")
        self.champ_nb_cluster_max = QLineEdit()
        self.champ_nb_cluster_max.setText("12")
        self.champ_secteur = QLineEdit()
        self.champ_secteur.setText("G I Q")
        self.champ_rayon = QLineEdit()
        self.champ_rayon.setText("10")
        
        # création du bouton
        self.bouton = QPushButton("Clusterize !")
        self.seine_div = QCheckBox("Séparer par la Seine")
        self.NAF_voulu = QRadioButton("Sélectionner uniquement ces secteurs")
        self.NAF_compl = QRadioButton("Sélectionner tous les secteurs sauf ceux-ci")
        self.NAF_voulu.setChecked(True)
 
        # création des étiquettes
        self.label_cluster = QLabel("Nombre de clusters")
        self.label_cluster_min = QLabel("Min :")
        self.label_cluster_max = QLabel("Max :")

        self.label_secteur = QLabel("Secteur NAF : (lettre entre A et U)\nSéparer les secteurs par un espace.")

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
        layout_princip.addWidget(self.NAF_voulu)
        layout_princip.addWidget(self.NAF_compl)

        # Layout rayon
        layout_rayon.addWidget(self.label_rayon)
        layout_rayon.addWidget(self.champ_rayon)
        layout_rayon.addWidget(self.label_unite)
        layout_princip.addLayout(layout_rayon)

        # Séparer par la Seine
        layout_princip.addWidget(self.seine_div)

        # Bouton
        layout_princip.addWidget(self.bouton)
        
        # Fenetre
        self.setLayout(layout_princip)
