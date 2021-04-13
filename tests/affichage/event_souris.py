import sys
from PyQt5.QtWidgets import QApplication, QWidget

# Pour ajouter des fonctionnalités en plus de ce qu'il y a dans QWidget (héritage)
class Fenetre(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Ma fenetre")

    # Gestion des événements de la souris, exrension d'une fonction déjà existante
    def mousePressEvent(self, event):
        print("appui souris")

app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)
    
fen = Fenetre()
fen.show()

app.exec_()
