from PyQt6.QtWidgets import QApplication, QMainWindow

import sys

from src.inventory_handler import InventoryHandler
from src.sqlite_connector import SqliteConnector

app = QApplication(sys.argv)


app.setApplicationName("Handcraft cost analyzer")
app.setApplicationDisplayName("Handcraft cost analyzer")


window = QMainWindow()
window.show()

db_connector = InventoryHandler(database_connector=SqliteConnector)
db_connector.add_bead(100)
db_connector.add_bead(150)
app.exec()
