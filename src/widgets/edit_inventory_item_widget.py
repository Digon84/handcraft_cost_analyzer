from PyQt6 import uic
from PyQt6.QtWidgets import QDialog


class InventoryEditItem(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("src/ui/edit_inventory_item_widget.ui", self)
        self.show()
