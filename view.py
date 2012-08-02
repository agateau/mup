import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

import markdown

class WebPage(QWebPage):
    def javaScriptConsoleMessage(self, msg, lineNumber, sourceID):
        print "JsConsole(%s:%d): %s" % (sourceID, lineNumber, msg)

class View(QWidget):
    internalUrlClicked = pyqtSignal(QUrl)
    loadRequested = pyqtSignal(QString)

    def __init__(self, dataDir, parent=None):
        QWidget.__init__(self, parent)
        self.dataDir = dataDir
        self.filename = QString()
        self.template = open(os.path.join(self.dataDir, "template.html")).read()

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

    def load(self, filename):
        self.filename = filename
        self.reload()

    def reload(self):
        filename = unicode(self.filename)
        if not os.path.exists(filename):
            filename = os.path.join(self.dataDir, "placeholder.md")
        txt = open(filename).read()

        html = self.template.replace("%content%", markdown.markdown(txt))
        baseUrl = QUrl(os.path.dirname(filename) + "/")
        self.view.setHtml(html, baseUrl)

    def _openUrl(self, url):
        if url.scheme() == "internal":
            self.internalUrlClicked.emit(url)
        if url.scheme() in ("file", "") and url.path().endsWith(".md"):
            self.loadRequested.emit(url.path())
        else:
            QDesktopServices.openUrl(url)
