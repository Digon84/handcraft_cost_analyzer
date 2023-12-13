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

        product_list_layout = qtw.QVBoxLayout()
        search_layout = qtw.QHBoxLayout()
        self.search_label = qtw.QLabel()
        print(ProductsListWidget.get_image_path("magnifier.png"))
        self.search_label.setPixmap(qtg.QPixmap(ProductsListWidget.get_image_path("magnifier.png")))

        self.search_line_edit = qtw.QLineEdit()

        self.search_line_edit.setPlaceholderText("Search...")

        self.products_list_view = qtw.QTreeView()

        search_layout.addWidget(self.search_line_edit)
        search_layout.addWidget(self.search_label)

        product_list_layout.addLayout(search_layout)
        product_list_layout.addWidget(self.products_list_view)

        self.setLayout(product_list_layout)
        # end of code
        self.show()

    @staticmethod
    def get_image_path(image_file_name):
        absolute_path = os.path.dirname(__file__)
        image_relative_path = os.path.join("..", "..", "..", "assets", "pictures", image_file_name)
        return os.path.join(absolute_path, image_relative_path)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = ProductsListWidget()
    sys.exit(app.exec())
