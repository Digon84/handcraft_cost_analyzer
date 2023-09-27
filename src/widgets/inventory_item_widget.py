import datetime

from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtSql import QSqlRelationalTableModel
from PyQt6.QtWidgets import QDialogButtonBox, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QDialog


class InventoryItemWidget(QDialog):
    def __init__(self, table_model: QSqlRelationalTableModel):
        super().__init__()
        self.table_model = table_model
        self.setWindowTitle("Update item")
        self.buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.draw_widget()

    def draw_widget(self):
        button_box = QDialogButtonBox(self.buttons)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        grid_layout = QGridLayout()

        for i in range(self.table_model.columnCount()):
            column_name = self.table_model.headerData(i, Qt.Orientation.Horizontal)

            label = QLabel(column_name)
            line_edit = QLineEdit()
            line_edit.setObjectName(column_name)
            line_edit.setProperty("name", column_name)

            if column_name == "add_date":
                line_edit.setText(str(datetime.date.today()))

            grid_layout.addWidget(label, i, 0)
            grid_layout.addWidget(line_edit, i, 1)

            self.setLayout(grid_layout)

        layout = QVBoxLayout()
        layout.addWidget(button_box)
        grid_layout.addLayout(layout, i+1, 1)
