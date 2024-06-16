import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from ui import Ui_MainWindow
import sys

con = sqlite3.connect("base.db")
curs = con.cursor()
app = QApplication(sys.argv)
window = QMainWindow()

ui = Ui_MainWindow()
ui.setupUi(window)

window.show()

ui.label.setVisible(False)
curs.execute("select * from personal")
res = curs.fetchall()
print(res)
ui.tableWidget.setRowCount(len(res))
ui.tableWidget.setColumnCount(len(res[0])-1)
for row in range(len(res)):
    for col in range(len(res[0])-1):
        ui.tableWidget.setItem(row, col, QTableWidgetItem(str(res[row][col+1])))

ui.tableWidget.setHorizontalHeaderLabels(['email', 'username', 'password'])
ui.tableWidget.setColumnWidth(0, ui.tableWidget.width()//3-8)
ui.tableWidget.setColumnWidth(1, ui.tableWidget.width()//3-8)
ui.tableWidget.setColumnWidth(2, ui.tableWidget.width()//3)

print(str(ui.tableWidget.item(1, 1).text()), str(ui.tableWidget.item(1, 2).text()))

def save():
    try:
        curs.execute("select * from personal")
        res = curs.fetchall()
        if ui.tableWidget.rowCount() > len(res):
            for i in range(len(res)):
                curs.execute("update personal set email = ?, username = ?, password = ? where id = ? ", (str(ui.tableWidget.item(i, 0).text()), str(ui.tableWidget.item(i, 1).text()), str(ui.tableWidget.item(i, 2).text()), i + 1))
            for i in range(len(res), ui.tableWidget.rowCount()):
                curs.execute("insert into personal values(?, ?, ?, ?)", (str(i+1), str(ui.tableWidget.item(i, 0).text()), str(ui.tableWidget.item(i, 1).text()), str(ui.tableWidget.item(i, 2).text())))
        else:
            for i in range(ui.tableWidget.rowCount()):
                curs.execute("update personal set email = ?, username = ?, password = ? where id = ? ", (str(ui.tableWidget.item(i, 0).text()), str(ui.tableWidget.item(i, 1).text()), str(ui.tableWidget.item(i, 2).text()), i+1))
            for i in range(ui.tableWidget.rowCount(), len(res)):
                curs.execute("delete from personal where id = ? ", (i + 1,))
        curs.execute("select * from personal")
        res = curs.fetchall()
        print(res)
        con.commit()
    except:
        ui.label.setVisible(True)

def plus():
    ui.tableWidget.setRowCount(ui.tableWidget.rowCount()+1)
def minus():
    ui.tableWidget.setRowCount(ui.tableWidget.rowCount()-1)
def clean():
    ui.tableWidget.setRowCount(0)
    plus()

ui.save.clicked.connect(save)
ui.minus.clicked.connect(minus)
ui.plus.clicked.connect(plus)
ui.clean.clicked.connect(clean)

app.exec()
con.close()
