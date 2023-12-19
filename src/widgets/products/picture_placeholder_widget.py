import os
import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg


class PicturePlaceholderWidget(qtw.QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # code here
        self.filename = self.get_image_path("plus.png")
        self.setPixmap(qtg.QPixmap(self.filename))
        self.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)

        self.setFrameShape(qtw.QFrame.Shape.Box)
        self.setFrameShadow(qtw.QFrame.Shadow.Plain)
        self.setLineWidth(1)
        self.setMinimumWidth(250)
        # end of code

    def mousePressEvent(self, event: qtg.QMouseEvent):
        if self.filename == self.get_image_path("plus.png"):
            file_dialog = qtw.QFileDialog()
            if file_dialog.exec():
                filenames = file_dialog.selectedFiles()
                if filenames:
                    self.filename = filenames[-1]
                    self.set_image(self.filename)

    def set_image(self, image_name):
        self.filename = image_name
        self.setPixmap(qtg.QPixmap(image_name))
        self.setScaledContents(True)
        self.setSizePolicy(qtw.QSizePolicy.Policy.Ignored, qtw.QSizePolicy.Policy.Ignored)

    @staticmethod
    def get_image_path(image_file_name):
        absolute_path = os.path.dirname(__file__)
        image_relative_path = os.path.join("..", "..", "..", "assets", "pictures", image_file_name)
        return os.path.join(absolute_path, image_relative_path)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = PicturePlaceholderWidget()
    w.show()
    sys.exit(app.exec())
