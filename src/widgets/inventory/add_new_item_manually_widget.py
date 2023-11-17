from PyQt6.QtCore import pyqtSignal
from PyQt6.QtSql import QSqlRelationalTableModel, QSqlQueryModel
from PyQt6.QtWidgets import QMessageBox

from .inventory_item_widget import InventoryItemWidget
from ...database.dao.component_dao import ComponentDAO
from ...database.dao.inventory_dao import InventoryDAO
from ...entities.component import Component
from ...entities.inventory import Inventory


class AddNewItemManuallyWidget(InventoryItemWidget):

    submitted = pyqtSignal(list)

    def __init__(self, table_model: QSqlQueryModel):
        super().__init__(table_model)
        self.inventory_item = None
        # self.exec()

    def accept(self):
        row = {}
        for i in range(self.layout().count()):

            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget_name = widget.property("name")
                if widget_name is not None:
                    row[widget_name] = widget.text()
        self.inventory_item: Inventory = Inventory(row)
        self.submitted.emit([self.inventory_item])
        super().accept()
