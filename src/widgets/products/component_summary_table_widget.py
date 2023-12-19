import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg

from src.database.dao.component_dao import ComponentDAO


class ComponentSummaryTableWidget(qtw.QTableWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # code here
        self.component_dao = ComponentDAO()
        self.context_menu = self.create_context_menu()
        self.set_table()
        # end of code

    def set_table(self):
        # component = material + type + color
        self.setColumnCount(4)
        self.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeMode.Stretch)
        self.setHorizontalHeaderLabels(["component", "amount", "unit_price", "total_price"])

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

    def add_action_triggered(self):
        print("add_action_triggered")

    def delete_action_triggered(self):
        print("delete_action_triggered")

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = ComponentSummaryTableWidget()
    w.show()
    sys.exit(app.exec())
