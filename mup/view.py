from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebKit import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKitWidgets import *

from . import converters

from .converterthread import ConverterThread


class View(QWidget):
    internalUrlClicked = pyqtSignal(QUrl)
    loadRequested = pyqtSignal(str)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self._thread = ConverterThread()
        self._thread.done.connect(self._setHtml)

        self._setupView()
        self._setupLinkLabel()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(QMargins())
        layout.addWidget(self._view)

        self._lastScrollPos = None

    def _setupView(self):
        self._view = QWebView(self)
        self._view.contextMenuEvent = lambda e : None
        page = QWebPage()
        page.setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        page.linkClicked.connect(self._openUrl)
        page.linkHovered.connect(self._showHoveredLink)
        self._view.setPage(page)
        self._view.loadFinished.connect(self._onLoadFinished)

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

    def load(self, filename, converter, lastScrollPos=None):
        self._lastScrollPos = lastScrollPos
        self._thread.setFilename(filename)
        self._thread.setConverter(converter)

    def reload(self):
        self._lastScrollPos = self.scrollPosition()
        self._thread.reload()

    def find(self, text, backward=False):
        options = QWebPage.FindWrapsAroundDocument
        if backward:
            options |= QWebPage.FindBackward
        found = self._view.findText(text, options)

        # Redo highlight
        options = QWebPage.HighlightAllOccurrences
        self._view.findText("", options)
        self._view.findText(text, options)
        return found

    def removeFindHighlights(self):
        options = QWebPage.HighlightAllOccurrences
        self._view.findText("", options)

    def scrollPosition(self):
        return self._view.page().currentFrame().scrollPosition()

    def _setHtml(self, html):
        filename = str(self._thread.filename())
        baseUrl = QUrl.fromLocalFile(filename)
        self._view.setHtml(html, baseUrl)

    def _onLoadFinished(self):
        if self._lastScrollPos is not None:
            frame = self._view.page().currentFrame()
            frame.setScrollPosition(self._lastScrollPos)
            self._lastScrollPos = None

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
            elif converters.findConverters(str(url.path())):
                self.loadRequested.emit(url.path())
                return

        QDesktopServices.openUrl(url)

    def _showHoveredLink(self, link, title, textContent):
        if not link:
            self._linkLabelHideTimer.start()
            return

        self._linkLabelHideTimer.stop()
        text = link
        text.replace("file:///", "/")
        self._linkLabel.setText(text)
        self._linkLabel.adjustSize()

        self._linkLabel.show()
