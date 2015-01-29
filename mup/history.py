from PyQt4.QtCore import *


class HistoryItem(object):
    def __init__(self, filename, converter, scrollPos=None):
        self.filename = filename
        self.converter = converter
        self.scrollPos = scrollPos


class History(QObject):
    currentAboutToChange = pyqtSignal()
    currentChanged = pyqtSignal()

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self._lst = []
        self._index = -1

    def push(self, historyItem):
        """
        Discard items after _index and add our item
        """
        self.currentAboutToChange.emit()
        self._index += 1
        self._lst = self._lst[:self._index]
        self._lst.append(historyItem)
        self.currentChanged.emit()

    def canGoBack(self):
        return self._index > 0

    def canGoForward(self):
        return self._index < len(self._lst) - 1

    def goBack(self):
        assert self.canGoBack()
        self._go(-1)

    def goForward(self):
        assert self.canGoForward()
        self._go(1)

    def _go(self, delta):
        self.currentAboutToChange.emit()
        self._index += delta
        self.currentChanged.emit()

    def current(self):
        return self._lst[self._index] if self._index != -1 else None
