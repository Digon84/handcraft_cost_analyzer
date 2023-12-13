import os

from PyQt6 import uic

from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QCompleter, QFileDialog, QToolButton
from PyQt6.QtSql import QSqlQueryModel

from src.database.dao.component_dao import ComponentDAO
from src.database.dao.inventory_dao import InventoryDAO
from src.database.inventory_handler import InventoryHandler
from src.database.table_layouts import INVENTORY_TABLE_LAYOUT
from src.entities.inventory import Inventory
from src.file_operations.csv_exporter import write_content_to_csv
from src.proxy_models.inventory_filter_proxy_model import InventoryFilterProxyModel
from src.proxy_models.one_column_table_proxy_model import OneColumnTableProxyModel
from src.proxy_models.unique_items_proxy_model import UniqueItemsProxyModel
from src.database.sqlite_connector import SqliteConnector
from src.widgets.inventory.add_new_item_manually_widget import AddNewItemManuallyWidget
from src.widgets.inventory.edit_inventory_item_widget import InventoryEditItem
from src.widgets.inventory.inventory_widget import InventoryWidget
from src.widgets.inventory.load_from_file_widget import LoadFromFileWidget


class MainWindow(QMainWindow):

    data_saved = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("src/ui/main_window.ui", self)
        # self.show()

        self.inventory_add_from_file_window = None
        self.db_connector = InventoryHandler(database_connector=SqliteConnector)
        self.component_dao = ComponentDAO()
        self.inventory_dao = InventoryDAO()

        self.ui.action_add.triggered.connect(self.action_add_clicked)
        self.ui.action_import_from_file.triggered.connect(self.action_add_from_file_clicked)
        self.ui.action_copy.triggered.connect(self.copy_action_clicked)
        self.ui.action_export_to_file.triggered.connect(self.action_export_clicked)
        self.ui.action_paste.triggered.connect(self.action_paste_clicked)
        self.ui.action_print.triggered.connect(self.action_print_clicked)
        self.inventory_widget = InventoryWidget()
        self.ui.tabWidget.addTab(self.inventory_widget, "Inventory new")


        self.show()

    def inventory_add_from_file_clicked(self):
        self.inventory_widget.inventory_add_items_from_file()

    def inventory_add_manually_clicked(self):
        self.inventory_widget.inventory_add_item()

    def inventory_tab_changed(self):
        if self.ui.tabWidget.currentIndex() == 2:
            summary, error = self.inventory_dao.get_total_spend()
            self.ui.summary_total_spend.setText(str(summary))


    def action_add_clicked(self):
        self.inventory_add_manually_clicked()

    def action_add_from_file_clicked(self):
        self.inventory_add_from_file_clicked()

    def copy_action_clicked(self):
        print("copy_action_clicked")

    def action_export_clicked(self):
        self.inventory_widget.export_data_to_csv()

    def action_import_clicked(self):
        print("action_import_clicked")

    def action_paste_clicked(self):
        print("action_paste_clicked")

    def action_print_clicked(self):
        print("action_print_clicked")

