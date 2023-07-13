from PyQt6.QtWidgets import QApplication, QMainWindow

import sys

from src.database_connector import DataBaseConnector

app = QApplication(sys.argv)


app.setApplicationName("Handcraft cost analyzer")
app.setApplicationDisplayName("Handcraft cost analyzer")



window = QMainWindow()
window.show()

db_connector = DataBaseConnector()
db_connector.open_connection()

app.exec()


