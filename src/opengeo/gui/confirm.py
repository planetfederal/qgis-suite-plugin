'''
Routines to ask for confirmation when performing certain operations 
'''
from PyQt4 import QtGui, QtCore

def _confirmationBox(title, msg):
    QtGui.QApplication.restoreOverrideCursor()
    ret = QtGui.QMessageBox.warning(None, title, msg,
                                    QtGui.QMessageBox.Yes |
                                    QtGui.QMessageBox.No,
                                    QtGui.QMessageBox.No)
    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
    return ret == QtGui.QMessageBox.Yes


def confirmDelete():
    askConfirmation = bool(QtCore.QSettings().value("/OpenGeo/Settings/General/ConfirmDelete", True, bool))
    if not askConfirmation:
        return True
    msg = "You confirm that you want to delete the selected elements?"
    reply = QtGui.QMessageBox.question(None, "Delete confirmation",
                                       msg, QtGui.QMessageBox.Yes |
                                       QtGui.QMessageBox.No,
                                       QtGui.QMessageBox.No)
    return reply != QtGui.QMessageBox.No


# noinspection PyPep8Naming
class DeleteDependentsDialog(QtGui.QDialog):

    def __init__(self, dependent, parent=None):
        super(DeleteDependentsDialog, self).__init__(parent)
        self.title = "Confirm Deletion"
        self.msg = "The following elements depend on the elements to delete " \
                   "and will be deleted as well:"
        names = set(["<b>- (" + e.__class__.__name__ + ")</b> &nbsp;" + e.name
                     for e in dependent])
        self.deletes = "<br><br>".join(names)
        self.question = "Do you really want to delete all these elements?"
        self.buttonBox = None
        self.initGui()

    def initGui(self):
        self.setWindowTitle(self.title)
        layout = QtGui.QVBoxLayout()

        msgLabel = QtGui.QLabel(self.msg)
        msgLabel.setWordWrap(True)
        layout.addWidget(msgLabel)

        deletesView = QtGui.QTextEdit()
        deletesView.append(unicode(self.deletes))
        deletesView.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        layout.addWidget(deletesView)

        questLabel = QtGui.QLabel(self.question)
        questLabel.setWordWrap(True)
        questLabel.setAlignment(QtCore.Qt.AlignHCenter)
        layout.addWidget(questLabel)

        self.buttonBox = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
        # noinspection PyUnresolvedReferences
        self.buttonBox.accepted.connect(self.accept)
        # noinspection PyUnresolvedReferences
        self.buttonBox.rejected.connect(self.reject)

        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.resize(500, 400)
