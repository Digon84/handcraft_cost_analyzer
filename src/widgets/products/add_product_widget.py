import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg


class AddProductWidget(qtw.QDialog):
    adding_product_accepted = qtc.pyqtSignal(str, str, bool, str)

    def __init__(self, existing_products: list[str], existing_projects: list[str],  *args, **kwargs):
        super().__init__(*args, **kwargs)
        # code here
        self.setWindowTitle("Add new product")

        self.existing_products = existing_products
        self.existing_projects = existing_projects
        self.name_warning_label = self.get_warning_label()
        self.name_label = self.get_name_label()
        self.name_line_edit = self.get_name_line_edit()
        self.type_label = self.get_type_label()
        self.type_line_edit = self.get_type_line_edit()
        self.use_project_data = self.get_use_project_data()
        self.project_combo_box = self.get_project_combo_box()
        self.dialog_button_box = self.get_dialog_button_box()
        self.set_layout()
        # end of code

    def set_layout(self):
        h_layout_name = qtw.QHBoxLayout()
        h_layout_name.addWidget(self.name_label)
        h_layout_name.addWidget(self.name_line_edit)

        h_layout_type = qtw.QHBoxLayout()
        h_layout_type.addWidget(self.type_label)
        h_layout_type.addWidget(self.type_line_edit)

        v_layout = qtw.QVBoxLayout()

        v_layout.addWidget(self.name_warning_label)
        v_layout.addLayout(h_layout_name)
        v_layout.addLayout(h_layout_type)
        v_layout.addWidget(self.use_project_data)
        v_layout.addWidget(self.project_combo_box)
        v_layout.addWidget(self.dialog_button_box)

        self.setLayout(v_layout)

    def get_name_line_edit(self):
        line_edit = qtw.QLineEdit()
        line_edit.setPlaceholderText("Project name...")
        line_edit.textChanged.connect(self.validate_product_name)
        return line_edit

    def get_project_combo_box(self):
        combo_box = qtw.QComboBox()
        combo_box.setHidden(True)
        for project_name in self.existing_projects:
            combo_box.addItem(project_name)
        return combo_box

    def get_use_project_data(self):
        check_box = qtw.QCheckBox()
        check_box.setText("Use data from project")
        check_box.stateChanged.connect(self.use_project_data_state_changed)
        return check_box

    def get_dialog_button_box(self):
        dialog_box = qtw.QDialogButtonBox(qtc.Qt.Orientation.Horizontal)
        dialog_box.addButton(qtw.QDialogButtonBox.StandardButton.Ok)
        dialog_box.addButton(qtw.QDialogButtonBox.StandardButton.Cancel)
        dialog_box.accepted.connect(self.accept)
        dialog_box.rejected.connect(self.reject)
        return dialog_box

    def use_project_data_state_changed(self, state: qtc.Qt.CheckState):
        if state == qtc.Qt.CheckState.Checked.value:
            self.project_combo_box.setHidden(False)
        elif state == qtc.Qt.CheckState.Unchecked.value:
            self.project_combo_box.setHidden(True)

    def validate_product_name(self):
        add_button = self.dialog_button_box.button(qtw.QDialogButtonBox.StandardButton.Ok)
        if self.name_line_edit.text() in self.existing_products:
            self.set_name_warning("Please provide unique product name before continuing")
            add_button.setDisabled(True)
        else:
            self.clear_name_warning()
            add_button.setDisabled(False)

    def check_mandatory_fields(self):
        if self.name_line_edit.text():
            return True
        else:
            return False

    def accept(self):
        if self.check_mandatory_fields():
            use_project_data = True if self.use_project_data.checkState() == qtc.Qt.CheckState.Checked else False
            self.adding_product_accepted.emit(self.name_line_edit.text(),
                                              self.type_line_edit.text(),
                                              use_project_data,
                                              self.project_combo_box.currentText())
            super().accept()
        else:
            self.set_name_warning("Please provide product name.\nThis field is mandatory.")

    def set_name_warning(self, text: str):
        self.name_warning_label.setText(text)
        self.name_warning_label.setHidden(False)
        self.name_line_edit.setStyleSheet("border: 1px solid red")

    def clear_name_warning(self):
        self.name_warning_label.setHidden(True)
        self.name_line_edit.setStyleSheet("border: 1px solid black")

    def reject(self):
        print("Rejected")
        super().reject()

    @staticmethod
    def get_warning_label():
        label = qtw.QLabel()
        label.setStyleSheet("color:red")
        label.setHidden(True)
        return label

    @staticmethod
    def get_name_label():
        label = qtw.QLabel()
        label.setText("Project name: *")
        return label

    @staticmethod
    def get_type_label():
        label = qtw.QLabel()
        label.setText("Project type: ")
        return label

    @staticmethod
    def get_type_line_edit():
        line_edit = qtw.QLineEdit()
        line_edit.setPlaceholderText("Project type...")
        return line_edit


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = AddProductWidget(["test_product"], ["test_project_1", "test_project_2"])
    sys.exit(app.exec())
