from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QTreeView, QMessageBox, QMenu
from PyQt6.QtSql import QSqlTableModel, QSqlRelationalTableModel


from src.inventory_handler import InventoryHandler
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
        self.table_model = self._set_up_table_model()
        self.ui.inventory_table_view.setModel(self.table_model)
        self.show()

    def _set_up_table_model(self):
        model = QSqlRelationalTableModel(self)
        model.setTable("items")
        model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnRowChange)
        model.select()

        return model

    def _set_up_tree_model(self):
        pass

    def _set_up_view(self):
        view = QTreeView()
        view.setModel(self.model)
        self.setCentralWidget(view)

        return view

    def inventory_add_from_file_clicked(self):
        print("inventory_add_from_file_clicked")
        inventory_add_from_file = AddFromFileInventoryWidget(self.table_model)

    def inventory_add_manually_clicked(self):
        print("inventory_add_manually_clicked")
        add_new_item = AddNewItemManuallyWidget(self.table_model)
        

    def inventory_edit_item(self, model_index):
        print("inventory_table_view")
        inventory_edit = InventoryEditItem(self.table_model, model_index)
        

    def inventory_search_clicked(self):
        print("inventory_search")

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
                self.table_model.removeRow(index.row())
                self.table_model.submitAll()
                self.table_model.select()
