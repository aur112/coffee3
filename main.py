import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.loadTable('coffee.sqlite')

    def loadTable(self, table_name):
        con = sqlite3.connect(table_name)
        cur = con.cursor()
        info = list(cur.execute("""SELECT * FROM coffee""").fetchall())
        print(info)
        for i in range(len(info)):
            info[i] = list(info[i])
            info[i][1] = cur.execute("""SELECT name FROM sorts
                                    WHERE id=?""", (info[i][1],)).fetchone()[0]
            info[i][2] = cur.execute("""SELECT roast FROM roast_degree
                                                WHERE id=?""", (info[i][2],)).fetchone()[0]
            info[i][3] = cur.execute("""SELECT type FROM type
                                                            WHERE id=?""", (info[i][3],)).fetchone()[0]
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'название сорта', 'степень обжарки', 'тип', 'описание вкуса',
                                                    'цена', 'объем упаковки'])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(info):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())