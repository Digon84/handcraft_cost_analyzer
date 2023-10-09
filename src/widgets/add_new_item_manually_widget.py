from PyQt6.QtSql import QSqlRelationalTableModel, QSqlQueryModel

from .inventory_item_widget import InventoryItemWidget


class AddNewItemManuallyWidget(InventoryItemWidget):
    def __init__(self, table_model: QSqlQueryModel):
        super().__init__(table_model)
        self.exec()

    def accept(self):
        row = {}
        for i in range(self.layout().count()):

            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget_name = widget.property("name")
                if widget_name is not None:
                    row[widget_name] = widget.text()
        # self.table_model.insertRecord(-1, record)
        # self.table_model.select()
        self.insert_values(row)
        super().accept()

    def insert_values(self, row):
        pass
