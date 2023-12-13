import os
import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg

from src.widgets.products.product_details_widget import ProductDetailsWidget
from src.widgets.products.products_list_widget import ProductsListWidget


class ProductsWidget(qtw.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # code here
        self.product_list_widget = ProductsListWidget()
        self.product_details_widget = ProductDetailsWidget()
        self.set_layout()
        # end of code
        self.show()

    def set_layout(self):
        products_widget_layout = qtw.QHBoxLayout()
        products_widget_layout.addWidget(self.product_list_widget)
        products_widget_layout.addWidget(self.product_details_widget)
        products_widget_layout.setSpacing(0)
        self.setLayout(products_widget_layout)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = ProductsWidget()
    sys.exit(app.exec())
