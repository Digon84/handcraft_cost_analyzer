from typing import List

from PyQt6.QtCore import Qt
from PyQt6 import uic
from PyQt6.QtGui import QBrush, QColor, QColorConstants
from PyQt6.QtSql import QSqlRelationalTableModel, QSqlQuery
from PyQt6.QtWidgets import QDialog, QFileDialog, QTableWidget, QTableWidgetItem

from src.parsers.shopping_summary_parser import ShoppingSummaryParser
from src.parsers.file_parser import ParsedItem


# TODO: make connection to main window - right now when main window is closed this window remains
class AddFromFileInventoryWidget(QDialog):
    def __init__(self, table_model: QSqlRelationalTableModel):
        super(QDialog, self).__init__()
        self.table_model = table_model
        self.first_table_fill = True
        self.ui = uic.loadUi("src/ui/load_from_file_widget.ui", self)
        self.columns_mapping = {self.table_model.headerData(i, Qt.Orientation.Horizontal): i for i in
                                range(self.table_model.columnCount())}
        print(self.columns_mapping)
        self.shopping_summary_parser = ShoppingSummaryParser()
        self.add_columns()

        # for column in self.columns:
        #     print(self.get_distinct_values_for_column(column))
        self.show()

    def add_columns(self):
        table_widget: QTableWidget = self.ui.tableWidget
        table_widget.setColumnCount(len(self.columns_mapping))
        table_widget.setHorizontalHeaderLabels(self.columns_mapping.keys())

    def add_row(self, parsed_items: List[ParsedItem]):
        table_widget: QTableWidget = self.ui.tableWidget
        table_widget.insertRow(table_widget.rowCount())
        for parsed_item in parsed_items:
            next_item = table_widget.rowCount()-1
            column_number = self.columns_mapping[parsed_item.column_name]
            table_widget.setItem(next_item, column_number, QTableWidgetItem(str(parsed_item.value)))
            if not parsed_item.parsed_ok:
                table_widget.item(next_item, column_number).setBackground(QBrush(QColor(QColorConstants.Red)))

    def load_from_file_load_pressed(self):
        self.first_table_fill = True
        file_dialog = QFileDialog()
        parsed_items = []
        if file_dialog.exec():
            filenames = file_dialog.selectedFiles()
            print(f"filenames: {filenames}")
            for file in filenames:
                parsed_items.extend(self.shopping_summary_parser.parse_file(file))
        for parsed_item in parsed_items:
            self.add_row(parsed_item)
        self.first_table_fill = False

    def load_from_file_table_edit(self):
        print("load_from_file_table_edit")

    def cell_content_changed(self, row, column):
        if not self.first_table_fill:
            table_widget: QTableWidget = self.ui.tableWidget
            table_widget.item(row, column).setBackground(QBrush(QColor(QColorConstants.Yellow)))

    def accept(self):
        table_widget: QTableWidget = self.ui.tableWidget

        row_count = table_widget.rowCount()
        column_count = table_widget.columnCount()

        if row_count > 0:
            for i in range(row_count):
                record = self.table_model.record()
                for j in range(column_count):
                    # TODO: to make it work I needed to change add_date to NOT NULL, in other cases 2 rows were added -
                    #  one with date and one without. Check how it can be handled in the code
                    record.setValue(table_widget.horizontalHeaderItem(j).text(), table_widget.item(i, j).text())
                    self.table_model.insertRecord(-1, record)
            self.table_model.select()
        super().accept()

    # TODO: remove?
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
