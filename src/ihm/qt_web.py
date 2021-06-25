import sys
sys.path.append("../../")


from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor

# Pour ouvrir la carte dans PyQt (à rendre utilisable)


class Interceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        info.setHttpHeader(b"Accept-Language", b"en-US,en;q=0.9,es;q=0.8,de;q=0.7")


