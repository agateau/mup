import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class HistoryItem(object):
    def __init__(self, filename, converter, scrollPos=None):
        self.filename = os.path.abspath(unicode(filename))
        self.converter = converter
        self.scrollPos = scrollPos

    def __str__(self):
        return os.path.basename(self.filename)


class History(QObject):
    currentAboutToChange = pyqtSignal()
    currentChanged = pyqtSignal()

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self._lst = []
        self._index = -1

        self.backAction = QAction(self.tr("Back"), self)
        self.backAction.setIcon(QIcon.fromTheme("go-previous"))
        self.backAction.triggered.connect(self._goBack)
        self.forwardAction = QAction(self.tr("Forward"), self)
        self.forwardAction.triggered.connect(self._goForward)
        self.forwardAction.setIcon(QIcon.fromTheme("go-next"))
        self._updateBackForwardActions()

        self.currentChanged.connect(self._updateBackForwardActions)

    def push(self, historyItem):
        """
        Discard items after _index and add our item
        """
        self.currentAboutToChange.emit()
        self._index += 1
        self._lst = self._lst[:self._index]
        self._lst.append(historyItem)
        self.currentChanged.emit()

    def current(self):
        return self._lst[self._index] if self._index != -1 else None

    def _canGoBack(self):
        return self._index > 0

    def _canGoForward(self):
        return self._index < len(self._lst) - 1

    def _goBack(self):
        assert self._canGoBack()
        self._go(-1)

    def _goForward(self):
        assert self._canGoForward()
        self._go(1)

    def _go(self, delta):
        self.currentAboutToChange.emit()
        self._index += delta
        self.currentChanged.emit()

    def _updateBackForwardActions(self):
        if self._canGoBack():
            self.backAction.setEnabled(True)
            item = self._lst[self._index - 1]
            tip = self.tr("Go back to %1").arg(str(item))
            self.backAction.setToolTip(tip)
        else:
            self.backAction.setEnabled(False)

        if self._canGoForward():
            self.forwardAction.setEnabled(True)
            item = self._lst[self._index + 1]
            tip = self.tr("Go to %1").arg(str(item))
            self.forwardAction.setToolTip(tip)
        else:
            self.forwardAction.setEnabled(False)
