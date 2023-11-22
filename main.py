from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
import os
from src.widgets.main_window import MainWindow

os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"

app = QApplication(sys.argv)

window = MainWindow()

app.exec()
