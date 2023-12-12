import os

from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6 import QtSql as qsql

import sys

from src.database.dao.component_dao import ComponentDAO
from src.database.dao.inventory_dao import InventoryDAO
from src.database.table_layouts import INVENTORY_TABLE_LAYOUT
from src.entities.inventory import Inventory
from src.proxy_models.inventory_filter_proxy_model import InventoryFilterProxyModel
from src.proxy_models.one_column_table_proxy_model import OneColumnTableProxyModel
from src.proxy_models.unique_items_proxy_model import UniqueItemsProxyModel
from src.widgets.inventory.edit_inventory_item_widget import InventoryEditItem


class InventoryWidget(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.table_view = qtw.QTableView()
        self.source_table_model, self.filter_proxy_model = self.set_table_models()
        self.column_mapping = self.get_columns_mapping()
        self.hide_columns()
        self.search_text_field = self.get_search_text_field()
        self.search_button = qtw.QPushButton("Search")

        self.component_dao = ComponentDAO()
        self.inventory_dao = InventoryDAO()


        self.set_layouts()

        self.search_button.clicked.connect(self.search_clicked)
        self.search_text_field.returnPressed.connect(self.search_clicked)
        self.table_view.doubleClicked.connect(self.inventory_edit_item)



    def set_table_models(self):
        source_table_model = self._set_up_table_model()
        filter_proxy_model = InventoryFilterProxyModel(self)
        filter_proxy_model.setSourceModel(source_table_model)
        self.table_view.setModel(filter_proxy_model)
        return source_table_model, filter_proxy_model

    def get_search_text_field(self):
        line_edit = qtw.QLineEdit()
        line_edit.setPlaceholderText("Search...")
        line_edit.setClearButtonEnabled(True)
        line_edit.setCompleter(self._set_up_completer())
        clear_search_button = line_edit.findChild(qtw.QToolButton)
        clear_search_button.setIcon(
            qtg.QIcon(os.path.join(os.path.dirname(__file__), "../../../assets/pictures/cross.png"))
        )
        clear_search_button.clicked.connect(self.search_clicked)

        return line_edit

    def get_columns_mapping(self):
        return {self.source_table_model.headerData(i, qtc.Qt.Orientation.Horizontal): i - 2 for i in
                range(self.source_table_model.columnCount()) if
                self.source_table_model.headerData(i, qtc.Qt.Orientation.Horizontal) != "component_id" and
                self.source_table_model.headerData(i, qtc.Qt.Orientation.Horizontal) != "inventory_id"}

    def set_layouts(self):
        horizontal_layout = qtw.QHBoxLayout()
        vertical_layout = qtw.QVBoxLayout()

        horizontal_layout.addWidget(self.search_text_field)
        horizontal_layout.addWidget(self.search_button)
        vertical_layout.addLayout(horizontal_layout)
        vertical_layout.addWidget(self.table_view)

        self.setLayout(vertical_layout)

    def search_clicked(self):
        self.filter_proxy_model.filter = self.search_text_field.text()
        self.filter_proxy_model.invalidateFilter()

    def hide_columns(self):
        for i, column in enumerate(INVENTORY_TABLE_LAYOUT):
            if column.is_hidden:
                self.table_view.hideColumn(i)

    def inventory_edit_item(self, model_index):
        # TODO: check if this is needed. Can we have one index?
        source_index = self.filter_proxy_model.mapToSource(model_index)
        self.inventory_edit = InventoryEditItem(self.source_table_model, source_index)
        self.inventory_edit.submitted.connect(self.update_rows_in_inventory)
        self.inventory_edit.show()

    def keyPressEvent(self, event):
        if event.key() == qtc.Qt.Key.Key_Delete:
            if self.table_view.selectedIndexes():
                msg = qtw.QMessageBox()
                msg.setIcon(qtw.QMessageBox.Icon.Question)
                msg.setText("Delete item?")
                msg.setInformativeText(
                    "This operation will remove item(s) from database. Do you want to continue?"
                )
                msg.setStandardButtons(
                    qtw.QMessageBox.StandardButton.Yes | qtw.QMessageBox.StandardButton.Cancel
                )
                reply = msg.exec()
                if reply == qtw.QMessageBox.StandardButton.Yes:
                    selected_indexes = self.table_view.selectedIndexes()
                    for selected_index in selected_indexes:
                        inventory_id = self.source_table_model.data(
                            self.source_table_model.index(selected_index.row(), 0))
                        result, error = self.inventory_dao.delete(inventory_id)

                        if not result:
                            title = f"Cannot delete inventory item with id: {inventory_id}."
                            error_message = f"One or more items could not be added to database: \n{error}"
                            self.show_critical_message_box(title, error_message)
                    self.update_source_model()

    @qtc.pyqtSlot(list)
    def store_rows_into_inventory(self, table_content_to_be_inserted):
        for item in table_content_to_be_inserted:
            self.store_inventory_item_into_db(item)

        self.update_source_model()

    @qtc.pyqtSlot(int, Inventory)
    def update_rows_in_inventory(self, inventory_id, inventory_item):
        component_id, error = self.component_dao.get_component_id_or_insert(inventory_item.component)
        if component_id != -1:
            inventory_item.component_id = component_id
            result, error = self.inventory_dao.update(inventory_id, inventory_item)
        else:
            result = False

        if not result:
            title = "Cannot update inventory item."
            error_message = f"Item could not be updated: \n{error}"
            self.show_critical_message_box(title, error_message)

        self.update_source_model()

    def store_inventory_item_into_db(self, inventory_item):
        component_id, error = self.component_dao.get_component_id_or_insert(inventory_item.component)
        if component_id != -1:
            inventory_item.component_id = component_id
            result, error = self.inventory_dao.insert(inventory_item)
        else:
            result = False

        if not result:
            title = "Cannot add inventory item into database."
            error_message = f"One or more items could not be added to database: \n{error}"
            self.show_critical_message_box(title, error_message)

        return result, error

    def update_source_model(self):
        self.source_table_model.setQuery(self.query)
        self.source_table_model.dataChanged.emit(self.source_table_model.index(0, 0),
                                                 self.source_table_model.index(self.source_table_model.rowCount(),
                                                                               self.source_table_model.columnCount()),
                                                 [])
        self.table_view.scrollToBottom()

    @staticmethod
    def show_critical_message_box(box_title, error_message):
        msg = qtw.QMessageBox()
        msg.setIcon(qtw.QMessageBox.Icon.Critical)
        msg.setText(box_title)
        msg.setInformativeText(
            error_message
        )
        msg.setStandardButtons(
            qtw.QMessageBox.StandardButton.Ok
        )
        msg.exec()

    def _set_up_completer(self):
        completer_proxy_model = UniqueItemsProxyModel(self)
        one_column_table_proxy_model = OneColumnTableProxyModel()
        one_column_table_proxy_model.setSourceModel(self.source_table_model)
        completer_proxy_model.setSourceModel(one_column_table_proxy_model)
        completer = qtw.QCompleter(completer_proxy_model)
        completer.setCaseSensitivity(qtc.Qt.CaseSensitivity.CaseInsensitive)

        return completer

    def _set_up_table_model(self):
        model = qsql.QSqlQueryModel(self)
        self.query = """SELECT inventory.inventory_id, component.component_id, component.material, component.type,
        component.made_off, component.shape, 
        component.color, component.finishing_effect, component.component_size, inventory.amount,
                       inventory.unit_price, inventory.total_price, inventory.other, inventory.add_date
                       FROM inventory
                       INNER JOIN component ON inventory.component_id == component.component_id"""
        model.setQuery(self.query)
        return model


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    inventory = InventoryWidget()
    inventory.show()
    app.exec()
