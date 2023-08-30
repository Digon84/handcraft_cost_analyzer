from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
from src.widgets.main_window import MainWindow

app = QApplication(sys.argv)

window = MainWindow()

app.exec()
