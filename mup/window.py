# encoding: utf-8
import logging
import os
import subprocess

from pkg_resources import resource_filename

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import config
from view import View
from findwidget import FindWidget

import converters

from history import History, HistoryItem


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.config = config.load()
        self.converterList = []
        converters.init()

        self.watcher = QFileSystemWatcher(self)
        self.watcher.fileChanged.connect(self._onFileChanged)

        self.setupHistory()

        self.setupView()
        self.setupToolBar()
        self.setWindowIcon(QIcon.fromTheme("text-plain"))

    def closeEvent(self, event):
        QMainWindow.closeEvent(self, event)

    def setupHistory(self):
        self._history = History()
        self._history.currentAboutToChange.connect(self._updateCurrentHistoryItemScrollPos)
        self._history.currentAboutToChange.connect(self._stopWatching)
        self._history.currentChanged.connect(self._loadCurrentHistoryItem)

    def setupToolBar(self):
        toolBar = self.addToolBar(self.tr("Main"))
        toolBar.setMovable(False)
        toolBar.setFloatable(False)
        toolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        action = toolBar.addAction(self.tr("Open"))
        action.setIcon(QIcon.fromTheme("document-open"))
        action.setShortcut(QKeySequence.Open)
        action.triggered.connect(self.openFileDialog)

        toolBar.addAction(self._history.backAction)
        toolBar.addAction(self._history.forwardAction)

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

        action = menu.addAction(self.tr("Find"))
        action.setShortcuts((Qt.CTRL + Qt.Key_F, Qt.Key_Slash))
        action.setIcon(QIcon.fromTheme("edit-find"))
        action.triggered.connect(self.toggleFindWidget)

        action = menu.addAction(self.tr("Find Next"))
        action.setShortcut(Qt.Key_F3)
        action.triggered.connect(self._findWidget.findNext)

        action = menu.addAction(self.tr("Find Previous"))
        action.setShortcut(Qt.SHIFT + Qt.Key_F3)
        action.triggered.connect(self._findWidget.findPrevious)

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
        central = QWidget()
        vboxLayout = QVBoxLayout(central)
        vboxLayout.setMargin(0)
        vboxLayout.setSpacing(0)

        self.view = View()
        self.view.loadRequested.connect(self.load)
        self.view.internalUrlClicked.connect(self.handleInternalUrl)

        self._findWidget = FindWidget(self.view)
        self._findWidget.escapePressed.connect(self.toggleFindWidget)
        self._findWidget.hide()

        vboxLayout.addWidget(self.view)
        vboxLayout.addWidget(self._findWidget)

        self.setCentralWidget(central)

    def _updateCurrentHistoryItemScrollPos(self):
        item = self._history.current()
        if item:
            item.scrollPos = self.view.scrollPosition()

    def load(self, filename):
        self._history.push(HistoryItem(filename, None))

    def _stopWatching(self):
        item = self._history.current()
        if item:
            self.watcher.removePath(item.filename)

    def _loadCurrentHistoryItem(self):
        item = self._history.current()

        # Update watcher
        self.watcher.addPath(item.filename)

        # Update title
        self.setWindowTitle(item.filename + " - MUP")

        # Find file to really show and update converter list
        if os.path.exists(item.filename):
            viewFilename = item.filename
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

    def _onFileChanged(self):
        item = self._history.current()
        if os.path.exists(item.filename):
            self.watcher.addPath(item.filename)
            self.reload()
        else:
            QTimer.singleShot(500, self._onFileChanged)

    def reload(self):
        self._updateCurrentHistoryItemScrollPos()
        self.view.reload()

    def edit(self):
        item = self._history.current()
        if not item:
            return
        editor = self.config.get("editor", "gvim")
        subprocess.call([editor, item.filename])

    def toggleFindWidget(self):
        visible = not self._findWidget.isVisible()
        self._findWidget.setVisible(visible)
        if visible:
            self._findWidget.prepareNewSearch()
        else:
            self.view.removeFindHighlights()

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
