from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QFileDialog

class AddFromFileInventoryWidget(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("src/ui/load_from_file_widget.ui", self)
        self.show()

    def load_from_file_load_pressed(self):
        file_dialog = QFileDialog()
        if file_dialog.exec():
           filenames = file_dialog.selectedFiles()
           print(f"filenames: {filenames}")
           f = open(filenames[0], 'r')
           with f:
            data = f.read()
            print(f"file loaded: {filenames[0]}")
        print("load_from_file_load_pressed")

    def load_from_file_table_edit(self):
        print("load_from_file_table_edit")

    def load_from_file_text_window_clicked(self):
        file_dialog = QFileDialog()
        if file_dialog.exec():
         filenames = file_dialog.selectedFiles()
         f = open(filenames[0], 'r')
			
         with f:
            data = f.read()
            self.ui.lineEdit.setText(data)

        print("load_from_file_text_window_clicked")