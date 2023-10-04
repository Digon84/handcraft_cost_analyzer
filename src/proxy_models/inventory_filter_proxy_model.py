from PyQt6.QtCore import QSortFilterProxyModel, QModelIndex


class InventoryFilterProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.filter = ""

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        if self.filter != "":
            for column in range(self.sourceModel().columnCount()):
                first_column_index = self.sourceModel().index(source_row, column, source_parent)
                if self.filter in str(self.sourceModel().data(first_column_index)):
                    return True
                else:
                    continue
        else:
            return True
        return False
