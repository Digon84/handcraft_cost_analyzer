import os
import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg


class ProductDetailsWidget(qtw.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # code here
        project_details_layout = qtw.QGridLayout()

        self.picture_placeholders = []
        for i in range(3):
            picture_placeholder = qtw.QLabel()
            picture_placeholder.setPixmap(qtg.QPixmap(ProductDetailsWidget.get_image_path("plus.png")))
            picture_placeholder.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)

            picture_placeholder.setFrameShape(qtw.QFrame.Shape.Box)
            picture_placeholder.setFrameShadow(qtw.QFrame.Shadow.Plain)
            picture_placeholder.setLineWidth(1)
            picture_placeholder.setMinimumWidth(250)
            self.picture_placeholders.append(picture_placeholder)

        self.components_summary_table = qtw.QTableView()

        self.comments_field = qtw.QTextEdit()
        self.comments_field.setPlaceholderText("Comments...")

        self.additional_table = qtw.QTableView()

        details_layout = qtw.QGridLayout()
        self.price_for_piece_label = qtw.QLabel("Price for piece: ")
        self.price_for_piece_value_label = qtw.QLabel("-")
        self.price_for_piece_label.setMaximumWidth(100)
        self.price_for_piece_value_label.setMaximumWidth(150)
        details_layout.addWidget(self.price_for_piece_label, 0, 0)
        details_layout.addWidget(self.price_for_piece_value_label, 0, 1)

        self.price_for_pair_label = qtw.QLabel("Price for pair: ")
        self.price_for_pair_value_label = qtw.QLabel("-")
        self.price_for_pair_label.setMaximumWidth(100)
        self.price_for_pair_value_label.setMaximumWidth(150)
        details_layout.addWidget(self.price_for_pair_label, 1, 0)
        details_layout.addWidget(self.price_for_pair_value_label, 1, 1)

        self.product_type_label = qtw.QLabel("Product type: ")
        self.product_type_line_edit = qtw.QLineEdit()
        self.product_type_label.setMaximumWidth(100)
        self.product_type_line_edit.setMaximumWidth(150)
        details_layout.addWidget(self.product_type_label, 2, 0)
        details_layout.addWidget(self.product_type_line_edit, 2, 1)

        self.amount_label = qtw.QLabel("Amount: ")
        self.amount_line_edit = qtw.QLineEdit()
        self.amount_label.setMaximumWidth(100)
        self.amount_line_edit.setMaximumWidth(150)
        details_layout.addWidget(self.amount_label, 3, 0)
        details_layout.addWidget(self.amount_line_edit, 3, 1)

        project_details_layout.addWidget(self.picture_placeholders[0], 0, 0)
        project_details_layout.addWidget(self.picture_placeholders[1], 1, 0)
        project_details_layout.addWidget(self.picture_placeholders[2], 2, 0)
        project_details_layout.addWidget(self.components_summary_table, 0, 1)
        project_details_layout.addWidget(self.comments_field, 1, 1)
        project_details_layout.addWidget(self.additional_table, 2, 1)
        project_details_layout.addLayout(details_layout, 3, 0)

        self.setLayout(project_details_layout)
        # end of code
        self.show()

    @staticmethod
    def get_image_path(image_file_name):
        absolute_path = os.path.dirname(__file__)
        image_relative_path = os.path.join("..", "..", "..", "assets", "pictures", image_file_name)
        return os.path.join(absolute_path, image_relative_path)

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = ProductDetailsWidget()
    sys.exit(app.exec())
