from .inventory_item_widget import InventoryItemWidget


class AddNewItemManuallyWidget(InventoryItemWidget):
    def __init__(self, table_model):
        super().__init__(table_model)

        self.exec()
