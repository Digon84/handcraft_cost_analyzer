import os

from PyQt6 import uic

from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QCompleter, QFileDialog, QToolButton
from PyQt6.QtSql import QSqlQueryModel

from src.database.dao.component_dao import ComponentDAO
from src.database.dao.inventory_dao import InventoryDAO
from src.database.inventory_handler import InventoryHandler
from src.database.table_layouts import INVENTORY_TABLE_LAYOUT
from src.entities.inventory import Inventory
from src.file_operations.csv_exporter import write_content_to_csv
from src.proxy_models.inventory_filter_proxy_model import InventoryFilterProxyModel
from src.proxy_models.one_column_table_proxy_model import OneColumnTableProxyModel
from src.proxy_models.unique_items_proxy_model import UniqueItemsProxyModel
from src.database.sqlite_connector import SqliteConnector
from src.widgets.inventory.add_new_item_manually_widget import AddNewItemManuallyWidget
from src.widgets.inventory.edit_inventory_item_widget import InventoryEditItem
from src.widgets.inventory.load_from_file_widget import LoadFromFileWidget


class MainWindow(QMainWindow):

    data_saved = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("src/ui/main_window.ui", self)
        # self.show()

        self.inventory_add_from_file_window = None
        self.db_connector = InventoryHandler(database_connector=SqliteConnector)
        self.component_dao = ComponentDAO()
        self.inventory_dao = InventoryDAO()
        self.source_table_model = self._set_up_table_model()
        self.columns_mapping = {self.source_table_model.headerData(i, Qt.Orientation.Horizontal): i - 2 for i in
                                range(self.source_table_model.columnCount()) if
                                self.source_table_model.headerData(i, Qt.Orientation.Horizontal) != "component_id" and
                                self.source_table_model.headerData(i, Qt.Orientation.Horizontal) != "inventory_id"}
        self.ui.inventory_line_edit.setCompleter(self._set_up_completer())
        self.proxy_model = InventoryFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.source_table_model)

        self.ui.inventory_table_view.setModel(self.proxy_model)
        self.ui.action_add.triggered.connect(self.action_add_clicked)
        self.ui.action_import_from_file.triggered.connect(self.action_add_from_file_clicked)
        self.ui.action_copy.triggered.connect(self.copy_action_clicked)
        self.ui.action_export_to_file.triggered.connect(self.action_export_clicked)
        self.ui.action_paste.triggered.connect(self.action_paste_clicked)
        self.ui.action_print.triggered.connect(self.action_print_clicked)

        # set search line edit
        self.ui.inventory_line_edit.setPlaceholderText("Search...")
        self.ui.inventory_line_edit.setClearButtonEnabled(True)
        clear_search_button = self.ui.inventory_line_edit.findChild(QToolButton)
        clear_search_button.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "../../assets/pictures/cross.png"))
        )
        clear_search_button.clicked.connect(self.inventory_search_clicked)

        for i, column in enumerate(INVENTORY_TABLE_LAYOUT):
            if column.is_hidden:
                self.ui.inventory_table_view.hideColumn(i)
        self.show()

    def _set_up_completer(self):
        completer_proxy_model = UniqueItemsProxyModel(self)
        one_column_table_proxy_model = OneColumnTableProxyModel()
        one_column_table_proxy_model.setSourceModel(self.source_table_model)
        completer_proxy_model.setSourceModel(one_column_table_proxy_model)
        completer = QCompleter(completer_proxy_model)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        return completer

    def _set_up_table_model(self):
        model = QSqlQueryModel(self)
        self.query = """SELECT inventory.inventory_id, component.component_id, component.material, component.type,
        component.made_off, component.shape, 
        component.color, component.finishing_effect, component.component_size, inventory.amount,
                       inventory.unit_price, inventory.total_price, inventory.other, inventory.add_date
                       FROM inventory
                       INNER JOIN component ON inventory.component_id == component.component_id"""
        model.setQuery(self.query)
        # model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        return model

    def inventory_add_from_file_clicked(self):
        # TODO: make unique column identification, not to hardcode, i-2 for skipping component_id
        self.inventory_add_from_file_window = LoadFromFileWidget(self.columns_mapping, self.source_table_model)
        self.inventory_add_from_file_window.submitted.connect(self.store_rows_into_inventory)
        self.inventory_add_from_file_window.show()

    def inventory_add_manually_clicked(self):
        self.add_new_item = AddNewItemManuallyWidget(self.source_table_model)
        self.add_new_item.submitted.connect(self.store_rows_into_inventory)
        self.add_new_item.show()

    def inventory_edit_item(self, model_index):
        # TODO: check if this is needed. Can we have one index?
        source_index = self.proxy_model.mapToSource(model_index)
        self.inventory_edit = InventoryEditItem(self.source_table_model, source_index)
        self.inventory_edit.submitted.connect(self.update_rows_in_inventory)
        self.inventory_edit.show()

    def inventory_search_clicked(self):
        self.proxy_model.filter = self.ui.inventory_line_edit.text()
        self.proxy_model.invalidateFilter()

    def inventory_tab_changed(self):
        if self.ui.tabWidget.currentIndex() == 2:
            summary, error = self.inventory_dao.get_total_spend()
            self.ui.summary_total_spend.setText(str(summary))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            if self.ui.inventory_table_view.selectedIndexes():
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Question)
                msg.setText("Delete item?")
                msg.setInformativeText(
                    "This operation will remove item(s) from database. Do you want to continue?"
                )
                msg.setStandardButtons(
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
                )
                reply = msg.exec()
                if reply == QMessageBox.StandardButton.Yes:
                    selected_indexes = self.ui.inventory_table_view.selectedIndexes()
                    for selected_index in selected_indexes:
                        inventory_id = self.source_table_model.data(
                            self.source_table_model.index(selected_index.row(), 0))
                        result, error = self.inventory_dao.delete(inventory_id)

                        if not result:
                            title = f"Cannot delete inventory item with id: {inventory_id}."
                            error_message = f"One or more items could not be added to database: \n{error}"
                            self.show_critical_message_box(title, error_message)
                    self.update_source_model()

    @pyqtSlot(list)
    def store_rows_into_inventory(self, table_content_to_be_inserted):
        for item in table_content_to_be_inserted:
            self.store_inventory_item_into_db(item)

        self.update_source_model()

    @pyqtSlot(int, Inventory)
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

    @staticmethod
    def show_critical_message_box(box_title, error_message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(box_title)
        msg.setInformativeText(
            error_message
        )
        msg.setStandardButtons(
            QMessageBox.StandardButton.Ok
        )
        msg.exec()

    def action_add_clicked(self):
        self.inventory_add_manually_clicked()

    def action_add_from_file_clicked(self):
        self.inventory_add_from_file_clicked()

    def copy_action_clicked(self):
        print("copy_action_clicked")

    def action_export_clicked(self):
        # TODO: same code is used in load_from_file_widget. Create a module to have it written once? but ExistingFiles vs Existing file
        file_dialog = QFileDialog()
        (file_name, filters) = file_dialog.getSaveFileName(self, "Export file to csv", "")

        data_to_write = self.get_data_for_export_to_csv()
        if file_name:
            write_content_to_csv(file_name, data_to_write)

    def action_import_clicked(self):
        print("action_import_clicked")

    def action_paste_clicked(self):
        print("action_paste_clicked")

    def action_print_clicked(self):
        print("action_print_clicked")

    def get_data_for_export_to_csv(self):
        data_to_export = []
        for row_index in range(self.source_table_model.rowCount()):
            row = {}
            for column_index in range(self.source_table_model.columnCount()):
                column_name = self.source_table_model.headerData(column_index, Qt.Orientation.Horizontal)
                data = self.source_table_model.data(self.source_table_model.index(row_index, column_index))
                if column_name != "inventory_id" and column_name != "component_id" and column_name != "add_date":
                    row[column_name] = data
            data_to_export.append(row)
        return data_to_export
