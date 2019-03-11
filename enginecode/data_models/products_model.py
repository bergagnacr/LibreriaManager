
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSql import *


class ProductsDatabaseModel(QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super(ProductsDatabaseModel, self).__init__(*args, **kwargs)
        self.setTable("_Products")
        # self.setEditStrategy(QSqlTableModel.OnFieldChange)
        # self.select()
        self.setHeaderData(1, Qt.Horizontal, "Descripcion")
        self.setHeaderData(2, Qt.Horizontal, "Codigo\nProveedor")
        self.setHeaderData(3, Qt.Horizontal, "Categoria")
        self.setHeaderData(4, Qt.Horizontal, "Precio\nLista")
        self.setHeaderData(5, Qt.Horizontal, "Precio\nMinorista")
        self.setHeaderData(6, Qt.Horizontal, "Precio\nMayorista")
        self.setHeaderData(8, Qt.Horizontal, "Proveedor")
        self.setHeaderData(9, Qt.Horizontal, "Ultima\nActualizacion")

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.BackgroundRole:
            if index.column() == 6:
                return QBrush(QColor(212, 175, 55))
            if index.column() == 5:
                return QBrush(QColor(222, 91, 91))
            if index.column() == 8:
                if QSqlTableModel.data(self, index, Qt.DisplayRole) == "ARTEC":
                    return QBrush(QColor(255, 252, 193))
                if QSqlTableModel.data(self, index, Qt.DisplayRole) == "MONTENEGRO":
                    return QBrush(QColor(217, 252, 254))
                if QSqlTableModel.data(self, index, Qt.DisplayRole) == "AUDITOR":
                    return QBrush(QColor(138, 255, 210))
        if role == Qt.FontRole:
            font = QtGui.QFont()
            if QSqlQueryModel.data(self, self.index(index.row(), index.column()), Qt.DisplayRole):
                if index.column() == 6 or index.column() == 5:
                    font.setBold(True)
                    return font
        return QSqlTableModel.data(self, index, role)