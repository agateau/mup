import logging
import os
import subprocess

from pkg_resources import resource_filename

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import config
from view import View

import converters


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.config = config.load()
        self.filename = unicode()
        self.converterList = []
        converters.init()

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

        self.converterComboBox = QComboBox()
        self.converterComboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addStretch()
        layout.addWidget(QLabel(self.tr("Converter:")))
        layout.addWidget(self.converterComboBox)
        toolBar.addWidget(widget)
        self.converterComboBox.currentIndexChanged.connect(self._onConverterChanged)
        self.converterComboBox.setFocusPolicy(Qt.ClickFocus)

    def setupView(self):
        self.view = View()
        self.view.loadRequested.connect(self.load)
        self.view.internalUrlClicked.connect(self.handleInternalUrl)

    def load(self, filename):
        if self.filename:
            self.watcher.removePath(self.filename)
        self.filename = os.path.abspath(unicode(filename))
        self.watcher.addPath(self.filename)
        self.setWindowTitle(self.filename + " - MUP")

        if os.path.exists(self.filename):
            viewFilename = self.filename
        else:
            viewFilename = resource_filename(__name__, "data/placeholder.html")
        self.converterList = converters.findConverters(viewFilename)
        if not self.converterList:
            viewFilename = resource_filename(__name__, "data/unsupported.html")
            self.converterList = converters.findConverters(viewFilename)
        assert self.converterList
        self.updateConverterComboBox()
        self.view.load(viewFilename, self.converterList[0])

    def updateConverterComboBox(self):
        self.converterComboBox.clear()
        for converter in self.converterList:
            self.converterComboBox.addItem(converter.name)

    def _onConverterChanged(self, index):
        self.view.setConverter(self.converterList[index])

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
        editor = self.config.get("editor", "gvim")
        subprocess.call([editor, self.filename])

    def handleInternalUrl(self, url):
        if url.path() == "create":
            self.edit()
        else:
            logging.error("Don't know how to handle internal url {}".format(url.toString()))

    def openFileDialog(self):
        name = QFileDialog.getOpenFileName(self, self.tr("Select a file to view"))
        if not name:
            return
        self.load(name)
