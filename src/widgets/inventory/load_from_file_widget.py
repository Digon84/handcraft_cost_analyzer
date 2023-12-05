from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg

from src.entities.inventory import Inventory
from src.database.dao.component_dao import ComponentDAO
from src.database.dao.inventory_dao import InventoryDAO
from src.file_operations.parsers.file_parser import Parsed, Row
from src.file_operations.parsers.shopping_summary_parser import ShoppingSummaryParser
from src.proxy_models.unique_items_proxy_model import UniqueItemsProxyModel


class LoadFromFileWidget(qtw.QWidget):

    submitted = qtc.pyqtSignal(list)

    def __init__(self, columns_mapping, source_table_model):
        super().__init__()
        self.shopping_summary_parser = ShoppingSummaryParser()
        self.source_table_model = source_table_model
        self.component_dao = ComponentDAO()
        self.inventory_dao = InventoryDAO()
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
        self.table.itemChanged.connect(self.set_unit_price)
        self.add_columns()

    def setup_buttons(self):
        self.load_button = qtw.QPushButton('Load')
        self.load_button.setFixedSize(qtc.QSize(120, 25))
        self.ok_button = qtw.QPushButton('Ok')
        self.ok_button.setFixedSize(qtc.QSize(120, 25))
        self.cancel_button = qtw.QPushButton('Cancel')
        self.cancel_button.setFixedSize(qtc.QSize(120, 25))

    def setup_window(self):
        self.resize(qtc.QSize(1270, 600))
        self.setWindowTitle("Load from file")

    def add_columns(self):
        table_widget: qtw.QTableWidget = self.table
        table_widget.setColumnCount(len(self.columns_mapping))
        table_widget.setHorizontalHeaderLabels(self.columns_mapping.keys())

    def add_row(self, row: Row) -> int:
        table_widget: qtw.QTableWidget = self.table
        table_widget.insertRow(table_widget.rowCount())
        for parsed_item in row.parsed_items.values():
            next_item = table_widget.rowCount()-1
            column_number = self.columns_mapping[parsed_item.column_name]
            table_item = qtw.QTableWidgetItem(str(parsed_item.value))
            if parsed_item.parsed_ok == Parsed.NOK:
                table_item.setBackground(qtg.QBrush(qtg.QColor(qtg.QColorConstants.Red)))
            elif parsed_item.parsed_ok == Parsed.CONDITIONAL:
                table_item.setBackground(qtg.QBrush(qtg.QColor(qtg.QColorConstants.Yellow)))
            if parsed_item.column_name == "unit_price":
                total_price = row.parsed_items["total_price"].value
                amount = row.parsed_items["amount"].value
                if total_price and amount:
                    table_item.setText(str(round(float(total_price) / float(amount), 3)))
                flags = table_item.flags() & ~qtc.Qt.ItemFlag.ItemIsEnabled
                table_item.setFlags(flags)

            table_widget.setItem(next_item, column_number, table_item)

        return table_widget.rowCount()-1

    def add_parsing_result_row(self, hint):
        table_widget: qtw.QTableWidget = self.table
        table_widget.insertRow(table_widget.rowCount())
        next_item = table_widget.rowCount() - 1

        table_widget.setSpan(next_item, 0, 1, table_widget.columnCount())
        parsing_row = qtw.QTableWidgetItem(hint)
        parsing_row.setFlags(parsing_row.flags() & ~qtc.Qt.ItemFlag.ItemIsEnabled)
        table_widget.setItem(next_item, 0, parsing_row)

        table_widget.resizeRowsToContents()

        return table_widget.rowCount()

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
            self.add_parsing_result_row(row.hint)
            _ = self.add_row(row)

        completer = TableItemCompleter(self.source_table_model)
        for column in self.columns_mapping.values():
            self.table.setItemDelegateForColumn(column, completer)

        self.first_table_fill = False

    def on_submit(self):
        table_content = []
        for i in range(1, self.table.rowCount(), 2):
            row = {}
            for j in range(self.table.columnCount()):
                row[self.table.horizontalHeaderItem(j).text()] = self.table.item(i, j).text()
            table_content.append(Inventory(row))

        self.submitted.emit(table_content)
        self.close()

    def keyPressEvent(self, event):
        if event.modifiers() & qtc.Qt.KeyboardModifier.ControlModifier:
            if event.key() == qtc.Qt.Key.Key_V:
                clipboard_text = qtg.QGuiApplication.clipboard().text()
                if clipboard_text:
                    for selected_index in self.table.selectedIndexes():
                        self.table.item(selected_index.row(), selected_index.column()).setText(clipboard_text)
            elif event.key() == qtc.Qt.Key.Key_D:
                selected_indexes = self.table.selectedIndexes()
                if selected_indexes and len(selected_indexes) == 1:
                    index = selected_indexes[-1]
                    row = index.row()
                    column = index.column()
                    if row >= 2:
                        data = self.table.item(row - 2, column).text()
                        self.table.item(row, column).setText(data)
        # if event.key() == qtc.Qt.Key.Key_Up:
        #     selected_indexes = self.table.selectedIndexes()
        #     if selected_indexes and len(selected_indexes) == 1:
        #         index = selected_indexes[-1]
        #         row = index.row()
        #         column = index.column()
        #         item_currently_selected = self.table.item(row, column)
        #         item = self.table.item(row - 2, column)
        #         if item:
        #             item.setSelected(True)
        #             self.table.scrollToItem(item)
        #             if item_currently_selected:
        #                 item_currently_selected.setSelected(False)
        # elif event.key() == qtc.Qt.Key.Key_Down:
        #     selected_indexes = self.table.selectedIndexes()
        #     if selected_indexes and len(selected_indexes) == 1:
        #         index = selected_indexes[-1]
        #         row = index.row()
        #         column = index.column()
        #         item_currently_selected = self.table.item(row, column)
        #         item = self.table.item(row + 2, column)
        #         if item:
        #             item.setSelected(True)
        #             self.table.scrollToItem(item)
        #             if item_currently_selected:
        #                 item_currently_selected.setSelected(False)

    def set_unit_price(self, item_changed: qtw.QTableWidgetItem):
        item_changed_row = item_changed.row()
        item_changed_column = item_changed.column()

        if item_changed_column == 9 or item_changed_column == 7:
            # TODO: fix hardcodes
            total_price = self.table.item(item_changed_row, 9).text() if self.table.item(item_changed_row, 9) else ""
            amount = self.table.item(item_changed_row, 7).text() if self.table.item(item_changed_row, 7) else ""

            if total_price and amount:
                unit_price_item = self.table.item(item_changed_row, 8)
                unit_price_item.setText(str(round(float(total_price) / float(amount), 3)))


class TableItemCompleter(qtw.QStyledItemDelegate):
    def __init__(self, source_table_model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source_table_model = source_table_model

    def createEditor(self, parent, option, index):
        editor = qtw.QLineEdit(parent)
        # TODO: get rid of hardcodes. column + 2 since we are ignoring inventory_id and component_id
        auto_completer = self.get_completer(index.column() + 2)
        editor.setCompleter(auto_completer)
        return editor

    def get_completer(self, column):
        completer_proxy_model = UniqueItemsProxyModel(self)
        completer_proxy_model.setSourceModel(self.source_table_model)
        completer_proxy_model.setFilterKeyColumn(column)
        completer_proxy_model.set_desired_column(column)
        completer = qtw.QCompleter(completer_proxy_model)
        completer.setCaseSensitivity(qtc.Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionColumn(column)

        return completer
