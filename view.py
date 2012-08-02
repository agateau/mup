import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

try:
    import docutils.core
    HAS_DOCUTILS = True
except ImportError:
    HAS_DOCUTILS = False

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

class WebPage(QWebPage):
    def javaScriptConsoleMessage(self, msg, lineNumber, sourceID):
        print "JsConsole(%s:%d): %s" % (sourceID, lineNumber, msg)

def getFileExtension(filename):
    return os.path.splitext(unicode(filename))[1]

class View(QWidget):
    internalUrlClicked = pyqtSignal(QUrl)
    loadRequested = pyqtSignal(QString)

    def __init__(self, dataDir, parent=None):
        QWidget.__init__(self, parent)
        self.dataDir = dataDir
        self.filename = QString()
        self.template = open(os.path.join(self.dataDir, "template.html")).read()

        self.setupConverters()
        self.setupView()

        layout = QHBoxLayout(self)
        layout.setMargin(0)
        layout.addWidget(self.view)

    def setupConverters(self):
        self.converters = dict()

        if HAS_DOCUTILS:
            def rstConverter(txt):
                return docutils.core.publish_string(txt, writer_name="html")
            self.converters[".rst"] = rstConverter

        if HAS_MARKDOWN:
            def mdConverter(txt):
                return self.template.replace("%content%", markdown.markdown(txt))
            self.converters[".md"] = mdConverter
            self.converters[".mkd"] = mdConverter
            self.converters[".markdown"] = mdConverter

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

        ext = getFileExtension(filename)
        converter = self.converters.get(ext)
        if not converter:
            print "Don't know how to convert file '%s'. Maybe you need to install a module for it?" % filename
            return
        html = converter(txt)
        baseUrl = QUrl(os.path.dirname(filename) + "/")
        self.view.setHtml(html, baseUrl)

    def _openUrl(self, url):
        if url.scheme() == "internal":
            self.internalUrlClicked.emit(url)
        if url.scheme() in ("file", "") and getFileExtension(url.path()) in self.converters:
            self.loadRequested.emit(url.path())
        else:
            QDesktopServices.openUrl(url)
