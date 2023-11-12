import sys
from typing import List

from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg

from src.parsers.file_parser import ParsedItem, Parsed
from src.parsers.shopping_summary_parser import ShoppingSummaryParser


class LoadFromFileWidget(qtw.QWidget):

    submitted = qtc.pyqtSignal(list)

    def __init__(self, columns_mapping):
        super().__init__()
        self.shopping_summary_parser = ShoppingSummaryParser()

        self.setup_window()
        self.setup_table(columns_mapping)
        self.setup_buttons()

        layout = self.setup_layout()

        self.cancel_button.clicked.connect(self.close)
        self.ok_button.clicked.connect(self.on_submit)
        self.load_button.clicked.connect(self.load_button_clicked)
        self.table.cellChanged.connect(self.cell_content_changed)

        self.setLayout(layout)

    def setup_layout(self):
        layout = qtw.QFormLayout()
        layout.addWidget(self.table)
        button_widget = qtw.QWidget()
        button_widget.setLayout(qtw.QHBoxLayout())
        button_widget.layout().addWidget(self.load_button)
        button_widget.layout().addStretch(1)
        button_widget.layout().addWidget(self.ok_button)
        button_widget.layout().addWidget(self.cancel_button)

        layout.addRow('', button_widget)
        return layout

    def setup_table(self, columns_mapping):
        self.columns_mapping = columns_mapping
        self.first_table_fill = True
        self.table = qtw.QTableWidget()
        self.add_columns()

    def setup_buttons(self):
        self.load_button = qtw.QPushButton('Load')
        self.load_button.setFixedSize(qtc.QSize(120, 25))
        self.ok_button = qtw.QPushButton('Ok')
        self.ok_button.setFixedSize(qtc.QSize(120, 25))
        self.cancel_button = qtw.QPushButton('Cancel')
        self.cancel_button.setFixedSize(qtc.QSize(120, 25))

    def setup_window(self):
        self.resize(qtc.QSize(1250, 600))
        self.setWindowTitle("Load from file")

    def add_columns(self):
        table_widget: qtw.QTableWidget = self.table
        table_widget.setColumnCount(len(self.columns_mapping))
        table_widget.setHorizontalHeaderLabels(self.columns_mapping.keys())

    def add_row(self, row: dict):
        table_widget: qtw.QTableWidget = self.table
        table_widget.insertRow(table_widget.rowCount())
        for parsed_item in row.values():
            next_item = table_widget.rowCount()-1
            column_number = self.columns_mapping[parsed_item.column_name]
            table_widget.setItem(next_item, column_number, qtw.QTableWidgetItem(str(parsed_item.value)))
            if parsed_item.parsed_ok == Parsed.NOK:
                table_widget.item(next_item, column_number).setBackground(
                    qtg.QBrush(qtg.QColor(qtg.QColorConstants.Red)))
            elif parsed_item.parsed_ok == Parsed.CONDITIONAL:
                table_widget.item(next_item, column_number).setBackground(
                    qtg.QBrush(qtg.QColor(qtg.QColorConstants.Yellow)))

    def cell_content_changed(self, row, column):
        if not self.first_table_fill:
            table_widget: qtw.QTableWidget = self.table
            table_widget.item(row, column).setBackground(qtg.QBrush(qtg.QColor(qtg.QColorConstants.Yellow)))

    def load_button_clicked(self):
        self.first_table_fill = True
        file_dialog = qtw.QFileDialog()
        file_dialog.setFileMode(qtw.QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("*.txt *.csv")
        parsed_items = []
        if file_dialog.exec():
            filenames = file_dialog.selectedFiles()
            for file in filenames:
                parsed_items.extend(self.shopping_summary_parser.parse_file(file))
        for row in parsed_items:
            self.add_row(row)
        self.first_table_fill = False

    def on_submit(self):
        table_content = []
        for i in range(self.table.rowCount()):
            row = []
            for j in range(self.table.columnCount()):
                row.append((self.table.horizontalHeaderItem(j).text(), self.table.item(i, j).text()))
            table_content.append(row)

        self.submitted.emit(table_content)
        self.close()

    def keyPressEvent(self, event):
        if event.modifiers() & qtc.Qt.KeyboardModifier.ControlModifier:
            if event.key() == qtc.Qt.Key.Key_V:
                clipboard_text = qtg.QGuiApplication.clipboard().text()
                if clipboard_text:
                    for selected_index in self.table.selectedIndexes():
                        self.table.item(selected_index.row(), selected_index.column()).setText(clipboard_text)


