from PyQt4.QtCore import *
from PyQt4.QtGui import *

from view import View

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.view = View()
        self.view.mdUrlClicked.connect(self.load)
        self.setCentralWidget(self.view)

    def load(self, filename):
        self.setWindowTitle(filename + " - mdview")
        self.view.load(filename)
