from ui.compra import Ui_CompraDialog
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSql import *
import datetime
from data_models.productos_compra_model import ProductPorCompra
from processor.database import DatabaseManager


class Product(object):
    def __init__(self, description, code, provider, list_price, quantity):
        self.description = description
        self.code = code
        self.provider = provider
        self.list_price = list_price
        self.quantity = quantity

class CompraDialog(QtWidgets.QDialog, Ui_CompraDialog):
    def __init__(self, parent):
        super(CompraDialog, self).__init__(parent)
        self.setupUi(self)
        self.database_manager = DatabaseManager()

        self.__init_status()

        self.__set_model()

        self.productoNuevoRadioButton.toggled.connect(self.__handle_checkboxes)
        self.productoExistenteRadioButton.toggled.connect(self.__handle_checkboxes)

        self.codigoProductoExistenteLineEdit.textChanged.connect(self._handle_codigo_producto_existente)
        self.cantidadNuevoProductoLineEdit_2.textChanged.connect(self._handle_codigo_producto_existente)
        self.agregarProductoExistenteButton.clicked.connect(self._handle_agregar_producto_existente)
        self.codigoProductoNuevoLineEdit.textChanged.connect(self._handle_boton_nuevo_producto)
        self.descripcionNuevoProductoLineEdit.textChanged.connect(self._handle_boton_nuevo_producto)
        self.proveedorNuevoProductoLineEdit.textChanged.connect(self._handle_boton_nuevo_producto)
        self.precioListaNuevoProductoLineEdit.textChanged.connect(self._handle_boton_nuevo_producto)
        self.cantidadNuevoProductoLineEdit.textChanged.connect(self._handle_boton_nuevo_producto)
        self.agregarProductoNuevoButton.clicked.connect(self._handle_agregar_nuevo_producto)
        self.productosCompraTableView.clicked.connect(self._handle_click_table)
        self.okButton.clicked.connect(self.handle_ok_button)

    def __init_status(self):
        self.setWindowTitle("Agregar Nueva Compra")
        self.productoExistenteRadioButton.setChecked(True)
        self.productoExistenteGroupBox.setEnabled(True)
        self.productoNuevoRadioButton.setChecked(False)
        self.nuevoProductoGroupBox.setEnabled(False)
        self.borrarProductoButton.setEnabled(False)
        self.agregarProductoNuevoButton.setEnabled(False)
        self.agregarProductoExistenteButton.setEnabled(False)
        self.dateEdit.setDate(datetime.datetime.today())
        self.okButton.setEnabled(False)

    def __handle_checkboxes(self):
        if self.productoNuevoRadioButton.isChecked():
            self.nuevoProductoGroupBox.setEnabled(True)
            self.productoExistenteGroupBox.setEnabled(False)
        else:
            self.productoExistenteGroupBox.setEnabled(True)
            self.nuevoProductoGroupBox.setEnabled(False)

    def __set_model(self):
        self.model = ProductPorCompra()
        self.productosCompraTableView.setModel(self.model)
        self.productosCompraTableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.productosCompraTableView.setAlternatingRowColors(True)
        self.productosCompraTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.productosCompraTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.productosCompraTableView.resizeColumnsToContents()

    def add_new_existent(self, sql_consult, quantity):
        code = sql_consult[2].encode('utf-8')
        description = sql_consult[1].encode('utf-8')
        provider = sql_consult[8].encode('utf-8')
        list_price = sql_consult[4]
        self.model.insertRows(self.model.rowCount()+1, 1, [description, code, provider, list_price, quantity])

    def _handle_codigo_producto_existente(self):
        if self.codigoProductoExistenteLineEdit.text() == '' or self.cantidadNuevoProductoLineEdit_2.text() == '' or \
                self.cantidadNuevoProductoLineEdit_2.text() == '0':
            self.agregarProductoExistenteButton.setEnabled(False)
        else:
            self.agregarProductoExistenteButton.setEnabled(True)

    def _handle_boton_nuevo_producto(self):
        if self.codigoProductoNuevoLineEdit.text() == '' or self.descripcionNuevoProductoLineEdit.text() == '' or \
            self.proveedorNuevoProductoLineEdit.text() == '' or self.precioListaNuevoProductoLineEdit.text() == '' or \
                self.cantidadNuevoProductoLineEdit.text() == '':
            self.agregarProductoNuevoButton.setEnabled(False)
        else:
            self.agregarProductoNuevoButton.setEnabled(True)

    def _handle_agregar_producto_existente(self):
        code = self.codigoProductoExistenteLineEdit.text()
        sql_data = self.database_manager.return_product_data_with_code(code)
        if len(sql_data) > 0:
            quantity = int(self.cantidadNuevoProductoLineEdit_2.text())
            self.add_new_existent(sql_data[0], quantity)
        else:
            dialog = QMessageBox.critical(self, "Producto No existente", "El codigo del producto ingresado es erroneo",
                                          QMessageBox.Ok)
            dialog.show()
        self.codigoProductoExistenteLineEdit.clear()
        self.cantidadNuevoProductoLineEdit_2.clear()
        if self.model.rowCount() > 0:
            self.borrarProductoButton.setEnabled(True)
            self.okButton.setEnabled(True)

    def _handle_agregar_nuevo_producto(self):
        code = self.codigoProductoNuevoLineEdit.text()
        description = self.descripcionNuevoProductoLineEdit.text()
        provider = self.proveedorNuevoProductoLineEdit.text()
        list_price = float(self.precioListaNuevoProductoLineEdit.text())
        quantity = int(self.cantidadNuevoProductoLineEdit.text())
        self.model.insertRows(self.model.rowCount() + 1, 1, [description, code, provider, list_price, quantity])
        self.codigoProductoNuevoLineEdit.clear()
        self.descripcionNuevoProductoLineEdit.clear()
        self.proveedorNuevoProductoLineEdit.clear()
        self.precioListaNuevoProductoLineEdit.clear()

    def _handle_click_table(self):
        self.borrarProductoButton.setEnabled(True)

    def handle_ok_button(self):
        compra_code = self.codigoFacturaLineEdit.text()
        provider = self.proveedorLineEdit.text()
        date = self.dateEdit.text()
        product_codes = []
        for product in self.model.productos:
            code = product[1]
            product_codes.append(code)
        self.database_manager.nueva_compra(compra_code, provider, date, product_codes)
        self.accept()
