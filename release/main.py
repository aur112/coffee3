import sys
import sqlite3
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QWidget
from mainUI import Ui_MainWindow
from addEditCoffeeForm import Ui_MainWindow2


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sqnames = {
            0: "name",
            1: "roast",
            2: "type",
            3: "description",
            4: "cost",
            5: "size",
        }
        self.loadTable('coffee.sqlite')
        self.tableWidget.cellChanged.connect(self.edit)
        self.add.clicked.connect(self.new)

    def loadTable(self, table_name):
        self.con = sqlite3.connect(table_name)
        self.cur = self.con.cursor()
        info = list(self.cur.execute("""SELECT name, roast, type, description, cost, size FROM coffee""").fetchall())
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['название сорта', 'степень обжарки', 'тип', 'описание вкуса',
                                                    'цена', 'объем упаковки'])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(info):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def edit(self, row, column):
        if column > 3:
            s = """UPDATE coffee SET """ + self.sqnames[column]
            self.cur.execute(s + """= ?
                              WHERE id = ?""", (int(self.tableWidget.item(row, column).text()), row + 1))
            self.con.commit()
        else:
            s = """UPDATE coffee SET """ + self.sqnames[column]
            self.cur.execute(s + """= ?
                  WHERE id = ?""", (self.tableWidget.item(row, column).text(), row + 1))
            self.con.commit()

    def new(self):
        self.add = Add()
        self.add.show()


class Add(QMainWindow, Ui_MainWindow2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_new)

    def add_new(self):
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        s = len(self.cur.execute("""SELECT * FROM coffee""").fetchall())
        self.cur.execute("""INSERT INTO coffee(id, name, roast, type, description, cost, size) 
                                            VALUES(?, ?, ?, ?, ?, ?, ?)""", (s + 1, self.lineEdit_2.text(),
                                        self.lineEdit_3.text(), self.lineEdit_4.text(), self.lineEdit_5.text(),
                                                            self.lineEdit_6.text(), self.lineEdit_7.text()))
        self.con.commit()
        ex.loadTable('coffee.sqlite')
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())