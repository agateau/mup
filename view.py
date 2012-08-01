import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class WebPage(QWebPage):
    def javaScriptConsoleMessage(self, msg, lineNumber, sourceID):
        print "JsConsole(%s:%d): %s" % (sourceID, lineNumber, msg)

class View(QWidget):
    internalUrlClicked = pyqtSignal(QUrl)
    loadRequested = pyqtSignal(QString)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.dataDir = os.path.dirname(__file__)
        self._text = QString()
        self.filename = QString()

        self.setupView()

        layout = QHBoxLayout(self)
        layout.setMargin(0)
        layout.addWidget(self.view)

    def setupView(self):
        self.view = QWebView(self)
        page = WebPage()
        page.setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        page.linkClicked.connect(self._openUrl)
        self.view.setPage(page)
        page.mainFrame().addToJavaScriptWindowObject("qtWindow", self)
        url = QUrl("file://" + self.dataDir + "/view.html")
        self.view.setUrl(url)

    def load(self, filename):
        self.filename = filename
        self.reload()

    def reload(self):
        if os.path.exists(self.filename):
            filename = self.filename
        else:
            filename = os.path.join(self.dataDir, "placeholder.md")
        txt = open(filename).read()
        self.setText(QString(txt))

    # Definition of "text" property, used on the JS side
    textChanged = pyqtSignal(QString)

    def setText(self, value):
        if self._text != value:
            self._text = value
            self.textChanged.emit(self._text)

    @pyqtProperty(QString, fset=setText, notify=textChanged)
    def text(self):
        return self._text
    # /Definition

    def _openUrl(self, url):
        if url.scheme() == "internal":
            self.internalUrlClicked.emit(url)
        if url.isLocalFile() and url.path().endsWith(".md"):
            self.loadRequested.emit(url.path())
        else:
            QDesktopServices.openUrl(url)
