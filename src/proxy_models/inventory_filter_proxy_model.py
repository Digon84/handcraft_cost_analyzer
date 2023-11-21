from PyQt6.QtCore import QSortFilterProxyModel, QModelIndex


class InventoryFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filter = ""

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        if self.filter != "":
            filter_elements = self.filter.split(" ")
            matched_elements = 0
            elements = []
            # TODO: skip columns with indexes, make it easier to maintain
            for column in range(2, self.sourceModel().columnCount()):
                first_column_index = self.sourceModel().index(source_row, column, source_parent)
                element = str(self.sourceModel().data(first_column_index))
                elements.append(element)
                for filter_element in filter_elements:
                    if filter_element in str(self.sourceModel().data(first_column_index)):
                        matched_elements += 1
                if matched_elements == len(filter_elements):
                    return True
                else:
                    continue
        else:
            return True
        return False

    def setSourceModel(self, source_model):

        super().setSourceModel(source_model)
