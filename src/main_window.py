from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QTreeView
from PyQt6.QtSql import QSqlRelationalTableModel


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
        model = QSqlRelationalTableModel(self)
        model.setTable("beads")
        model.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)
        model.setHeaderData(0, Qt.Orientation.Horizontal, "shape")
        model.setHeaderData(1, Qt.Orientation.Horizontal, "type")
        model.setHeaderData(2, Qt.Orientation.Horizontal, "color")
        model.setHeaderData(3, Qt.Orientation.Horizontal, "finishing_effect")
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

