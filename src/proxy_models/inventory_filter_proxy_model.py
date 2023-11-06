from PyQt6.QtCore import QSortFilterProxyModel, QModelIndex


class InventoryFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter = ""

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        print(f"filterAcceptsRow {self.sourceModel().rowCount()}")
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

    def setSourceModel(self, source_model):

        super().setSourceModel(source_model)
        self.sourceModel().dataChanged.connect(self.test_method)

    def test_method(self, top, low):
        print(f"data changed :) {top} {low}")


