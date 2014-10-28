import os
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *



class ValidationErrorDialog(QtGui.QDialog):

    def __init__(self, message, parent = None):
        super(ValidationErrorDialog, self).__init__(parent)
        self.message = message
        self.initGui()

    def initGui(self):
        self.resize(400, 100)
        self.setWindowTitle('Validation')

        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setMargin(10)

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setMargin(10)

        self.msgLabel = QtGui.QLabel(
                                     "The metadata did not validate.")
        self.imgLabel = QtGui.QLabel()
        self.imgLabel.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__),
                                                           "..", "..", "images", "warning32.png")))
        self.imgLabel.setMaximumWidth(50)
        self.horizontalLayout.addWidget(self.imgLabel)
        self.horizontalLayout.addWidget(self.msgLabel)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.text = QtGui.QPlainTextEdit()
        self.text.setVisible(False)
        self.text.setPlainText(unicode(self.message))
        self.verticalLayout.addWidget(self.text)
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Close)
        self.showErrors = QtGui.QPushButton()
        self.showErrors.setText("Show errors detail")
        self.showErrors.clicked.connect(self.showErrorsPressed)
        self.buttonBox.addButton(self.showErrors, QtGui.QDialogButtonBox.ActionRole)

        self.verticalLayout.addWidget(self.buttonBox)
        self.setLayout(self.verticalLayout)

        self.buttonBox.rejected.connect(self.closePressed)

    def closePressed(self):
        self.close()

    def showErrorsPressed(self):
        if self.text.isVisible():
            self.showErrors.setText("Show errors detail")
            self.text.setVisible(False)
            self.resize(400, 100)
        else:
            self.resize(400, 400)
            self.text.setVisible(True)
            self.showErrors.setText("Hide errors detail")

