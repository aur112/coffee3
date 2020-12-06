import sys
from random import randrange
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.b = False
        self.pushButton.clicked.connect(self.circles)

    def circles(self):
        self.b = True
        self.update()

    def paintEvent(self, event):
        if self.b:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            for i in range(20):
                painter.setBrush(
                    QBrush(QColor(randrange(0, 255), randrange(0, 255), randrange(0, 255)), Qt.SolidPattern))
                r = randrange(5, 50)
                painter.drawEllipse(randrange(0, self.width()), randrange(0, self.height()), r, r)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())