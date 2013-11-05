import os
import shutil
 
src = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'opengeo')
dst = os.path.join(os.path.expanduser("~"), '.qgis2', 'python', 'plugins', 'opengeo')
shutil.rmtree(dst, True)
shutil.copytree(src, dst)

