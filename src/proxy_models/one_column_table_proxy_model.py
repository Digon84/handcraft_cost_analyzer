import typing

from PyQt6.QtCore import QAbstractProxyModel, QModelIndex, QObject, Qt


class OneColumnTableProxyModel(QAbstractProxyModel):
    def __init__(self):
        super().__init__()

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        return self.createIndex(row, 0)

    def parent(self, index) -> QModelIndex:
        return QModelIndex()

    def columnCount(self, parent: QModelIndex = ...) -> int:
        if self.sourceModel() is None or parent.isValid():
            return 0
        return 1

    def rowCount(self, parent: QModelIndex = ...) -> int:
        if self.sourceModel() is None or parent.isValid():
            return 0
        return self.sourceModel().rowCount() * self.sourceModel().columnCount()

    def mapToSource(self, proxy_index: QModelIndex) -> QModelIndex:
        if not proxy_index.isValid():
            return QModelIndex()
        source_column = proxy_index.row() % self.sourceModel().columnCount()
        source_row = (proxy_index.row() - source_column) // self.sourceModel().columnCount()

        return self.sourceModel().index(source_row, source_column)

    def mapFromSource(self, source_index: QModelIndex) -> QModelIndex:
        if not source_index.isValid():
            return QModelIndex()
        proxy_row = source_index.row() * (self.sourceModel().columnCount() - 1) + source_index.column()

        return self.index(proxy_row, 0)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return "One column proxy"
        elif orientation == Qt.Orientation.Vertical and role == Qt.ItemDataRole.DisplayRole:
            return section
        return super().headerData(section, orientation, role)
