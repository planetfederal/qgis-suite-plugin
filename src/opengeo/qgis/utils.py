import os
import uuid
import time
from PyQt4.QtCore import *


def temp_folder():
    tempDir = os.path.join(unicode(QDir.tempPath()), "suiteplugin")
    if not QDir(tempDir).exists():
        QDir().mkpath(tempDir)
    return unicode(os.path.abspath(tempDir))

def temp_filename(ext):
    path = temp_folder()
    ext = "" if ext is None else ext
    filename = path + os.sep + str(time.time())  + "." + ext
    return filename

def temp_filename_in_temp_folder(basename):
    '''returns a temporary filename for a given file, putting it into a temp folder but not changing its basename'''
    path = temp_folder()
    folder = os.path.join(path, str(uuid.uuid4()).replace("-",""))
    mkdir(folder)
    filename =  os.path.join(folder, basename)
    return filename

def mkdir(newdir):
    if os.path.isdir(newdir):
        pass
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            mkdir(head)
        if tail:
            os.mkdir(newdir)