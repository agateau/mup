# coding: utf-8
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def _createArrowButton(arrowType, toolTip):
    button = QToolButton()
    button.setArrowType(arrowType)
    button.setAutoRaise(True)
    button.setToolTip(toolTip)
    return button


class FindWidget(QWidget):
    closeRequested = pyqtSignal()

    def __init__(self, view, parent=None):
        QWidget.__init__(self, parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self._view = view

        layout = QHBoxLayout(self)
        layout.setContentsMargins(QMargins())
        self._lineEdit = QLineEdit()

        self._previousButton = _createArrowButton(Qt.UpArrow, self.tr("Previous"))
        self._previousButton.clicked.connect(self.findPrevious)

        self._nextButton = _createArrowButton(Qt.DownArrow, self.tr("Next"))
        self._nextButton.clicked.connect(self.findNext)

        self._closeButton = QToolButton()
        self._closeButton.setAutoRaise(True)
        self._closeButton.setText("⨯")
        self._closeButton.setToolTip(self.tr("Close"))
        self._closeButton.clicked.connect(self.closeRequested)

        layout.addWidget(self._lineEdit)
        layout.addWidget(self._previousButton)
        layout.addWidget(self._nextButton)
        layout.addWidget(self._closeButton)

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

    def prepareNewSearch(self):
        self._lineEdit.clear()
        self._lineEdit.setFocus()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.closeRequested.emit()
        return False
