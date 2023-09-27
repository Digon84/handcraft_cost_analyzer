from PyQt6.QtCore import Qt
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

        print(self.layout().count())
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget_name = widget.property("name")
                if widget_name is not None:
                    self.mapper.addMapping(widget, self.table_model.fieldIndex(widget_name))
        self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.ManualSubmit)
        self.mapper.setCurrentModelIndex(self.model_index)

    def accept(self):
        self.mapper.submit()
        super().accept()
