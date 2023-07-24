from PyQt6.QtWidgets import QApplication, QMainWindow

import sys



from src.main_window import MainWindow

app = QApplication(sys.argv)


# app.setApplicationName("Handcraft cost analyzer")
# app.setApplicationDisplayName("Handcraft cost analyzer")


window = MainWindow()



# db_connector.add_bead(100)
# db_connector.add_bead(150)
app.exec()
