from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QDataWidgetMapper, QDialogButtonBox, QVBoxLayout, QLabel, QGridLayout, QLineEdit


class InventoryEditItem(QDialog):
    def __init__(self, table_model, model_index):
        super().__init__()
        self.table_model = table_model
        self.model_index = model_index
        self.mapper = QDataWidgetMapper(self)

        self.draw_widget()
        # self.ui = uic.loadUi("src/ui/edit_inventory_item_widget.ui", self)

        #



        # self.mapper.setModel(table_model)
        # self.mapper.addMapping(self.ui.matherial_line_edit, table_model.fieldIndex("material"))
        # self.mapper.addMapping(self.ui.type_line_edit, table_model.fieldIndex("type"))
        # self.mapper.addMapping(self.ui.shape_line_edit, table_model.fieldIndex("shape"))
        # self.mapper.addMapping(self.ui.color_line_edit, table_model.fieldIndex("color"))
        # self.mapper.addMapping(self.ui.finishing_effect_line_edit, table_model.fieldIndex("finishing_effect"))
        # self.mapper.addMapping(self.ui.size_line_edit, table_model.fieldIndex("size"))
        # self.mapper.addMapping(self.ui.amount_line_edit, table_model.fieldIndex("amount"))
        # self.mapper.addMapping(self.ui.other_line_edit, table_model.fieldIndex("other"))
        # self.mapper.addMapping(self.ui.unit_price_line_edit, table_model.fieldIndex("unit_price"))
        # self.mapper.addMapping(self.ui.total_price_line_edit, table_model.fieldIndex("total_price"))


        self.exec()

    def draw_widget(self):
        self.setWindowTitle("Update item")
        q_btn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        button_box = QDialogButtonBox(q_btn)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        grid_layout = QGridLayout()
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.table_model)

        for i in range(self.table_model.columnCount()):
            column_name = self.table_model.headerData(i, Qt.Orientation.Horizontal)
            print(column_name)

            label = QLabel(column_name)
            line_edit = QLineEdit()

            grid_layout.addWidget(label, i, 0)
            grid_layout.addWidget(line_edit, i, 1)
            self.mapper.addMapping(line_edit, self.table_model.fieldIndex(column_name))
            self.setLayout(grid_layout)

        self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.ManualSubmit)
        self.mapper.setCurrentModelIndex(self.model_index)
        # layout = QVBoxLayout()
        # layout.addWidget(button_box)
        # self.setLayout(layout)

    def accept(self):
        print("accept")
        # self.mapper.submit()
        super().accept()
