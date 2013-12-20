import os
import subprocess

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import config
from view import View

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.dataDir = os.path.dirname(__file__)
        self.config = config.load(self.dataDir)
        self.filename = QString()
        self.watcher = QFileSystemWatcher(self)
        self.watcher.fileChanged.connect(self._onFileChanged)

        self.setupToolBar()
        self.setupView()
        self.setCentralWidget(self.view)
        self.setWindowIcon(QIcon.fromTheme("text-plain"))

    def closeEvent(self, event):
        QMainWindow.closeEvent(self, event)

    def setupToolBar(self):
        toolBar = self.addToolBar(self.tr("Main"))
        toolBar.setMovable(False)
        toolBar.setFloatable(False)
        toolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        action = toolBar.addAction(self.tr("Open"))
        action.setIcon(QIcon.fromTheme("document-open"))
        action.setShortcut(QKeySequence.Open)
        action.triggered.connect(self.openFileDialog)

        action = toolBar.addAction(self.tr("Reload"))
        action.setIcon(QIcon.fromTheme("view-refresh"))
        action.setShortcut(QKeySequence.Refresh)
        action.triggered.connect(self.reload)

        action = toolBar.addAction(self.tr("Open with Editor"))
        action.setIcon(QIcon.fromTheme("document-edit"))
        action.triggered.connect(self.edit)

    def setupView(self):
        self.view = View(self.dataDir)
        self.view.loadRequested.connect(self.load)
        self.view.internalUrlClicked.connect(self.handleInternalUrl)

    def load(self, filename):
        if not self.filename.isEmpty():
            self.watcher.removePath(self.filename)
        self.filename = QString(os.path.abspath(unicode(filename)))
        self.watcher.addPath(self.filename)
        self.setWindowTitle(self.filename + " - mdview")
        self.view.load(self.filename)

    def _onFileChanged(self, name):
        if os.path.exists(self.filename):
            self.watcher.addPath(self.filename)
            self.reload()
        else:
            self._scheduleCheck()

    def _scheduleCheck(self):
        if os.path.exists(self.filename):
            self.watcher.addPath(self.filename)
            self.reload()
        else:
            QTimer.singleShot(500, self._scheduleCheck)

    def reload(self):
        self.view.reload()

    def edit(self):
        editor = self.config.get("general", "editor")
        subprocess.call([editor, self.filename])

    def handleInternalUrl(self, url):
        if url.path() == "create":
            self.edit()
        else:
            print "Don't know how to handle internal url", url.toString()

    def openFileDialog(self):
        name = QFileDialog.getOpenFileName(self, self.tr("Select a file to view"))
        if not name:
            return
        self.load(name)
