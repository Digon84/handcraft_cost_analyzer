from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import QDataWidgetMapper, QDialogButtonBox, QVBoxLayout, QLabel, QGridLayout, QLineEdit

from src.widgets.inventory_item_widget import InventoryItemWidget


class InventoryEditItem(InventoryItemWidget):
    def __init__(self, table_model, model_index):
        super().__init__(table_model)
        self.model_index = model_index
        self.mapper = QDataWidgetMapper(self)
        self.connect_mapper()

        self.exec()

    def connect_mapper(self):
        self.mapper.setModel(self.table_model)
        row_data = {}
        print(self.layout().count())
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
        self.update_values()
        super().accept()

    def update_values(self):
        query = QSqlQuery()

