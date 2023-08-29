from typing import List

from PyQt6.QtCore import Qt
from PyQt6 import uic
from PyQt6.QtGui import QBrush, QColor, QColorConstants
from PyQt6.QtSql import QSqlRelationalTableModel, QSqlQuery
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
        for column in self.columns:
            print(self.get_distinct_values_for_column(column))
        self.show()

    def add_columns(self):
        table_widget: QTableWidget = self.ui.tableWidget
        table_widget.setColumnCount(len(self.columns))
        table_widget.setHorizontalHeaderLabels(self.columns)

    def add_row(self):
        table_widget: QTableWidget = self.ui.tableWidget
        table_widget.insertRow(table_widget.rowCount())
        table_widget.setItem(table_widget.rowCount()-1, 0, QTableWidgetItem("test"))
        table_widget.item(0, 0).setBackground(QBrush(QColor(QColorConstants.Red)))

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

    @staticmethod
    def get_distinct_values_for_column(column_name) -> List:
        result = []
        sql_select_query = QSqlQuery()
        sql_select_query.exec(f"SELECT distinct({column_name}) FROM items")
        while sql_select_query.next():
            result.append(sql_select_query.value(0))
        return result
