from ui.mainwindow import Ui_MainWindow
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSql import *
import sys
from enginecode.processor.importer import ProcessorThread
from data_models.products_model import ProductsDatabaseModel
from data_models.compras_model import ComprasDatabaseModel
import time
import compra


class MainWindowDialog(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindowDialog, self).__init__()
        self.setupUi(self)
        # self.importer = PriceListsProcessor()
        # self.products_model = None
        # self.proxy_model = None
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName("./../database/database.db")
        self.setWindowTitle("Sarmiento Librerias")
        self.__init_status()
        self._setting_products_model()

        self.actionImportar_Lista.triggered.connect(self.__handle_import_price_list)
        self.lineEdit.returnPressed.connect(self.on_lineEdit_returnPressed)
        self.lineEdit.textChanged.connect(self.on_lineEdit_textChanged)
        self.pushButton.clicked.connect(self.on_new_compra_clicked)
        self.tabWidget.currentChanged.connect(self._handle_change_tab)

    def __register_new_dialog(self, dialog):
        return dialog.exec_()

    def __init_status(self):

        self.showMaximized()
        self.__set_icons()
        self.label_2.setPixmap(QtGui.QPixmap("./resources/images/IMG_8545.png"))
        self.tabWidget.setCurrentIndex(0)

    def __set_icons(self):
        """
        set Icons for all the ToolBar actions
        """
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./resources/icons/icons8-import-50.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionImportar_Lista.setIcon(icon)
        self.actionImportar_Lista.setText("Importar\nLista Precios")

    def _setting_products_model(self):
        """
        Set SQL Model for QT in order to load the information of products for ARTEC in TableView
        """
        self.tableView.reset()
        self.products_model = ProductsDatabaseModel()
        self.products_model.select()
        self.tableView.setModel(self.products_model)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableView.resizeColumnsToContents()
        self.tableView.hideColumn(7)
        self.tableView.hideColumn(0)
        self.tableView.hideColumn(3)
        print "Modelo actualizado"

    def _setting_compras_model(self):
        self.tableView_3.reset()
        self.compras_model = ComprasDatabaseModel()
        self.compras_model.select()
        self.tableView_3.setModel(self.compras_model)
        self.tableView_3.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView_3.setAlternatingRowColors(True)
        self.tableView_3.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView_3.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableView_3.resizeColumnsToContents()
    """
    EVENTS and SIGNALS
    """

    def __handle_import_price_list(self):
        """
        Event for asking the path of the new file to import for ARTEC provider
        """
        self.db.close()

        price_list_url = QFileDialog(self).getOpenFileName(self, "Abrir Lista de Precios")
        price_list_url = price_list_url[0].encode('utf-8')
        self.progressBar = QProgressDialog(parent=self, labelText="Procesando Lista...")
        self.progressBar.resize(400, 100)
        self.progressBar.setWindowTitle("Espere")
        self.progressBar.setAutoClose(True)

        # self.importer.import_sheet(price_list_url)
        # self.progressBar.setRange(0, 0)
        # self.progressBar.show()
        self.processor_thread = ProcessorThread(price_list_url)
        self.processor_thread.setMaximum.connect(self.set_maximum_value)
        self.processor_thread.updateProgress.connect(self.update_value)
        self.processor_thread.start()
        self.processor_thread.finished.connect(self._setting_products_model)

    def set_maximum_value(self, value):
        self.progressBar.setMaximum(value)

    def update_value(self, value):
        self.progressBar.setValue(value)

    def on_lineEdit_returnPressed(self):
        text = self.lineEdit.text()
        self.products_model.setFilter("description LIKE '%%" + text + "%%'")

    def on_lineEdit_textChanged(self, text):
        if text == "":
            self.products_model.setFilter("")

    def on_new_compra_clicked(self):
        compra_dialog = self.__register_new_dialog(compra.CompraDialog(self))
        if compra_dialog:
            print "Dialogo de compra cerrado con OK"
        else:
            print "Dialogo de compra cerrado con Cancel"

    def _handle_change_tab(self):
        if self.tabWidget.currentIndex() == 2:
            self._setting_compras_model()
        elif self.tabWidget.currentIndex() == 0:
            self._setting_products_model()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindowDialog()
    window.show()
    sys.exit(app.exec_())
