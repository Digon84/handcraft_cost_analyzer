from PyQt6 import uic
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QModelIndex
from PyQt6.QtWidgets import QMainWindow, QTreeView, QMessageBox, QMenu, QCompleter
from PyQt6.QtSql import QSqlTableModel, QSqlRelationalTableModel


from src.inventory_handler import InventoryHandler
from src.proxy_models.inventory_filter_proxy_model import InventoryFilterProxyModel
from src.proxy_models.one_column_table_proxy_model import OneColumnTableProxyModel
from src.proxy_models.unique_items_proxy_model import UniqueItemsProxyModel
from src.sqlite_connector import SqliteConnector
from src.widgets.add_new_item_manually_widget import AddNewItemManuallyWidget
from src.widgets.edit_inventory_item_widget import InventoryEditItem
from src.widgets.add_from_file_inventory_widget import AddFromFileInventoryWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("src/ui/main_window.ui", self)
        self.show()
        self.db_connector = InventoryHandler(database_connector=SqliteConnector)
        self.source_table_model = self._set_up_table_model()
        self.proxy_model = InventoryFilterProxyModel()
        self.proxy_model.setSourceModel(self.source_table_model)

        self.completer_proxy_model = UniqueItemsProxyModel()
        one_column_table_proxy_model = OneColumnTableProxyModel()
        one_column_table_proxy_model.setSourceModel(self.source_table_model)

        self.completer_proxy_model.setSourceModel(one_column_table_proxy_model)

        completer = QCompleter(self.completer_proxy_model)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.ui.inventory_line_edit.setCompleter(completer)
        self.ui.inventory_table_view.setModel(self.proxy_model)
        self.show()

    def _set_up_table_model(self):
        model = QSqlRelationalTableModel(self)
        model.setTable("items")
        model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnRowChange)
        model.select()

        return model

    def inventory_add_from_file_clicked(self):
        print("inventory_add_from_file_clicked")
        inventory_add_from_file = AddFromFileInventoryWidget(self.source_table_model)

    def inventory_add_manually_clicked(self):
        print("inventory_add_manually_clicked")
        add_new_item = AddNewItemManuallyWidget(self.source_table_model)

    def inventory_edit_item(self, model_index):
        print("inventory_table_view")
        # TODO: check if this is needed. Can we have one index?
        source_index = self.proxy_model.mapToSource(model_index)
        inventory_edit = InventoryEditItem(self.source_table_model, source_index)

    def inventory_search_clicked(self):
        print("inventory_search")
        self.proxy_model.filter = self.ui.inventory_line_edit.text()
        self.proxy_model.invalidateFilter()

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
