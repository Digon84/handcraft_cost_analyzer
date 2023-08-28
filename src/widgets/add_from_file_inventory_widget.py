from PyQt6.QtCore import Qt
from PyQt6 import uic
from PyQt6.QtGui import QPalette, QBrush, QColor, QColorConstants
from PyQt6.QtSql import QSqlRelationalTableModel
from PyQt6.QtWidgets import QDialog, QFileDialog, QTableWidget, QTableWidgetItem


class AddFromFileInventoryWidget(QDialog):
    def __init__(self, table_model: QSqlRelationalTableModel):
        super(QDialog, self).__init__()
        self.table_model = table_model
        self.ui = uic.loadUi("src/ui/load_from_file_widget.ui", self)
        self.columns = [self.table_model.headerData(i, Qt.Orientation.Horizontal) for i in
                        range(self.table_model.columnCount())]
        self.add_columns()
        self.add_row()
        # self.get_values()
        self.show()

    def add_columns(self):
        table_widget: QTableWidget = self.ui.tableWidget
        table_widget.setColumnCount(len(self.columns))
        table_widget.setHorizontalHeaderLabels(self.columns)
        print(table_widget.columnCount())
        print(self.columns)

    def add_row(self):
        table_widget: QTableWidget = self.ui.tableWidget
        table_widget.insertRow(table_widget.rowCount())
        table_widget.setItem(table_widget.rowCount()-1, 0, QTableWidgetItem("test"))
        table_widget.item(0, 0).setBackground(QBrush(QColor(QColorConstants.Red)))

    def get_values(self):
        self.table_model.setTable("items")
        self.table_model.setQuery("SELECT distinct(material) FROM items")


    def load_from_file_load_pressed(self):
        file_dialog = QFileDialog()
        if file_dialog.exec():
           filenames = file_dialog.selectedFiles()
           print(f"filenames: {filenames}")
           f = open(filenames[0], 'r')
           with f:
            data = f.read()
            print(f"file loaded: {filenames[0]}")
        print("load_from_file_load_pressed")

    def load_from_file_table_edit(self):
        print("load_from_file_table_edit")

    def load_from_file_text_window_clicked(self):
        file_dialog = QFileDialog()
        if file_dialog.exec():
         filenames = file_dialog.selectedFiles()
         f = open(filenames[0], 'r')
         with f:
            data = f.read()
            self.ui.lineEdit.setText(data)

        print("load_from_file_text_window_clicked")