
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSql import *


class ComprasDatabaseModel(QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super(ComprasDatabaseModel, self).__init__(*args, **kwargs)
        self.setTable("_Compras")

    def data(self, index, role=Qt.DisplayRole):
        return QSqlTableModel.data(self, index, role)
