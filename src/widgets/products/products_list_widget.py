import os
import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6 import QtSql as qsql

from src.database.dao.products_dao import ProductsDAO


class ProductsListWidget(qtw.QWidget):
    item_selection_changed = qtc.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # code here
        self.setMaximumWidth(350)
        self.products = []
        self.product_dao = ProductsDAO()
        self.search_label = self.get_search_label()
        self.search_line_edit = self.get_search_line_edit()
        self.products_list_widget = self.get_product_list_widget()

        self.set_layouts()

        # end of code

    def set_layouts(self):
        product_list_layout = qtw.QVBoxLayout()
        search_layout = qtw.QHBoxLayout()

        search_layout.addWidget(self.search_line_edit)
        search_layout.addWidget(self.search_label)

        product_list_layout.addLayout(search_layout)
        product_list_layout.addWidget(self.products_list_widget)

        self.setLayout(product_list_layout)

    def get_product_list_widget(self):
        tree_widget = qtw.QTreeWidget()
        self.products, _ = self.product_dao.get_product_names()
        tree_widget.setHeaderHidden(True)

        for index, self.products in enumerate(self.products):
            item = qtw.QTreeWidgetItem()
            item.setText(0, self.products)
            tree_widget.insertTopLevelItem(index, item)

        tree_widget.currentItemChanged.connect(self.current_item_changed)
        tree_widget.itemChanged.connect(self.handle_item_changed)

        return tree_widget

    def current_item_changed(self, current: qtw.QTreeWidgetItem, previous: qtw.QTreeWidgetItem):
        print("load_currently_selected_item_data")
        print(f"Current item: {current.text(0)}")
        self.item_selection_changed.emit(current.text(0))

    def handle_item_changed(self, item: qtw.QTreeWidgetItem, column: int):
        name = item.text(0)

        if not name.endswith(" *"):
            item.setText(column, name + " *")

    def add_product(self, product_name):
        item = qtw.QTreeWidgetItem()
        item.setText(0, product_name + " *")
        item.setFlags(item.flags() | qtc.Qt.ItemFlag.ItemIsEditable)
        self.products_list_widget.insertTopLevelItem(self.products_list_widget.topLevelItemCount(), item)
        self.products_list_widget.setCurrentItem(item)

    @staticmethod
    def get_search_label():
        search_label = qtw.QLabel()
        search_label.setPixmap(qtg.QPixmap(ProductsListWidget.get_image_path("magnifier.png")))
        return search_label

    @staticmethod
    def get_search_line_edit():
        search_line_edit = qtw.QLineEdit()
        search_line_edit.setPlaceholderText("Search...")
        return search_line_edit

    @staticmethod
    def get_image_path(image_file_name):
        absolute_path = os.path.dirname(__file__)
        image_relative_path = os.path.join("..", "..", "..", "assets", "pictures", image_file_name)
        return os.path.join(absolute_path, image_relative_path)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = ProductsListWidget()
    sys.exit(app.exec())
