from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

import converters

from converterthread import ConverterThread


class View(QWidget):
    internalUrlClicked = pyqtSignal(QUrl)
    loadRequested = pyqtSignal(QString)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._thread = ConverterThread()
        self._thread.done.connect(self._setHtml)

        self._setupView()
        self._setupLinkLabel()

        layout = QHBoxLayout(self)
        layout.setMargin(0)
        layout.addWidget(self._view)

        self._lastScrollPos = None

    def _setupView(self):
        self._view = QWebView(self)
        page = QWebPage()
        page.setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        page.linkClicked.connect(self._openUrl)
        page.linkHovered.connect(self._showHoveredLink)
        self._view.setPage(page)

    def _setupLinkLabel(self):
        self._linkLabel = QLabel(self._view)
        self._linkLabel.setStyleSheet("""
        background-color: #abc;
        color: #123;
        padding: 3px;
        border-bottom-right-radius: 3px;
        border-right: 1px solid #bce;
        border-bottom: 1px solid #bce;
        """)
        self._linkLabel.hide()
        self._linkLabelHideTimer = QTimer(self)
        self._linkLabelHideTimer.setSingleShot(True)
        self._linkLabelHideTimer.setInterval(250)
        self._linkLabelHideTimer.timeout.connect(self._linkLabel.hide)

    def load(self, filename, converter):
        self._thread.setFilename(filename)
        self._thread.setConverter(converter)
        self.reload()

    def reload(self):
        self._thread.start()

    def _setHtml(self, html):
        frame = self._view.page().currentFrame()
        self._lastScrollPos = frame.scrollPosition()

        filename = unicode(self._thread.filename())
        baseUrl = QUrl.fromLocalFile(filename)
        self._view.loadFinished.connect(self._onLoadFinished)
        self._view.setHtml(html, baseUrl)

    def setConverter(self, converter):
        self._thread.setConverter(converter)
        self.reload()

    def _onLoadFinished(self):
        if self._lastScrollPos is not None:
            frame = self._view.page().currentFrame()
            frame.setScrollPosition(self._lastScrollPos)
            self._lastScrollPos = None
            self._view.loadFinished.disconnect(self._onLoadFinished)

    def _openUrl(self, url):
        if url.scheme() == "internal":
            self.internalUrlClicked.emit(url)
            return

        if url.scheme() in ("file", ""):
            frame = self._view.page().currentFrame()
            if url.path() == frame.baseUrl().path():
                anchor = url.fragment()
                frame.scrollToAnchor(anchor)
                return
            elif converters.findConverters(unicode(url.path())):
                self.loadRequested.emit(url.path())
                return

        QDesktopServices.openUrl(url)

    def _showHoveredLink(self, link, title, textContent):
        if link.isEmpty():
            self._linkLabelHideTimer.start()
            return

        self._linkLabelHideTimer.stop()
        text = link
        text.replace("file:///", "/")
        self._linkLabel.setText(text)
        self._linkLabel.adjustSize()

        self._linkLabel.show()
