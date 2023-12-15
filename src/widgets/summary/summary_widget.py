import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg


class SummaryWidget(qtw.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # code here
        self.total_spend_label = self.get_total_spend_label()
        self.total_spend_line_edit = self.get_total_spend_line_edit()

        self.set_layouts()
        # end of code

    def set_layouts(self):
        h_box_layout = qtw.QHBoxLayout()

        h_box_layout.addWidget(self.total_spend_label)
        h_box_layout.addWidget(self.total_spend_line_edit)
        h_box_layout.setAlignment(qtc.Qt.AlignmentFlag.AlignTop | qtc.Qt.AlignmentFlag.AlignLeft)
        h_box_layout.addStretch()

        self.setLayout(h_box_layout)

    def set_total_spend(self, value: float):
        self.total_spend_line_edit.setText(str(value))

    @staticmethod
    def get_total_spend_label():
        return qtw.QLabel("Total spend")

    @staticmethod
    def get_total_spend_line_edit():
        total_spend_line_edit = qtw.QLineEdit()
        total_spend_line_edit.setDisabled(True)
        total_spend_line_edit.setMaximumWidth(250)
        return total_spend_line_edit


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = SummaryWidget()
    sys.exit(app.exec())
