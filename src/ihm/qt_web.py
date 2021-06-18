import sys
from PyQt5.QtCore import QUrl
sys.path.append("../../")

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor

# Pour ouvrir la carte dans PyQt (à rendre utilisable)


class Interceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        info.setHttpHeader(b"Accept-Language", b"en-US,en;q=0.9,es;q=0.8,de;q=0.7")


app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)
    
fen = QMainWindow()
fen.setWindowTitle("Ouverture HTML ?")

view = QtWebEngineWidgets.QWebEngineView()
interceptor = Interceptor()
view.page().profile().setUrlRequestInterceptor(interceptor)

view.setHtml(open("output_ihm/clusterized_ihm.html", 'r').read())


fen.setCentralWidget(view)

fen.show()

app.exec_()
