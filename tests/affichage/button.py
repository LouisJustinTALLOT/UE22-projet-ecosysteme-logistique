from PyQt5.QtWidgets import *

app = QApplication([])

# Création de la fenêtre
window = QWidget()

# Création d'une boîte
layout = QVBoxLayout()

layout.addWidget(QLabel("Nombre de cluster :"))

# Ajout des deux boutons dans la boite
# Les boutins :
but1 = QPushButton('5')
but2 = QPushButton('10')
but3 = QPushButton('15')
but4 = QPushButton('20')
but5 = QPushButton('25')

layout.addWidget(but1)
layout.addWidget(but2)
layout.addWidget(but3)
layout.addWidget(but4)
layout.addWidget(but5)

# Ajout de la boite dans la fenetre
window.setLayout(layout)

# Titre et taille de la fenetre
window.setWindowTitle("Des boutons")
window.resize(500, 500)

# Interraction boutons
def on_button_clicked():
    alert = QMessageBox()
    alert.setText('You clicked the button!')
    alert.exec_()

but1.clicked.connect(on_button_clicked)


window.show()
app.exec_()
