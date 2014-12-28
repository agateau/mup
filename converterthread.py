import os

from PyQt4.QtCore import *


class ConverterThread(QThread):
    done = pyqtSignal(QString)

    def __init__(self, parent=None):
        super(ConverterThread, self).__init__(parent)
        self._mutex = QMutex()
        self._converter = None
        self._filename = None

    def setConverter(self, converter):
        with QMutexLocker(self._mutex):
            self._converter = converter

    def setFilename(self, filename):
        with QMutexLocker(self._mutex):
            self._filename = filename

    def filename(self):
        with QMutexLocker(self._mutex):
            name = self._filename
        return name

    def run(self):
        with QMutexLocker(self._mutex):
            filename = unicode(self._filename)
            if os.path.exists(filename) and self._converter is not None:
                html = self._converter.convert(self._filename)
            else:
                html = ''
        self.done.emit(html)
