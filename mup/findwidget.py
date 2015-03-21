from PyQt4.QtCore import *
from PyQt4.QtGui import *


class FindWidget(QWidget):
    escapePressed = pyqtSignal()

    def __init__(self, view, parent=None):
        QWidget.__init__(self, parent)

        self._view = view

        layout = QHBoxLayout(self)
        self._lineEdit = QLineEdit()
        layout.addWidget(self._lineEdit)

        self._findTimer = QTimer(self)
        self._findTimer.setSingleShot(True)
        self._findTimer.setInterval(100)
        self._findTimer.timeout.connect(self._doFind)

        self._lineEdit.textEdited.connect(self._findTimer.start)
        self._lineEdit.installEventFilter(self)

        self._notFoundPalette = QPalette(self._lineEdit.palette())
        self._notFoundPalette.setColor(self._lineEdit.backgroundRole(),
                                       QColor(255, 102, 102))

    def findNext(self):
        self._doFind()

    def findPrevious(self):
        self._view.find(self._lineEdit.text(), backward=True)

    def _doFind(self):
        text = self._lineEdit.text()
        found = self._view.find(text)
        if found or text.isEmpty():
            self._lineEdit.setPalette(self.palette())
        else:
            self._lineEdit.setPalette(self._notFoundPalette)

    def setFocus(self):
        self._lineEdit.setFocus()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.escapePressed.emit()
        return False
