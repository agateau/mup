import subprocess

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from view import View

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self._filename = ""

        self.setupToolBar()
        self.view = View()
        self.view.mdUrlClicked.connect(self.load)
        self.setCentralWidget(self.view)

    def setupToolBar(self):
        toolBar = self.addToolBar(self.tr("Main"))
        action = toolBar.addAction(self.tr("Edit"))
        action.triggered.connect(self.edit)

    def load(self, filename):
        self._filename = filename
        self.setWindowTitle(filename + " - mdview")
        self.view.load(filename)

    def edit(self):
        # FIXME: Use configurable editor
        subprocess.call(["gvim", self._filename])
