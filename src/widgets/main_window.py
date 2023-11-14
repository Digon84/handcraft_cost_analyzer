from PyQt6 import uic

from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QCompleter
from PyQt6.QtSql import QSqlQueryModel

from src.database.inventory_handler import InventoryHandler
from src.database.table_layouts import INVENTORY_TABLE_LAYOUT
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
        self.source_table_model = self._set_up_table_model()
        self.ui.inventory_line_edit.setCompleter(self._set_up_completer())
        self.proxy_model = InventoryFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.source_table_model)
        self.ui.inventory_table_view.setModel(self.proxy_model)
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
        self.query = """SELECT component.component_id, component.material, component.type, component.made_off, component.shape,
                       component.color, component.finishing_effect, component.component_size, inventory.amount,
                       inventory.other, inventory.unit_price, inventory.total_price, inventory.add_date
                       FROM inventory
                       INNER JOIN component ON inventory.component_id == component.component_id"""
        model.setQuery(self.query)
        # model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        return model

    def inventory_add_from_file_clicked(self):
        columns_mapping = {self.source_table_model.headerData(i, Qt.Orientation.Horizontal): i for i in
                           range(self.source_table_model.columnCount())}
        self.inventory_add_from_file_window = LoadFromFileWidget(columns_mapping, self.source_table_model)
        self.inventory_add_from_file_window.submitted.connect(self.inventory_update_table)
        self.inventory_add_from_file_window.show()

    def inventory_add_manually_clicked(self):
        print("inventory_add_manually_clicked")
        add_new_item = AddNewItemManuallyWidget(self.source_table_model)

        self.source_table_model.setQuery(self.query)
        self.source_table_model.dataChanged.emit(self.source_table_model.index(0, 0),
                                                 self.source_table_model.index(self.source_table_model.rowCount(),
                                                                               self.source_table_model.columnCount()),
                                                 [])

        print(f"row count: {self.source_table_model.rowCount()}")
        # self.proxy_model.setSourceModel(self.source_table_model)


    def inventory_edit_item(self, model_index):
        print("inventory_table_view")
        # TODO: check if this is needed. Can we have one index?
        source_index = self.proxy_model.mapToSource(model_index)
        inventory_edit = InventoryEditItem(self.source_table_model, source_index)

    def inventory_search_clicked(self):
        print("inventory_search")
        self.proxy_model.filter = self.ui.inventory_line_edit.text()
        self.proxy_model.invalidateFilter()

    @pyqtSlot(list)
    def inventory_update_table(self, table_content_to_be_added):
        # TODO: change list of lists into structures. It would be easier to parse and set them
        for i in range(len(table_content_to_be_added)):
            record = self.source_table_model.record()
            for j in range(len(table_content_to_be_added[-1])):
                # TODO: to make it work I needed to change add_date to NOT NULL, in other cases 2 rows were added -
                #  one with date and one without. Check how it can be handled in the code
                record.setValue(*table_content_to_be_added[i][j])
                self.source_table_model.insertRecord(-1, record)
        self.source_table_model.select()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            if self.ui.inventory_table_view.selectedIndexes():
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Question)
                msg.setText("Delete item?")
                msg.setInformativeText(
                    "This operation will remove item from database. Do you want to continue?"
                )
                msg.setStandardButtons(
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
                )
                msg.exec()
                index = self.ui.inventory_table_view.selectedIndexes()[0]
                self.source_table_model.removeRow(index.row())
                self.source_table_model.submitAll()
                self.source_table_model.select()
