from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QTreeView, QMessageBox
from PyQt6.QtSql import QSqlTableModel


from src.inventory_handler import InventoryHandler
from src.sqlite_connector import SqliteConnector


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.setWindowTitle("Handcraft cost analyzer")
        # self.resize(1200, 600)
        self.ui = uic.loadUi("src/main_window.ui", self)
        self.show()
        self.db_connector = InventoryHandler(database_connector=SqliteConnector)
        self.table_model = self._set_up_table_model()
        self.ui.tableView.setModel(self.table_model)
        # self.ui.treeView.setModel(self.model)
        self.show()
        # self.view = self._set_up_view()

    
    def _set_up_table_model(self):
        model = QSqlTableModel(self)
        model.setTable("beads")
        model.setEditStrategy(QSqlTableModel.EditStrategy.OnRowChange)
        model.select()
        
        return model
    
    def _set_up_tree_model(self):
        pass
    
    def _set_up_view(self):
        view = QTreeView()
        view.setModel(self.model)
        # view.resizeColumnsToContents()
        self.setCentralWidget(view)
        return view


    def edit_on_double_click(self, model_index):
        print(f"modelIndex.row(): {model_index.row()}")


    def delete_selected_row(self, model_index):
        print("delete")


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setText("Usunąć element?")
            msg.setInformativeText("Ta operacja usunie element z bazy danych na stałe. Czy kontunuowac?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
            msg.exec()
            
            

            if self.ui.tableView.selectedIndexes():
                index = self.ui.tableView.selectedIndexes()[0]
                self.table_model.removeRow(index.row())
                self.table_model.submitAll()
                self.table_model.select()

    def manualAddItem(self):
        print("Manual add placeholder")
        self.table_model.select()

    def loadFromFile(self):
        print("Load from file placeholder")
