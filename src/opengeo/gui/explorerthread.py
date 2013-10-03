from PyQt4.QtCore import *
from PyQt4.QtGui import *
import traceback

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
            self.method(*self.args)
            self.finish.emit()
        except Exception, e:          
            #print traceback.format_exc()  
            self.error.emit(traceback.format_exc())
            