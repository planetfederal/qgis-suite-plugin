from opengeo.geoserver import util
from PyQt4 import QtGui, QtCore

class TreeItem(QtGui.QTreeWidgetItem): 
    def __init__(self, element, icon = None, text = None): 
        QtGui.QTreeWidgetItem.__init__(self) 
        self.element = element    
        self.setData(0, QtCore.Qt.UserRole, element)            
        text = text if text is not None else util.name(element)
        self.setText(0, text)      
        if icon is not None:
            self.setIcon(0, icon)   
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)               
            
    def refreshContent(self, explorer):
        self.takeChildren()        
        if hasattr(self.element, "refresh"):
            self.element.refresh()
        explorer.run(self.populate, None, [])                
       
    def descriptionWidget(self, tree, explorer):                
        text = self.getDescriptionHtml(tree, explorer)                
        class MyBrowser(QtGui.QTextBrowser):
            def loadResource(self, type, name):                
                return None
        self.description = MyBrowser()                
        self.description.setOpenLinks(False)        
        def linkClicked(url):
            self.linkClicked(tree, explorer, url)
        self.description.connect(self.description, QtCore.SIGNAL("anchorClicked(const QUrl&)"), linkClicked)
        self.description.setHtml(text)   
        return self.description 
    
    def getDescriptionHtml(self, tree, explorer):
        html = self._getDescriptionHtml(tree, explorer)
        img = ""
        if hasattr(self, "iconPath"):
            img = '<img src="' + self.iconPath() + '"/>'
        header = u'<div style="background-color:#C7DBFC;"><h1>&nbsp; ' + img + "&nbsp;" + self.text(0) + '</h1></div>'
        html = u"""
            <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
            <html>
            <head>
            <style type="text/css">
                .section { margin-top: 25px; }
                table.header th { background-color: #dddddd; }
                table.header td { background-color: #f5f5f5; }
                table.header th, table.header td { padding: 0px 10px; }
                table td { padding-right: 20px; }
                .underline { text-decoration:underline; }
            </style>
            </head>
            <body>
            %s %s <br>
            </body>
            </html>
            """ % (header, html)  
        return html      
        
    def _getDescriptionHtml(self, tree, explorer):
        html = "<br>"
        actions = self.contextMenuActions(tree, explorer)
        if actions:
            html = "<p><b>Actions:</b></p><ul>" 
            for action in actions:
                if action.isEnabled():
                    html += '<li><a href="' + action.text() + '">' + action.text() + '</a></li>\n'
            html += '</ul>'
        return html 
    
    def linkClicked(self, tree, explorer, url):
        actionName = url.toString()
        actions = self.contextMenuActions(tree, explorer)
        for action in actions:
            if action.text() == actionName:
                action.trigger()
                return            
    
    def contextMenuActions(self, tree, explorer):
        return []   
    
    def multipleSelectionContextMenuActions(self, tree, explorer, selected):
        return []
    
    def acceptDroppedItem(self, tree, explorer, item):
        return []
        
    def acceptDroppedItems(self, tree, explorer, items):
        explorer.setProgressMaximum(len(items))
        toUpdate = []
        try:
            for i, item in enumerate(items):                
                toUpdate.extend(self.acceptDroppedItem(tree, explorer, item))                
                explorer.setProgress(i + 1)
        finally:
            explorer.resetActivity()
            return toUpdate
            
    def acceptDroppedUris(self, tree, explorer, uris):
        return []