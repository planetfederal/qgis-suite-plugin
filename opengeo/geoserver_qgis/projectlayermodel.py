from PyQt4.QtCore import *
from PyQt4.QtGui import *

from operator import itemgetter


class ProjectLayerModel(QAbstractTableModel):

    header_data = ["Workspace", "Name", "Title", "Abstract", "Keywords"]
    NAME = 1

    def __init__(self, projectLayers):
        super(ProjectLayerModel, self).__init__()
        self.layer_list = []
        for lyr in projectLayers:
            self.layer_list.append([
                lyr["workspace"],
                lyr["name"],
                lyr["title"],
                lyr["abstract"],
                lyr["keywords"]
            ])

    def sort(self, column, order):
        self.layer_list = sorted(self.layer_list,
                                 key=itemgetter(column))
        if order == Qt.DescendingOrder:
            self.layer_list.reverse()
        self.reset()

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or \
           not (0 <= index.row() < len(self.layer_list)):
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.layer_list[index.row()][index.column()])

    def headerData(self, column, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QVariant(int(Qt.AlignLeft | Qt.AlignVCenter))
            return QVariant(int(Qt.AlignRight | Qt.AlignVCenter))

        if role != Qt.DisplayRole:
            return QVariant()

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header_data[column])
        return QVariant()

    def rowCount(self, index=QModelIndex()):
        return len(self.layer_list)

    def columnCount(self, index=QModelIndex()):
        return 5
