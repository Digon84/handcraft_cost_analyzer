import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg

from src.entities.inventory import Inventory
from src.widgets.inventory.inventory_widget import InventoryWidget


class AddComponentWidget(qtw.QDialog):
    components_selected = qtc.pyqtSignal(list, str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # code here
        self.setWindowTitle("Select component")
        self.setGeometry(100, 100, 1320, 800)
        self.inventory = InventoryWidget()
        self.inventory.group_by_component_id()
        self.amount_label = self.get_amount_label()
        self.amount_line_edit = self.get_amount_line_edit()
        self.dialog_button_box = self.get_dialog_button_box()

        self.set_layout()

        # end of code

    def set_layout(self):
        vertical_layout = qtw.QVBoxLayout()
        vertical_layout.addWidget(self.inventory)

        horizontal_layout = qtw.QHBoxLayout()
        horizontal_layout.addWidget(self.amount_label)
        horizontal_layout.addWidget(self.amount_line_edit)

        vertical_layout.addLayout(horizontal_layout)
        vertical_layout.addWidget(self.dialog_button_box)

        self.setLayout(vertical_layout)

    def get_dialog_button_box(self):
        dialog_box = qtw.QDialogButtonBox(qtc.Qt.Orientation.Horizontal)
        dialog_box.addButton(qtw.QDialogButtonBox.StandardButton.Ok)
        dialog_box.addButton(qtw.QDialogButtonBox.StandardButton.Cancel)
        dialog_box.accepted.connect(self.accept)
        dialog_box.rejected.connect(self.reject)
        return dialog_box

    def accept(self):
        if self.amount_line_edit.text() and self.inventory.get_selected_indexes():
            amount = self.amount_line_edit.text()
            print(amount)
            inventory_items = self.inventory.get_selected_inventory_items()
            self.components_selected.emit(inventory_items, amount)
            super().accept()
        else:
            self.show_warning_message_box("Select product and fill the amount.",
                                          "Please select the component(s) and specify the amount.")

    def reject(self):
        super().reject()

    @staticmethod
    def show_warning_message_box(box_title, warning_message):
        msg = qtw.QMessageBox()
        msg.setIcon(qtw.QMessageBox.Icon.Warning)
        msg.setText(box_title)
        msg.setInformativeText(
            warning_message
        )
        msg.setStandardButtons(
            qtw.QMessageBox.StandardButton.Ok
        )
        msg.exec()

    @staticmethod
    def get_amount_label():
        label = qtw.QLabel()
        label.setText("Amount used: ")
        return label

    @staticmethod
    def get_amount_line_edit():
        line_edit = qtw.QLineEdit()
        line_edit.setPlaceholderText("Amount...")
        return line_edit


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = AddComponentWidget()
    w.show()
    sys.exit(app.exec())
