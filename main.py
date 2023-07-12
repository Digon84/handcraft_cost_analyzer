from PyQt6.QtWidgets import QApplication, QMainWindow

import sys

app = QApplication(sys.argv)


app.setApplicationName("Handcraft cost analyzer")
app.setApplicationDisplayName("Handcraft cost analyzer")

window = QMainWindow()
window.show()

app.exec()
