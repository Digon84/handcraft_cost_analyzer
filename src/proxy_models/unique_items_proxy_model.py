from PyQt6.QtCore import QSortFilterProxyModel, QModelIndex


class UniqueItemsProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.column = None
        self.unique_items = []

    def set_desired_column(self, column):
        self.column = column

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        first_column_index = self.sourceModel().index(source_row, self.column, source_parent)
        if str(self.sourceModel().data(first_column_index)) not in self.unique_items:
            self.unique_items.append(str(self.sourceModel().data(first_column_index)))
            return True
        return False
