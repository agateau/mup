import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class WebPage(QWebPage):
    def javaScriptConsoleMessage(self, msg, lineNumber, sourceID):
        print "JsConsole(%s:%d): %s" % (sourceID, lineNumber, msg)

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.dataDir = os.path.dirname(__file__)

        self._setupView()

        layout = QHBoxLayout(self)
        layout.setMargin(0)
        layout.addWidget(self._view)

        self._text = QString()

        cut = QShortcut(Qt.Key_F5, self)
        cut.activated.connect(self._reload)

    def _setupView(self):
        self._view = QWebView(self)
        page = WebPage()
        page.setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        page.linkClicked.connect(self._openUrl)
        self._view.setPage(page)
        page.mainFrame().addToJavaScriptWindowObject("qtWindow", self)
        url = QUrl("file://" + self.dataDir + "/view.html")
        self._view.setUrl(url)

    def load(self, filename):
        self._filename = filename
        self.setWindowTitle(self._filename + " - mdview")
        self._reload()

    def _reload(self):
        if os.path.exists(self._filename):
            filename = self._filename
        else:
            filename = os.path.join(self.dataDir, "placeholder.md")
        txt = open(filename).read()
        self.setText(QString(txt))

    textChanged = pyqtSignal(QString)

    def setText(self, value):
        if self._text != value:
            self._text = value
            self.textChanged.emit(self._text)

    @pyqtProperty(QString, fset=setText, notify=textChanged)
    def text(self):
        return self._text


    def _openUrl(self, url):
        if url.isLocalFile() and url.path().endsWith(".md"):
            self.load(url.path())
        else:
            QDesktopServices.openUrl(url)
