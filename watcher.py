import os

from PyQt4.QtCore import *

import pyinotify

class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, watcher):
        pyinotify.ProcessEvent.__init__(self)
        self.watcher = watcher

    def process_IN_MODIFY(self, event):
        self.watcher.onChanged(event.pathname)

class Watcher(QObject):
    changed = pyqtSignal()

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.watchId = None
        self.filename = None
        self.watchManager = pyinotify.WatchManager()
        self.notifier = pyinotify.ThreadedNotifier(self.watchManager, EventHandler(self))
        self.notifier.start()

    def stop(self):
        self.notifier.stop()

    def setFilename(self, filename):
        filename = os.path.abspath(unicode(filename))
        if self.filename == filename:
            print "Already watching", self.filename
            return
        self.filename = filename

        if self.watchId is not None:
            self.watchManager.rm_watch(self.watchId)

        aDir = os.path.split(self.filename)[0]
        # No need to watch for IN_CREATE, IN_MODIFY is emitted right after a creation
        wdd = self.watchManager.add_watch(aDir, pyinotify.IN_MODIFY)
        assert len(wdd) == 1
        self.watchId = wdd.values()[0]

    def onChanged(self, filename):
        if self.filename == filename:
            self.changed.emit()
