import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg

from src.database.dao.component_dao import ComponentDAO
from src.entities.inventory import Inventory
from src.widgets.products.add_component_widget import AddComponentWidget


class ComponentSummaryTableWidget(qtw.QTableWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # code here
        self.initiated = False
        self.component_dao = ComponentDAO()
        self.context_menu = self.create_context_menu()
        self.set_table()
        # end of code

    def set_table(self):
        self.setColumnCount(5)
        self.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeMode.Stretch)
        self.setHorizontalHeaderLabels(["component", "amount", "unit_price", "total_price", "component_id"])
        self.cellChanged.connect(self.cell_changed_triggered)
        # self.hideColumn(4)

    def create_context_menu(self):
        context_menu = qtw.QMenu(self)

        add_action = qtg.QAction("Add item", self)
        add_action.setText("Add item")
        add_action.setToolTip("Add item to components summary")
        add_action.triggered.connect(self.add_action_triggered)

        delete_action = qtg.QAction("Delete item", self)
        delete_action.setText("Delete item")
        delete_action.setToolTip("Delete item from components summary")
        delete_action.triggered.connect(self.delete_action_triggered)

        context_menu.addAction(add_action)
        context_menu.addAction(delete_action)

        return context_menu

    def contextMenuEvent(self, event):
        print("contextMenuEvent")
        self.context_menu.popup(qtg.QCursor.pos())

    def store_components_in_table(self, inventory_list: list[Inventory], amount: str):
        for inventory in inventory_list:
            self.insertRow(self.rowCount())
            next_item = self.rowCount() - 1
            component_short_name = " ".join([inventory.component.material,
                                             inventory.component.type,
                                             inventory.component.color])

            # component
            item = qtw.QTableWidgetItem(component_short_name)
            item.setFlags(item.flags() ^ qtc.Qt.ItemFlag.ItemIsEditable)
            self.setItem(next_item, 0, item)

            # amount
            self.setItem(next_item, 1, qtw.QTableWidgetItem(str(amount)))

            # unit_price
            item = qtw.QTableWidgetItem(str(round(inventory.unit_price, 3)))
            item.setFlags(item.flags() ^ qtc.Qt.ItemFlag.ItemIsEditable)
            self.setItem(next_item, 2, item)

            # total_price
            item = qtw.QTableWidgetItem(str(round(inventory.unit_price * int(amount), 3)))
            item.setFlags(item.flags() ^ qtc.Qt.ItemFlag.ItemIsEditable)
            self.setItem(next_item, 3, item)

            # component_id
            item = qtw.QTableWidgetItem(str(inventory.component_id))
            item.setFlags(item.flags() ^ qtc.Qt.ItemFlag.ItemIsEditable)
            self.setItem(next_item, 4, item)
        self.initiated = True

    def add_action_triggered(self):
        self.add_component_widget = AddComponentWidget()
        self.add_component_widget.components_selected.connect(self.store_components_in_table)
        self.add_component_widget.show()

    def delete_action_triggered(self):
        row_indexes = list(set([index.row() for index in self.selectedIndexes()]))
        row_indexes.sort(reverse=True)
        for row_index in row_indexes:
            self.removeRow(row_index)

    def cell_changed_triggered(self, row: int, column: int):
        if self.initiated:
            # amount
            if column == 1:
                amount = float(self.item(row, column).text())
                unit_price = float(self.item(row, 2).text())
                self.item(row, 3).setText(str(round(amount * unit_price, 3)))


    def keyPressEvent(self, event):
        if event.key() == qtc.Qt.Key.Key_Delete:
            self.delete_action_triggered()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = ComponentSummaryTableWidget()
    w.show()
    sys.exit(app.exec())
