from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant, QModelIndex


class BaseTaBleModel(QAbstractTableModel):
    """
    Simmple basis model in Qt.
    Data is stored in the list.
    For more complex structures subclass QAbstractModel directly.
    Model needs a list of headers to work properly
    """

    def __init__(self, headers):
        super(BaseTaBleModel, self).__init__()

        self.headers = headers
        self.items = []

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.items)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.headers)

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        elif role != Qt.DisplayRole:
            return QVariant()

        data = self.items[index.row()][index.column()]
        return QVariant(data)

    def headerData(self, col, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[col])
        return QVariant()

    def setData(self, index, value, role=None):
        if index.isValid():
            self.items[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, position, rows, parent=QModelIndex(), *args, **kwargs):
        self.beginInsertRows(parent, position, position + rows - 1)
        for i in range(rows):
            self.items.insert(position, [None] * self.columnCount())
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QModelIndex(), *args, **kwargs):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for i in range(rows):
            self.items.pop(position)
        self.endRemoveRows()
        return True