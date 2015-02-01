import os
from PyQt4.QtCore import *
from PyQt4 import QtGui
import sip
from qgis.core import *
from qgis.gui import *
from opengeo.gui.exploreritems import *
from opengeo.gui.explorerwidget import ExplorerWidget
from opengeo import config
from qgis.utils import pluginMetadata
import traceback
from opengeo.gui.dialogs.errorreportdialog import ErrorReportDialog

class OpenGeoExplorer(QtGui.QDockWidget):

    objectName = 'OpenGeoExplorer'

    def __init__(self, parent = None, singletab = True):
        super(OpenGeoExplorer, self).__init__()
        self.singletab = singletab
        self.initGui()

    def initGui(self):
        self.explorerWidget = None
        self.progressMaximum = 0
        self.isProgressVisible = False
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.dockWidgetContents = QtGui.QWidget()
        self.setWindowTitle('OpenGeo Explorer')
        self.splitter = QtGui.QSplitter()
        self.splitter.setOrientation(Qt.Vertical)
        self.subwidget = QtGui.QWidget()
        self.explorerWidget = ExplorerWidget(self, self.singletab)
        self.toolbar = QtGui.QToolBar()
        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.toolbar.setVisible(self.singletab)
        self.setToolbarActions([])
        self.splitter.addWidget(self.explorerWidget)
        self.log = QtGui.QTextEdit()
        self.description = QtGui.QWidget()
        self.descriptionLayout = QtGui.QVBoxLayout()
        self.descriptionLayout.setSpacing(2)
        self.descriptionLayout.setMargin(0)
        self.description.setLayout(self.descriptionLayout)
        self.splitter.addWidget(self.description)
        self.setDescriptionWidget()
        showDescription = QSettings().value("/OpenGeo/Settings/General/ShowDescription", True, bool)
        self.description.setVisible(showDescription)
        self.progress = None
        self.layout = QtGui.QVBoxLayout()
        self.layout.setSpacing(2)
        self.layout.setMargin(0)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.splitter)
        self.dockWidgetContents.setLayout(self.layout)
        self.setWidget(self.dockWidgetContents)

        self.topLevelChanged.connect(self.dockStateChanged)

    def dockStateChanged(self, floating):
        if floating:
            self.resize(800, 450)
            self.splitter.setOrientation(Qt.Horizontal)
        else:
            self.splitter.setOrientation(Qt.Vertical)

    def setToolbarActions(self, actions):
        self.toolbar.clear()
        for action in actions:
            if action.icon().isNull():
                icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/process.png")
                action.setIcon(icon)
        if len(actions) == 0:
            refreshIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/refresh.png")
            refreshAction = QtGui.QAction(refreshIcon, "Refresh", self)
            refreshAction.triggered.connect(self.explorerWidget.refreshContent)
            actions.append(refreshAction)

        for action in actions:
            button = QtGui.QPushButton()
            button.setIcon(action.icon())
            button.setToolTip(action.text())
            button.setEnabled(action.isEnabled())
            button.clicked.connect(action.trigger)
            self.toolbar.addWidget(button)

        self.toolbar.update()

    def refreshContent(self):
        showDescription = QSettings().value("/OpenGeo/Settings/General/ShowDescription", True, bool)
        self.description.setVisible(showDescription)
        self.explorerWidget.refreshContent()
        self.refreshDescription()

    def catalogs(self):
        if self.explorerWidget is None:
            return {}
        return self.explorerWidget.catalogs()

    def pgDatabases(self):
        return self.explorerWidget.pgDatabases()

    def updateQgisContent(self):
        self.explorerWidget.updateQgisContent()

    def run(self, command, msg, refresh, *params):
        noerror = True
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))
        try:
            command(*params)
            for item in refresh:
                if item is not None:
                    item.refreshContent(self)
            if None in refresh:
                self.refreshContent()
            if msg is not None and not self.isProgressVisible:
                self.setInfo("Operation <i>" + msg + "</i> correctly executed")
        except Exception, e:
            s = e.message
            if not isinstance(s, unicode):
                s = unicode(e.message, errors = "ignore").encode("utf-8")
            self.setError(s + "\n" + traceback.format_exc())
            noerror = False
        finally:
            QtGui.QApplication.restoreOverrideCursor()
            self.refreshDescription()

        return noerror

    def resetActivity(self):
        if self.progress is not None:
            config.iface.messageBar().clearWidgets()
            self.isProgressVisible = False
            self.progress = None
            self.progressMaximum = 0

    def setProgress(self, value):
        if self.progress is not None and not sip.isdeleted(self.progress):
            self.progress.setValue(value)

    def setProgressMaximum(self, value, msg = ""):
        self.progressMaximum = value
        self.isProgressVisible = True
        self.progressMessageBar = config.iface.messageBar().createMessage(msg)
        self.progress = QtGui.QProgressBar()
        self.progress.setMaximum(self.progressMaximum)
        self.progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.progressMessageBar.layout().addWidget(self.progress)
        config.iface.messageBar().pushWidget(self.progressMessageBar, QgsMessageBar.INFO)

    def setInfo(self, msg):
        config.iface.messageBar().popWidget()
        config.iface.messageBar().pushMessage("Info", msg,
                                              level = QgsMessageBar.INFO,
                                              duration = 10)

    def setWarning(self, msg):
        config.iface.messageBar().pushMessage("Warning", msg,
                                              level = QgsMessageBar.WARNING,
                                              duration = 10)

    def setError(self, msg):
        firstLine = msg.split("\n")[0]
        if self.progressMaximum != 0:
            QtGui.QMessageBox.critical(self, "Error", firstLine)
        self.resetActivity()
        widget = config.iface.messageBar().createMessage("Error", firstLine)
        showButton = QtGui.QPushButton(widget)
        showButton.setText("View more")
        def showMore():
            dlg = QgsMessageOutput.createMessageOutput()
            dlg.setTitle('Error')
            dlg.setMessage(msg, QgsMessageOutput.MessageHtml)
            dlg.showMessage()
        showButton.pressed.connect(showMore)
        widget.layout().addWidget(showButton)
        config.iface.messageBar().pushWidget(widget, QgsMessageBar.CRITICAL,
                                             duration = 10)

    def setDescriptionWidget(self, widget = None):
        item = self.descriptionLayout.itemAt(0)
        if item:
            self.descriptionLayout.removeItem(item)
            item.widget().close()
        if widget is None:
            widget = QtGui.QTextBrowser()
            widget.setHtml(u'<div style="background-color:#ffffcc;"><h1>No description available</h1></div><ul>')

        self.descriptionLayout.addWidget(widget)



    def refreshDescription(self):
        item = self.explorerWidget.currentTree().lastClickedItem()
        if item is not None:
            try:
                self.explorerWidget.currentTree().treeItemClicked(item, 0)
            except:
                self.setDescriptionWidget(None)
