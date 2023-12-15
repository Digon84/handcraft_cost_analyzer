import os
import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg


class ProductsListWidget(qtw.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # code here
        self.setMaximumWidth(350)

        self.search_label = self.get_search_label()
        self.search_line_edit = self.get_search_line_edit()
        self.products_list_view = self.get_product_list_view()

        self.set_layouts()

        # end of code

    def set_layouts(self):
        product_list_layout = qtw.QVBoxLayout()
        search_layout = qtw.QHBoxLayout()

        search_layout.addWidget(self.search_line_edit)
        search_layout.addWidget(self.search_label)

        product_list_layout.addLayout(search_layout)
        product_list_layout.addWidget(self.products_list_view)

        self.setLayout(product_list_layout)

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
    def get_product_list_view():
        return qtw.QTreeView()

    @staticmethod
    def get_image_path(image_file_name):
        absolute_path = os.path.dirname(__file__)
        image_relative_path = os.path.join("..", "..", "..", "assets", "pictures", image_file_name)
        return os.path.join(absolute_path, image_relative_path)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = ProductsListWidget()
    sys.exit(app.exec())
