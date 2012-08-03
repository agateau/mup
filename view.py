import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

import converters

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

        self.setupView()

        layout = QHBoxLayout(self)
        layout.setMargin(0)
        layout.addWidget(self.view)

    def setupView(self):
        self.view = QWebView(self)
        page = WebPage()
        page.setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        page.linkClicked.connect(self._openUrl)
        page.linkHovered.connect(self.showToolTip)
        self.view.setPage(page)

    def load(self, filename):
        self.filename = filename
        self.reload()

    def reload(self):
        filename = unicode(self.filename)
        if not os.path.exists(filename):
            filename = os.path.join(self.dataDir, "placeholder.md")

        html = converters.convert(filename)
        baseUrl = QUrl.fromLocalFile(os.path.dirname(filename) + "/")
        self.view.setHtml(html, baseUrl)

    def _openUrl(self, url):
        if url.scheme() == "internal":
            self.internalUrlClicked.emit(url)
        if url.scheme() in ("file", "") and converters.canHandle(unicode(url.path())):
            self.loadRequested.emit(url.path())
        else:
            QDesktopServices.openUrl(url)

    def showToolTip(self, link, title, textContent):
        if title.isEmpty():
            text = link
        else:
            text = QString(title + "\n" + link)
        QToolTip.showText(QCursor.pos() + QPoint(12, 12), text) #, self.view.viewport())
