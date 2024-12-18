import os
import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg


class ProductDetailsWidget(qtw.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # code here
        self.picture_placeholders = self.get_picture_placeholders()
        self.components_summary_table = self.get_components_summary_table()
        self.comments_field = self.get_comments_field()
        self.additional_table = self.get_additional_table()
        self.price_for_piece_label = self.get_price_for_piece_label()
        self.price_for_piece_value_label = self.get_price_for_piece_value_label()
        self.price_for_pair_label = self.get_price_for_pair_label()
        self.price_for_pair_value_label = self.get_price_for_pair_value_label()
        self.product_type_label = self.get_product_type_label()
        self.product_type_line_edit = self.get_product_type_line_edit()
        self.amount_label = self.get_amount_label()
        self.amount_line_edit = self.get_amount_line_edit()
        self.set_layouts()
        # end of code

    @staticmethod
    def get_price_for_piece_label():
        price_for_piece_label = qtw.QLabel("Price for piece: ")
        price_for_piece_label.setMaximumWidth(100)
        return price_for_piece_label

    @staticmethod
    def get_picture_placeholders():
        picture_placeholders = []
        for i in range(3):
            picture_placeholder = qtw.QLabel()
            picture_placeholder.setPixmap(qtg.QPixmap(ProductDetailsWidget.get_image_path("plus.png")))
            picture_placeholder.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)

            picture_placeholder.setFrameShape(qtw.QFrame.Shape.Box)
            picture_placeholder.setFrameShadow(qtw.QFrame.Shadow.Plain)
            picture_placeholder.setLineWidth(1)
            picture_placeholder.setMinimumWidth(250)
            picture_placeholders.append(picture_placeholder)
        return picture_placeholders

    def set_layouts(self):
        project_details_layout = qtw.QGridLayout()
        details_layout = qtw.QGridLayout()

        details_layout.addWidget(self.price_for_piece_label, 0, 0)
        details_layout.addWidget(self.price_for_piece_value_label, 0, 1)
        details_layout.addWidget(self.price_for_pair_label, 1, 0)
        details_layout.addWidget(self.price_for_pair_value_label, 1, 1)
        details_layout.addWidget(self.product_type_label, 2, 0)
        details_layout.addWidget(self.product_type_line_edit, 2, 1)
        details_layout.addWidget(self.amount_label, 3, 0)
        details_layout.addWidget(self.amount_line_edit, 3, 1)

        project_details_layout.addWidget(self.picture_placeholders[0], 0, 0)
        project_details_layout.addWidget(self.picture_placeholders[1], 1, 0)
        project_details_layout.addWidget(self.picture_placeholders[2], 2, 0)
        project_details_layout.addWidget(self.components_summary_table, 0, 1)
        project_details_layout.addWidget(self.additional_table, 1, 1)
        project_details_layout.addWidget(self.comments_field, 2, 1)
        project_details_layout.addLayout(details_layout, 3, 0)

        self.setLayout(project_details_layout)

    @staticmethod
    def get_components_summary_table():
        return qtw.QTableView()

    @staticmethod
    def get_comments_field():
        comments_field = qtw.QTextEdit()
        comments_field.setPlaceholderText("Comments...")
        return comments_field

    @staticmethod
    def get_additional_table():
        return qtw.QTableView()

    @staticmethod
    def get_price_for_piece_value_label():
        price_for_piece_value_label= qtw.QLabel("-")
        price_for_piece_value_label.setMaximumWidth(150)
        return price_for_piece_value_label

    @staticmethod
    def get_price_for_pair_label():
        price_for_pair_label = qtw.QLabel("Price for pair: ")
        price_for_pair_label.setMaximumWidth(100)
        return price_for_pair_label

    @staticmethod
    def get_price_for_pair_value_label():
        price_for_pair_value_label = qtw.QLabel("-")
        price_for_pair_value_label.setMaximumWidth(150)
        return price_for_pair_value_label

    @staticmethod
    def get_product_type_label():
        product_type_label = qtw.QLabel("Product type: ")
        product_type_label.setMaximumWidth(100)
        return product_type_label

    @staticmethod
    def get_product_type_line_edit():
        product_type_line_edit = qtw.QLineEdit()
        product_type_line_edit.setMaximumWidth(150)
        return product_type_line_edit

    @staticmethod
    def get_amount_label():
        amount_label = qtw.QLabel("Amount: ")
        amount_label.setMaximumWidth(100)
        return amount_label

    @staticmethod
    def get_amount_line_edit():
        amount_line_edit = qtw.QLineEdit()
        amount_line_edit.setMaximumWidth(150)
        return amount_line_edit

    @staticmethod
    def get_image_path(image_file_name):
        absolute_path = os.path.dirname(__file__)
        image_relative_path = os.path.join("..", "..", "..", "assets", "pictures", image_file_name)
        return os.path.join(absolute_path, image_relative_path)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = ProductDetailsWidget()
    sys.exit(app.exec())
