import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg


class AddComponentWidget(qtw.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # code here

        # end of code


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = AddComponentWidget()
    w.show()
    sys.exit(app.exec())
