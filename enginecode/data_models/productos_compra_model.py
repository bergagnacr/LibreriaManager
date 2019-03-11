from PySide2.QtCore import *


class ProductPorCompra(QAbstractTableModel):
    def __init__(self, variable=None, parent=None):
        super(ProductPorCompra, self).__init__(parent)
        if variable is None:
            self.productos = []
        else:
            self.productos = variable
        self.header = ['Descripcion', 'Codigo\nProveedor', 'Proveedor', 'Precio\nLista', 'Cantidad']

    def rowCount(self, index=QModelIndex()):
        """ Returns the number of rows the model holds. """
        return len(self.productos)

    def columnCount(self, index=QModelIndex()):
        """ Returns the number of columns the model holds. """
        return len(self.header)

    def data(self, index, role=Qt.DisplayRole):
        """ Depending on the index and role given, return data. If not
            returning data, return None (PySide equivalent of QT's
            "invalid QVariant").
        """
        if not index.isValid():
            return None
        if not 0 <= index.row() < len(self.productos):
            return None

        if role == Qt.DisplayRole:
            return self.productos[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """ Set the headers to be displayed. """
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.header[section]
        return None

    def insertRows(self, position, rows=1, index=QModelIndex()):
        """ Insert a row into the model. """
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.productos.insert(position + row, index)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        """ Remove a row from the model. """
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        del self.productos[position:position + rows]
        self.endRemoveRows()
        return True