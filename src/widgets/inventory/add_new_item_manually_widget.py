from PyQt6.QtSql import QSqlRelationalTableModel, QSqlQueryModel
from PyQt6.QtWidgets import QMessageBox

from .inventory_item_widget import InventoryItemWidget
from ...database.dao.component_dao import ComponentDAO
from ...database.dao.inventory_dao import InventoryDAO
from ...entities.component import Component
from ...entities.inventory import Inventory


class AddNewItemManuallyWidget(InventoryItemWidget):
    def __init__(self, table_model: QSqlQueryModel):
        super().__init__(table_model)
        self.component_dao = ComponentDAO()
        self.inventory_dao = InventoryDAO()
        self.inventory_item = None
        self.exec()

    def accept(self):
        row = {}
        for i in range(self.layout().count()):

            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget_name = widget.property("name")
                if widget_name is not None:
                    row[widget_name] = widget.text()
        self.inventory_item: Inventory = Inventory(row)
        self.store_inventory_item_into_db()
        super().accept()

    def store_inventory_item_into_db(self):
        component_id, error_message = self.component_dao.get_component_id_or_insert(self.inventory_item.component)
        if component_id != -1:
            self.inventory_item.component_id = component_id
            result, error_message = self.inventory_dao.insert(self.inventory_item)
        else:
            result = False

        if not result:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Cannot add inventory item into database.")
            msg.setInformativeText(
                f"Adding inventory item into database was not possible: \n{error_message}"
            )
            msg.setStandardButtons(
                QMessageBox.StandardButton.Yes
            )
            msg.exec()

        return result, error_message
