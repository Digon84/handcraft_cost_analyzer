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

    def inventory_add_item_action_triggered(self):
        self.inventory_add_item_manually()

    def inventory_import_items_from_file_action_triggered(self):
        self.inventory_import_items_from_file()

    def inventory_export_to_csv_action_triggered(self):
        self.inventory_widget.export_data_to_csv()

    def print_action_triggered(self):
        print("print_action_triggered")

    def _create_actions(self):
        self._create_inventory_actions()
        self._create_print_actions()

    def _create_inventory_actions(self):
        self.inventory_add_item_action = qtg.QAction(self)
        self.inventory_add_item_action.setText("&inventory_add_item_action")
        self.inventory_add_item_action.setIcon(qtg.QIcon(qtg.QPixmap(self.get_image_path("plus.png"))))
        self.inventory_add_item_action.setToolTip("Add new inventory item")
        self.inventory_add_item_action.triggered.connect(self.inventory_add_item_action_triggered)

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

    def _create_print_actions(self):
        self.print_action = qtg.QAction(self)
        self.print_action.setText("&add_inventory_item_action")
        self.print_action.setIcon(qtg.QIcon(qtg.QPixmap(self.get_image_path("printer.png"))))
        self.print_action.setToolTip("Add new inventory item")
        self.print_action.triggered.connect(self.print_action_triggered)

    def _create_tool_bars(self):
        tool_bars = {}
        inventory_tool_bar = self.addToolBar("inventory_tool_bar")
        inventory_tool_bar.addAction(self.inventory_add_item_action)
        inventory_tool_bar.addAction(self.inventory_import_items_from_file_action)
        inventory_tool_bar.addAction(self.inventory_export_to_csv_action)
        tool_bars["inventory_tool_bar"] = inventory_tool_bar

        print_tool_bar = self.addToolBar("print_tool_bar")
        print_tool_bar.addAction(self.print_action)
        tool_bars["print_tool_bar"] = print_tool_bar

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
