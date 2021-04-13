# importations à faire pour la réalisation d'une interface graphique
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

# Première étape : création d'une application Qt avec QApplication
#    afin d'avoir un fonctionnement correct avec IDLE ou Spyder
#    on vérifie s'il existe déjà une instance de QApplication
app = QApplication.instance() 
if not app: # sinon on crée une instance de QApplication
    app = QApplication(sys.argv)

# création d'une fenêtre avec QWidget dont on place la référence dans fen
fen = QWidget()

# on donne un titre à la fenêtre
fen.setWindowTitle("Premiere fenetre")

# on fixe la taille de la fenêtre
fen.resize(500,500)

# on fixe la position de la fenêtre
fen.move(300,50)

fen.label = QLabel("hello")
fen.label.show()

# la fenêtre est rendue visible
fen.show()

# exécution de l'application, l'exécution permet de gérer les événements
app.exec_()
