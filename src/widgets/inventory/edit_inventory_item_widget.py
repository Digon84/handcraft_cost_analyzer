from PyQt6.QtCore import pyqtSignal
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import QDataWidgetMapper

from src.entities.inventory import Inventory
from src.widgets.inventory.inventory_item_widget import InventoryItemWidget


class InventoryEditItem(InventoryItemWidget):

    submitted = pyqtSignal(int, Inventory)

    def __init__(self, table_model, model_index):
        super().__init__(table_model)
        self.model_index = model_index
        self.mapper = QDataWidgetMapper(self)
        self.connect_mapper()

    def connect_mapper(self):
        self.mapper.setModel(self.table_model)
        row_data = {}
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget_name = widget.property("name")
                if widget_name is not None:
                    column_index = self.table_model.record().indexOf(widget_name)
                    self.mapper.addMapping(widget, column_index)
                    row_data[widget_name] = self.table_model.index(self.model_index.row(), column_index).data()
        self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.ManualSubmit)
        self.mapper.setCurrentModelIndex(self.model_index)

    def accept(self):
        row_data = {}
        inventory_id = self.table_model.data(self.table_model.index(self.model_index.row(), 0))
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget_name = widget.property("name")
                if widget_name is not None:
                    row_data[widget_name] = widget.text()
        inventory = Inventory(row_data)
        self.submitted.emit(inventory_id, inventory)
        super().accept()
