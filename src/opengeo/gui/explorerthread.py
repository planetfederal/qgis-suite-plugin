from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ExplorerThread(QThread):
    
    message = pyqtSignal(str)
    error = pyqtSignal(str)
    finish = pyqtSignal()
            
    def __init__(self, method, *args):
        QThread.__init__(self)       
        self.method = method       
        self.args = args                                               
                
    def run (self):                
        try:
            #self.message.emit(" ".join(command) + "\n")
            print self.method
            print self.args
            
            self.method(*self.args)
            self.finish.emit()
        except Exception, e:            
            self.error.emit(unicode(e))