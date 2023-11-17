import datetime

from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtSql import QSqlRelationalTableModel, QSqlQueryModel
from PyQt6.QtWidgets import QDialogButtonBox, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QDialog, QCompleter

from src.database.table_layouts import INVENTORY_TABLE_LAYOUT
from src.proxy_models.unique_items_proxy_model import UniqueItemsProxyModel


class InventoryItemWidget(QDialog):
    def __init__(self, table_model: QSqlQueryModel):
        super().__init__()
        self.line_edit_mapping = {}
        self.table_model = table_model
        self.setWindowTitle("Update item")
        self.buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.draw_widget()

    def draw_widget(self):
        button_box = QDialogButtonBox(self.buttons)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        grid_layout = QGridLayout()

        for i, column in enumerate(INVENTORY_TABLE_LAYOUT):
            # column_name = self.table_model.headerData(i, Qt.Orientation.Horizontal)
            # Don't drow for component_id. It is only used in queries.
            if column.is_hidden:
                continue

            label = QLabel(column.column_name + ("*" if column.is_mandatory else ""))
            line_edit = QLineEdit()
            line_edit.setObjectName(column.column_name)
            line_edit.setProperty("name", column.column_name)
            line_edit.setCompleter(self.get_completer(i))

            if column.column_name == "add_date":
                line_edit.setText(str(datetime.date.today()))
                line_edit.setDisabled(True)

            if column.is_disabled:
                line_edit.setDisabled(True)

            if column.column_name == "total_price" or column.column_name == "amount":
                line_edit.editingFinished.connect(self.set_unit_price)

            if column.is_disabled:
                line_edit.setDisabled(True)
            grid_layout.addWidget(label, i, 0)
            grid_layout.addWidget(line_edit, i, 1)
            self.line_edit_mapping[column.column_name] = line_edit
            self.setLayout(grid_layout)

        layout = QVBoxLayout()
        layout.addWidget(button_box)
        grid_layout.addLayout(layout, i+1, 1)

    def get_completer(self, column):
        completer_proxy_model = UniqueItemsProxyModel(self)

        completer_proxy_model.setSourceModel(self.table_model)
        completer_proxy_model.setFilterKeyColumn(column)
        completer_proxy_model.set_desired_column(column)
        completer = QCompleter(completer_proxy_model)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionColumn(column)

        return completer

    def set_unit_price(self):
        total_price = self.line_edit_mapping["total_price"].text()
        amount = self.line_edit_mapping["amount"].text()
        if total_price and amount:
            unit_price = round(float(total_price.replace(',', '.')) / float(amount.replace(',', '.')), 3)
            self.line_edit_mapping["unit_price"].setText(str(unit_price))
