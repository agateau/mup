# encoding: utf-8
import logging
import os
import subprocess

from pkg_resources import resource_filename

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import config
from view import View

import converters

from history import History, HistoryItem


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.config = config.load()
        self.filename = unicode()
        self.converterList = []
        converters.init()

        self.watcher = QFileSystemWatcher(self)
        self.watcher.fileChanged.connect(self._onFileChanged)

        self._history = History()
        self._backAction = QAction(self.tr("Back"), self)
        self._backAction.triggered.connect(self._goBack)
        self._forwardAction = QAction(self.tr("Forward"), self)
        self._forwardAction.triggered.connect(self._goForward)
        self._updateBackForwardActions()

        self.setupView()
        self.setupToolBar()
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

        toolBar.addAction(self._backAction)
        toolBar.addAction(self._forwardAction)

        self.converterComboBox = QComboBox()
        self.converterComboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        label = QLabel(self.tr("&Converter:"))
        label.setBuddy(self.converterComboBox)

        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addStretch()
        layout.addWidget(label)
        layout.addWidget(self.converterComboBox)
        toolBar.addWidget(widget)
        self.converterComboBox.currentIndexChanged.connect(self._onConverterChanged)
        self.converterComboBox.setFocusPolicy(Qt.ClickFocus)

        action = toolBar.addAction(self.tr("Menu"))
        action.setIcon(QIcon.fromTheme("applications-system"))
        action.setToolTip(self.tr("Menu (F10)"))
        action.setPriority(QAction.LowPriority)
        self.setupMenu(action)
        button = toolBar.widgetForAction(action)
        button.setPopupMode(QToolButton.InstantPopup)
        shortcut = QShortcut(Qt.Key_F10, self)
        shortcut.activated.connect(button.animateClick)

    def setupMenu(self, menuAction):
        menu = QMenu()
        menuAction.setMenu(menu)

        action = menu.addAction(self.tr("Force Reload"))
        action.setIcon(QIcon.fromTheme("view-refresh"))
        action.setShortcut(QKeySequence.Refresh)
        action.triggered.connect(self.reload)

        action = menu.addAction(self.tr("Open with Editor"))
        action.setIcon(QIcon.fromTheme("document-edit"))
        action.setShortcut(Qt.CTRL + Qt.Key_E)
        action.triggered.connect(self.edit)

        menu.addSeparator()

        action = menu.addAction(self.tr("About MUP"))
        action.triggered.connect(self.showAboutDialog)

    def showAboutDialog(self):
        title = self.tr("About MUP")
        text = self.tr(u"<h2>MUP, a Markup Previewer</h2>"
                u"<p>Aurélien Gâteau &ndash; <a href='mailto:mail@agateau.com'>mail@agateau.com</a></p>"
                u"<p><a href='http://github.com/agateau/mup'>http://github.com/agateau/mup</a></p>")
        QMessageBox.about(self, title, text)

    def setupView(self):
        self.view = View()
        self.view.loadRequested.connect(self.load)
        self.view.internalUrlClicked.connect(self.handleInternalUrl)
        self.setCentralWidget(self.view)

    def _goBack(self):
        self._updateCurrentHistoryItemScrollPos()
        self._history.goBack()
        self._updateBackForwardActions()
        self._loadCurrentHistoryItem()

    def _goForward(self):
        self._updateCurrentHistoryItemScrollPos()
        self._history.goForward()
        self._updateBackForwardActions()
        self._loadCurrentHistoryItem()

    def _updateCurrentHistoryItemScrollPos(self):
        item = self._history.current()
        if item:
            item.scrollPos = self.view.scrollPosition()

    def _updateBackForwardActions(self):
        self._backAction.setEnabled(self._history.canGoBack())
        self._forwardAction.setEnabled(self._history.canGoForward())

    def load(self, filename):
        self._updateCurrentHistoryItemScrollPos()
        self._history.push(HistoryItem(filename, None))
        self._updateBackForwardActions()
        self._loadCurrentHistoryItem()

    def _loadCurrentHistoryItem(self):
        item = self._history.current()

        # Update watcher
        if self.filename:
            self.watcher.removePath(self.filename)
        self.filename = os.path.abspath(unicode(item.filename))
        self.watcher.addPath(self.filename)

        # Update title
        self.setWindowTitle(self.filename + " - MUP")

        # Find file to really show and update converter list
        if os.path.exists(self.filename):
            viewFilename = self.filename
        else:
            viewFilename = resource_filename(__name__, "data/placeholder.html")
        self.converterList = converters.findConverters(viewFilename)
        if not self.converterList:
            viewFilename = resource_filename(__name__, "data/unsupported.html")
            self.converterList = converters.findConverters(viewFilename)
        assert self.converterList
        converter = item.converter or self.converterList[0]
        self.updateConverterComboBox(currentConverter=converter)

        # Update view
        self.view.load(viewFilename, converter, item.scrollPos)

    def updateConverterComboBox(self, currentConverter=None):
        self.converterComboBox.blockSignals(True)
        self.converterComboBox.clear()
        for idx, converter in enumerate(self.converterList):
            self.converterComboBox.addItem(converter.name)
            if converter == currentConverter:
                self.converterComboBox.setCurrentIndex(idx)
        self.converterComboBox.blockSignals(False)

    def _onConverterChanged(self, index):
        if index == -1:
            return
        self._history.current().converter = self.converterList[index]
        self._updateCurrentHistoryItemScrollPos()
        self._loadCurrentHistoryItem()

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
        self._updateCurrentHistoryItemScrollPos()
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
