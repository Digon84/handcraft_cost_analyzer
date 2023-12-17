import os
import sys
from enum import IntEnum

from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg

from src.database.dao.inventory_dao import InventoryDAO
from src.database.inventory_handler import InventoryHandler
from src.database.sqlite_connector import SqliteConnector
from src.widgets.inventory.inventory_widget import InventoryWidget
from src.widgets.products.products_widget import ProductsWidget
from src.widgets.summary.summary_widget import SummaryWidget


class TabIndexes(IntEnum):
    Inventory = 0
    Products = 1
    Summary = 2


class MainWindow(qtw.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # code here
        self.setWindowTitle("Handcraft designer and cost analyzer")
        self.setGeometry(100, 100, 1500, 800)

        self.db_connector = InventoryHandler(database_connector=SqliteConnector)
        self.product_changed = False
        self.inventory_dao = InventoryDAO()
        self.inventory_widget = InventoryWidget()
        self.products_widget = ProductsWidget()
        self.summary_widget = SummaryWidget()
        self.tab_widget = self.get_tab_widget()
        self._create_actions()
        self.tool_bars = self._create_tool_bars()

        self.set_layout()
        # end of code

    def get_tab_widget(self):
        tab_widget = qtw.QTabWidget()

        tab_widget.addTab(self.inventory_widget, "Inventory")
        tab_widget.setTabIcon(TabIndexes.Inventory, qtg.QIcon(qtg.QPixmap(self.get_image_path("inventory.png"))))
        tab_widget.addTab(self.products_widget, "Products")
        tab_widget.setTabIcon(TabIndexes.Products, qtg.QIcon(qtg.QPixmap(self.get_image_path("products.png"))))
        tab_widget.addTab(self.summary_widget, "Summary")
        tab_widget.setTabIcon(TabIndexes.Summary, qtg.QIcon(qtg.QPixmap(self.get_image_path("summary.png"))))

        tab_widget.currentChanged.connect(self.inventory_tab_changed)

        return tab_widget

    def set_layout(self):
        self.setCentralWidget(self.tab_widget)

    # inventory functions
    def inventory_import_items_from_file(self):
        self.inventory_widget.inventory_add_items_from_file()

    def inventory_add_item_manually(self):
        self.inventory_widget.inventory_add_item()

    def inventory_tab_changed(self):
        if self.tab_widget.currentIndex() == TabIndexes.Inventory:
            self.tool_bars["inventory_tool_bar"].setDisabled(False)
        elif self.tab_widget.currentIndex() == TabIndexes.Products:
            self.tool_bars["inventory_tool_bar"].setDisabled(True)
        if self.tab_widget.currentIndex() == TabIndexes.Summary:
            self.tool_bars["inventory_tool_bar"].setDisabled(True)
            summary, error = self.inventory_dao.get_total_spend()
            self.summary_widget.set_total_spend(summary)

    # projects functions
    def products_add_product(self):
        print("Add product")
        self.products_widget.add_product("New product")
        self.save_action.setDisabled(False)

    # common actions triggered
    def add_item_action_triggered(self):
        if self.tab_widget.currentIndex() == TabIndexes.Inventory:
            self.inventory_add_item_manually()
        elif self.tab_widget.currentIndex() == TabIndexes.Products:
            self.products_add_product()

    def save_action_triggered(self):
        print("save_action_triggered")

    def copy_item_action_triggered(self):
        print("products_copy_product_action_triggered")

    def paste_item_action_triggered(self):
        print("products_paste_product_action_triggered")

    def print_action_triggered(self):
        print("print_action_triggered")

    # inventory actions triggered
    def inventory_import_items_from_file_action_triggered(self):
        self.inventory_import_items_from_file()

    def inventory_export_to_csv_action_triggered(self):
        self.inventory_widget.export_data_to_csv()

    def _create_actions(self):
        self._create_common_actions()
        self._create_inventory_actions()

    def _create_common_actions(self):
        self.add_item_action = qtg.QAction(self)
        self.add_item_action.setText("&add_item_action")
        self.add_item_action.setIcon(qtg.QIcon(qtg.QPixmap(self.get_image_path("plus.png"))))
        self.add_item_action.setToolTip("Add new item to inventory")
        self.add_item_action.triggered.connect(self.add_item_action_triggered)

        self.save_action = qtg.QAction(self)
        self.save_action.setText("&save_action")
        self.save_action.setIcon(qtg.QIcon(qtg.QPixmap(self.get_image_path("disk-black.png"))))
        self.save_action.setDisabled(False) if self.product_changed else self.save_action.setDisabled(True)
        self.save_action.setToolTip("Save")
        self.save_action.triggered.connect(self.save_action_triggered)

        self.copy_item_action = qtg.QAction(self)
        self.copy_item_action.setText("&copy_item_action")
        self.copy_item_action.setIcon(qtg.QIcon(qtg.QPixmap(self.get_image_path("document-copy.png"))))
        self.copy_item_action.setToolTip("Copy selected item")
        self.copy_item_action.triggered.connect(self.copy_item_action_triggered)

        self.paste_item_action = qtg.QAction(self)
        self.paste_item_action.setText("&paste_item_action")
        self.paste_item_action.setIcon(
            qtg.QIcon(qtg.QPixmap(self.get_image_path("clipboard-paste-document-text.png"))))
        self.paste_item_action.setToolTip("Paste selected item")
        self.paste_item_action.triggered.connect(self.paste_item_action_triggered)

        self.print_action = qtg.QAction(self)
        self.print_action.setText("&print_action")
        self.print_action.setIcon(qtg.QIcon(qtg.QPixmap(self.get_image_path("printer.png"))))
        self.print_action.setToolTip("Print current tab")
        self.print_action.triggered.connect(self.print_action_triggered)

    def _create_inventory_actions(self):
        self.inventory_import_items_from_file_action = qtg.QAction(self)
        self.inventory_import_items_from_file_action.setText("&inventory_import_items_from_file_action")
        self.inventory_import_items_from_file_action.setIcon(qtg.QIcon(
            qtg.QPixmap(self.get_image_path("document--plus.png"))))
        self.inventory_import_items_from_file_action.setToolTip("Import items to inventory from file")
        self.inventory_import_items_from_file_action.triggered.connect(self.inventory_import_items_from_file)

        self.inventory_export_to_csv_action = qtg.QAction(self)
        self.inventory_export_to_csv_action.setText("&inventory_export_to_csv_action")
        self.inventory_export_to_csv_action.setIcon(qtg.QIcon(qtg.QPixmap(self.get_image_path("document--arrow.png"))))
        self.inventory_export_to_csv_action.setToolTip("Export inventory content to csv file")
        self.inventory_export_to_csv_action.triggered.connect(self.inventory_export_to_csv_action_triggered)

    def _create_tool_bars(self):
        tool_bars = {}

        common_tool_bar = self.addToolBar("common_tool_bar")
        common_tool_bar.addAction(self.add_item_action)
        common_tool_bar.addAction(self.save_action)
        common_tool_bar.addAction(self.copy_item_action)
        common_tool_bar.addAction(self.paste_item_action)
        common_tool_bar.addAction(self.print_action)
        tool_bars["common_tool_bar"] = common_tool_bar

        inventory_tool_bar = self.addToolBar("inventory_tool_bar")
        inventory_tool_bar.addAction(self.inventory_import_items_from_file_action)
        inventory_tool_bar.addAction(self.inventory_export_to_csv_action)
        tool_bars["inventory_tool_bar"] = inventory_tool_bar

        return tool_bars

    @staticmethod
    def get_image_path(image_file_name):
        absolute_path = os.path.dirname(__file__)
        image_relative_path = os.path.join("..", "..", "assets", "pictures", image_file_name)
        return os.path.join(absolute_path, image_relative_path)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
