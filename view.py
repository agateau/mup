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

        self.setupLinkLabel()

        layout = QHBoxLayout(self)
        layout.setMargin(0)
        layout.addWidget(self.view)

    def setupView(self):
        self.view = QWebView(self)
        page = WebPage()
        page.setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        page.linkClicked.connect(self._openUrl)
        page.linkHovered.connect(self.showHoveredLink)
        self.view.setPage(page)

    def setupLinkLabel(self):
        self.linkLabel = QLabel(self.view)
        self.linkLabel.setStyleSheet("""
        background-color: #abc;
        color: #123;
        padding: 3px;
        border-bottom-right-radius: 3px;
        border-right: 1px solid #bce;
        border-bottom: 1px solid #bce;
        """)
        self.linkLabel.hide()
        self.linkLabelHideTimer = QTimer(self)
        self.linkLabelHideTimer.setSingleShot(True)
        self.linkLabelHideTimer.setInterval(250)
        self.linkLabelHideTimer.timeout.connect(self.linkLabel.hide)

    def load(self, filename):
        self.filename = filename
        self.reload()

    def reload(self):
        filename = unicode(self.filename)
        if not os.path.exists(filename):
            filename = os.path.join(self.dataDir, "placeholder.md")

        frame = self.view.page().currentFrame()
        pos = frame.scrollPosition()

        html = converters.convert(filename)
        baseUrl = QUrl.fromLocalFile(os.path.dirname(filename) + "/")
        self.view.setHtml(html, baseUrl)

        frame.setScrollPosition(pos)

    def _openUrl(self, url):
        if url.scheme() == "internal":
            self.internalUrlClicked.emit(url)
        if url.scheme() in ("file", "") and converters.canHandle(unicode(url.path())):
            self.loadRequested.emit(url.path())
        else:
            QDesktopServices.openUrl(url)

    def showHoveredLink(self, link, title, textContent):
        if link.isEmpty():
            self.linkLabelHideTimer.start()
            return

        self.linkLabelHideTimer.stop()
        text = link
        text.replace("file:///", "/")
        self.linkLabel.setText(text)
        self.linkLabel.adjustSize()

        self.linkLabel.show()
