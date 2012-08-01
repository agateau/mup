import subprocess

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from view import View

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.filename = ""

        self.setupToolBar()
        self.setupView()
        self.setCentralWidget(self.view)

    def setupToolBar(self):
        toolBar = self.addToolBar(self.tr("Main"))

        action = toolBar.addAction(self.tr("Reload"))
        action.setShortcut(Qt.Key_F5)
        action.triggered.connect(self.reload)

        action = toolBar.addAction(self.tr("Edit"))
        action.triggered.connect(self.edit)

    def setupView(self):
        self.view = View()
        self.view.loadRequested.connect(self.load)
        self.view.internalUrlClicked.connect(self.handleInternalUrl)

    def load(self, filename):
        self.filename = filename
        self.setWindowTitle(filename + " - mdview")
        self.view.load(filename)

    def reload(self):
        self.view.reload()

    def edit(self):
        # FIXME: Use configurable editor
        subprocess.call(["gvim", self._filename])
        subprocess.call([editor, self.filename])

    def handleInternalUrl(self, url):
        if url.path() == "create":
            self.edit()
        else:
            print "Don't know how to handle internal url", url.toString()
