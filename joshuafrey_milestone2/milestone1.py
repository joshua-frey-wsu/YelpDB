import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import  QIcon, QPixmap
import psycopg2

qtCreatorFile = "milestone1App.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone1(QMainWindow):
    def __init__(self):
        super(milestone1, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateBox.currentTextChanged.connect(self.stateChanged)
        self.ui.cityBox.currentTextChanged.connect(self.cityChanged)


    def executeQuery(self, sql_str):
        try:
            conn = psycopg2.connect("dbname='yelpdb2' user='postgres' host='localhost' password='Sho1303Jo$h'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result


    def loadStateList(self):
        sql_str = "SELECT distinct state FROM Business ORDER BY state; "
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateBox.addItem(row[0])
        except:
            print("Query failed!")
        self.ui.stateBox.setCurrentIndex(-1)
        self.ui.stateBox.clearEditText()


    def stateChanged(self):
        self.ui.cityBox.clear()
        state = self.ui.stateBox.currentText()
        if (self.ui.stateBox.currentIndex() >=0):
            sql_str = "SELECT distinct city FROM business WHERE state = '" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityBox.addItem(row[0])
            except:
                print("Query failed!")

    def cityChanged(self):
        self.ui.zipcodeBox.clear()
        city = self.ui.cityBox.currentText()
        if (self.ui.cityBox.currentIndex() >= 0):
            sql_str = "SELECT DISTINCT zipcode FROM Business WHERE city = '" + city + "' ORDER BY zipcode;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.zipcodeBox.addItem(row[0])
            except:
                print("Query failed!")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone1()
    window.show()
    sys.exit(app.exec_())