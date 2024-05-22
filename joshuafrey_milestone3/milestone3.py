import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import*
import psycopg2


qtCreatorFile = "milestone3App.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone3(QMainWindow):
    def __init__(self):
        super(milestone3, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateBox.currentTextChanged.connect(self.stateChanged)
        self.ui.cityBox.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipcodeBox.itemSelectionChanged.connect(self.loadNumberBusiness)
        self.ui.zipcodeBox.itemSelectionChanged.connect(self.loadTotalPopulation)
        self.ui.zipcodeBox.itemSelectionChanged.connect(self.loadAverageIncome)
        self.ui.zipcodeBox.itemSelectionChanged.connect(self.loadTopCategories)
        self.ui.zipcodeBox.itemSelectionChanged.connect(self.loadCategories)
        self.ui.categoryList.itemSelectionChanged.connect(self.loadBusinesses)
        self.ui.zipcodeBox.itemSelectionChanged.connect(self.loadPopularBusinesses)
        self.ui.zipcodeBox.itemSelectionChanged.connect(self.loadSuccessfulBusinesses)
        
    def executeQuery(self, sql_str, params=None):
        try:
            conn = psycopg2.connect(
                "dbname='yelpdb2' user='postgres' host='localhost' password='Sho1303Jo$h'")
        except:
            print('Unable to connect to the database!')

        cur = conn.cursor()
        if params:
            cur.execute(sql_str, params)
        else:
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
                results = self.executeQuery(sql_str, (state,))
                for row in results:
                    self.ui.cityBox.addItem(row[0])
            except:
                print("Query failed!")

    def cityChanged(self):
        if (self.ui.stateBox.currentIndex() >= 0) and (len(self.ui.cityBox.selectedItems()) > 0):
            city = self.ui.cityBox.selectedItems()[0].text()
            sql_str = "SELECT distinct zipcode FROM business WHERE city = '" + city + "' ORDER BY zipcode;"
            try:
                self.ui.zipcodeBox.clear()
                results = self.executeQuery(sql_str, (city,))
                if len(results) == 0:
                    self.ui.zipcodeBox.addItem("No results found")
                else:
                    for row in results:
                        self.ui.zipcodeBox.addItem(row[0])
            except:
                print("Query failed!")
                
    def loadNumberBusiness(self):
        if len(self.ui.zipcodeBox.selectedItems()) > 0:
            zipcode = self.ui.zipcodeBox.selectedItems()[0].text()
            sql_str = "SELECT COUNT(*) FROM business WHERE zipcode = %s;"
            try:
                self.ui.numBusiness.clear()
                results = self.executeQuery(sql_str, (zipcode,))
                print("Query executed successfully")
                if len(results) == 0:
                    self.ui.numBusiness.addItem("No results found")
                else:
                    count = results[0][0]
                    self.ui.numBusiness.addItem(f"{count}")
            except Exception as e:
                print("Query failed with error:", e)

    def loadTotalPopulation(self):
        if len(self.ui.zipcodeBox.selectedItems()) > 0:
            zipcode = self.ui.zipcodeBox.selectedItems()[0].text()
            sql_str = "select population " \
                       "from zipcodeData "\
                        "where zipcode = %s;"
            try:
                self.ui.totalPop.clear()
                results = self.executeQuery(sql_str, (zipcode,))
                print("Query executed successfully")
                if len(results) == 0:
                    self.ui.totalPop.addItem("No results found")
                else:
                    population = results[0][0]
                    self.ui.totalPop.addItem(f"{population}")
            except Exception as e:
                print("Query failed with error:", e)

    def loadAverageIncome(self):
        if len(self.ui.zipcodeBox.selectedItems()) > 0:
            zipcode = self.ui.zipcodeBox.selectedItems()[0].text()
            sql_str = "select meanIncome " \
                       "from zipcodeData "\
                        "where zipcode = %s;"
            try:
                self.ui.avgIncome.clear()
                results = self.executeQuery(sql_str, (zipcode,))
                print("Query executed successfully")
                if len(results) == 0:
                    self.ui.avgIncome.addItem("No results found")
                else:
                    avg = results[0][0]
                    self.ui.avgIncome.addItem(f"{avg}")
            except Exception as e:
                print("Query failed with error:", e)

    def loadTopCategories(self):
        if len(self.ui.zipcodeBox.selectedItems()) > 0:
            zipcode = self.ui.zipcodeBox.selectedItems()[0].text()
            sql_str = "SELECT COUNT(*) AS count, category_name " \
                      "FROM categories as c, business as b " \
                      "WHERE b.business_id = c.business_id AND zipcode = '{}' " \
                      "GROUP BY category_name " \
                      "ORDER BY COUNT(DISTINCT b.business_id) DESC;".format(zipcode)

            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3 ;}"
                self.ui.topCategoryTable.horizontalHeader().setStyleSheet(style)
                self.ui.topCategoryTable.setColumnCount(len(results[0]))
                self.ui.topCategoryTable.setRowCount(len(results))
                self.ui.topCategoryTable.setHorizontalHeaderLabels(['# of Business', 'Category'])
                self.ui.topCategoryTable.resizeColumnsToContents()
                self.ui.topCategoryTable.setColumnWidth(0, 300)
                self.ui.topCategoryTable.setColumnWidth(1, 300)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.topCategoryTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print('Query failed!')

    def loadCategories(self):
        if len(self.ui.zipcodeBox.selectedItems()) > 0:
            zipcode = self.ui.zipcodeBox.selectedItems()[0].text()
            sql_str = "SELECT category_name " \
                      "FROM categories as c, business as b " \
                      "WHERE b.business_id = c.business_id AND zipcode = %s " \
                      "GROUP BY category_name;"
            try:
                self.ui.categoryList.clear()
                results = self.executeQuery(sql_str, (zipcode,))
                print("Query executed successfully")
                if len(results) == 0:
                    self.ui.categoryList.addItem("No results found")
                else:
                    for row in results:
                        category_name = row[0]
                        item = f"{category_name.strip()}"
                        self.ui.categoryList.addItem(item)
            except Exception as e:
                print("Query failed with error:", e)

    def loadBusinesses(self):
        if self.ui.categoryList.currentItem() is not None:
            category_name = self.ui.categoryList.currentItem().text()
            zipcode = self.ui.zipcodeBox.currentItem().text()
            sql_str = "select b.name, b.address, b.city, b.stars, b.review_count, b.reviewrating, b.num_checkins " \
                      "from business as b, categories as c " \
                      "where b.business_id = c.business_id AND b.zipcode = '{}' AND c.category_name = '{}';".format(zipcode, category_name)

            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3 ;}"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', 'Number of Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 500)
                self.ui.businessTable.setColumnWidth(1, 300)
                self.ui.businessTable.setColumnWidth(2, 300)
                self.ui.businessTable.setColumnWidth(3, 300)
                self.ui.businessTable.setColumnWidth(4, 300)
                self.ui.businessTable.setColumnWidth(5, 300)
                self.ui.businessTable.setColumnWidth(6, 300)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print('Query failed!')

    def loadPopularBusinesses(self):
        if len(self.ui.zipcodeBox.selectedItems()) > 0:
            zipcode = self.ui.zipcodeBox.selectedItems()[0].text()
            sql_str = "select name, stars, reviewRating, review_count " \
                      "from business " \
                      "where zipcode = '{}' AND stars > " \
                        "(select avg(stars) from business where zipcode = '{}') " \
                        "AND review_count > " \
                        "(select avg(review_count) from business where zipcode = '{}') " \
                       "ORDER BY stars desc;".format(zipcode, zipcode, zipcode) 

            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3 ;}"
                self.ui.popularBusinessTable.horizontalHeader().setStyleSheet(style)
                self.ui.popularBusinessTable.setColumnCount(len(results[0]))
                self.ui.popularBusinessTable.setRowCount(len(results))
                self.ui.popularBusinessTable.setHorizontalHeaderLabels(['Business Name', 'Stars', 'Review Rating', 'Review Count'])
                self.ui.popularBusinessTable.resizeColumnsToContents()
                self.ui.popularBusinessTable.setColumnWidth(0, 300)
                self.ui.popularBusinessTable.setColumnWidth(1, 300)
                self.ui.popularBusinessTable.setColumnWidth(2, 300)
                self.ui.popularBusinessTable.setColumnWidth(3, 300)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.popularBusinessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print('Query failed!')
                
    def loadSuccessfulBusinesses(self):
        if len(self.ui.zipcodeBox.selectedItems()) > 0:
            zipcode = self.ui.zipcodeBox.selectedItems()[0].text()
            sql_str = "select name, review_count, num_checkins " \
                      "from business " \
                      "where zipcode = '{}' AND num_checkins > " \
                        "(select avg(num_checkins) from business where zipcode = '{}') " \
                       "ORDER BY num_checkins desc;".format(zipcode, zipcode) 

            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3 ;}"
                self.ui.successfulBusinessTable.horizontalHeader().setStyleSheet(style)
                self.ui.successfulBusinessTable.setColumnCount(len(results[0]))
                self.ui.successfulBusinessTable.setRowCount(len(results))
                self.ui.successfulBusinessTable.setHorizontalHeaderLabels(['Business Name', 'Review Count', 'Number of Checkins'])
                self.ui.successfulBusinessTable.resizeColumnsToContents()
                self.ui.successfulBusinessTable.setColumnWidth(0, 300)
                self.ui.successfulBusinessTable.setColumnWidth(1, 300)
                self.ui.successfulBusinessTable.setColumnWidth(2, 300)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.successfulBusinessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
            except:
                print('Query failed!')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone3()
    window.show()
    window.resize(1800, 1200)
    sys.exit(app.exec_())