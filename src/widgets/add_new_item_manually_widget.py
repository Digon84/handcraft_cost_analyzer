from PyQt6.QtSql import QSqlRelationalTableModel
from PyQt6.QtWidgets import QLineEdit

from .inventory_item_widget import InventoryItemWidget


class AddNewItemManuallyWidget(InventoryItemWidget):
    def __init__(self, table_model: QSqlRelationalTableModel):
        super().__init__(table_model)
        self.exec()

    def accept(self):
        record = self.table_model.record()
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget_name = widget.property("name")
                if widget_name is not None:
                    record.setValue(widget_name, widget.text())
        self.table_model.insertRecord(-1, record)
        self.table_model.select()
        super().accept()
