import sys
sys.path.append("../../")

from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication


from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor

# Pour ouvrir la carte dans PyQt (à rendre utilisable)


class Interceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        info.setHttpHeader(b"Accept-Language", b"en-US,en;q=0.9,es;q=0.8,de;q=0.7")


if __name__ == "__main__":
    app = QApplication.instance() 
    if not app:
        app = QApplication(sys.argv)

    view = QtWebEngineWidgets.QWebEngineView()
    view.page().profile().clearHttpCache()
    interceptor = Interceptor()
    view.page().profile().setUrlRequestInterceptor(interceptor)

    view.setHtml(open("output_ihm/10_clusterized_ihm.html", 'r').read())

    view.show()

    app.exec_()