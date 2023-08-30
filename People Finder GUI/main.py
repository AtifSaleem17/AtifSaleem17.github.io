from loader import Ui_loader
from finalUI import  Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from fill_dialoge import Ui_Dialog as FD
from  del_dialoge import Ui_Dialog as DD
from select_dialoge import  Ui_Dialog as SD
from update_window import  Ui_update_window
import os
import csv


counter=0

class Main():
    def __init__(self):

    #todo loading window
        self.loading_window=QtWidgets.QMainWindow()
        self.loading_obj=Ui_loader()
        self.loading_obj.setupUi(self.loading_window)
        self.loading_window.show()
        # todo setting timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.loader_progress_bar)
        self.timer.start(35)

    #todo main_window
        self.main_window = QtWidgets.QMainWindow()
        self.main_obj = Ui_MainWindow()
        self.main_obj.setupUi(self.main_window)

    # todo loading data
        self.load_data()

    # todo update_window
        self.update_window = QtWidgets.QMainWindow()
        self.update_obj = Ui_update_window()
        self.update_obj.setupUi(self.update_window)

    #todo fill_dialoge
        self.fill_dia = QtWidgets.QDialog()
        self.fill_obj = FD()
        self.fill_obj.setupUi(self.fill_dia)

    # todo del_dialoge
        self.del_dia = QtWidgets.QDialog()
        self.del_obj = DD()
        self.del_obj.setupUi(self.del_dia)

    # todo select_dialoge
        self.select_dia = QtWidgets.QDialog()
        self.select_obj = SD()
        self.select_obj.setupUi(self.select_dia)

    def train_progress_bar(self):
        global counter
        # todo setting progress bar value
        self.main_obj.progressBar4.setValue(counter)
        self.main_obj.progressBar4.setTextVisible(True)
        if counter > 100:
            self.timer2.stop()
            self.main_obj.train4_1.setEnabled(True)
            counter=0
            self.main_obj.progressBar4.setValue(counter)
            self.main_obj.progressBar4.setTextVisible(False)
        counter += 1

    def start(self):
        self.timer2=QtCore.QTimer()
        self.main_obj.train4_1.setEnabled(False)
        self.timer2.start(100)
        self.timer2.timeout.connect(self.train_progress_bar)

    def loader_progress_bar(self):
        global counter
        # todo setting progress bar value
        self.loading_obj.progressBar.setValue(counter)
        if counter > 100:
            self.timer.stop()
            counter=0
            # todo open app and close loader
            self.loading_window.close()
            self.main_window.show()
        counter += 1

    def load_data(self):
        if self.check(): #calls the check fucntion
           # todo reading file
           self.file_data = self.read_file()
           # todo writing in table
           self.main_obj.table.setRowCount(0)
           self.file_data = iter(self.file_data)
           next(self.file_data)
           for row, rd in enumerate(self.file_data):
              self.main_obj.table.insertRow(row)
              for col, data in enumerate(rd):
                  self.main_obj.table.setItem(row, col, QtWidgets.QTableWidgetItem(str(data)))
           del self.file_data
        else:return

    def write_file(self,file_data):
        with open("subjects_data.csv", "w") as f:
            wo = csv.writer(f, lineterminator='\n')
            wo.writerows(self.file_data)
            del wo
        # todo load the file into table
        self.load_data()

    def read_file(self):
        self.file_data = list()
        with open("subjects_data.csv") as f:
            self.ro = csv.reader(f)
            for x in self.ro:
                self.file_data.append(x)
            del self.ro
        return self.file_data

    def insert(self):
        self.check()
        self.row=list()
        # todo taking values and inserting new person
        self.row.append(self.main_obj.name.text().upper())
        self.row.append(self.main_obj.age.text().upper())
        if self.main_obj.male.isChecked():
            self.row.append("MALE")
        elif self.main_obj.female.isChecked():
            self.row.append("FEMALE")
        self.row.append(self.main_obj.ph_number.text().upper())
        self.row.append(self.main_obj.address.text().upper())

        # todo checking validation
        if "" in self.row or (not self.main_obj.male.isChecked() and not self.main_obj.female.isChecked()):
            self.fill_dia.show()
            return
        else:
            # todo read file data
            self.file_data = self.read_file()

            # todo auto increment in ID
            if len(self.file_data) == 1:
                self.row.insert(0, 1)
            else:
                self.row.insert(0, int(self.file_data[len(self.file_data) - 1][0]) + 1)

            # todo appending row in file
            with open("subjects_data.csv", "a") as f:
                self.wo = csv.writer(f, lineterminator='\n')
                self.wo.writerow(self.row)
                del self.wo

            # todo releasing memory
            del self.row
            del self.file_data
            self.main_obj.name.clear()
            self.main_obj.age.clear()
            self.main_obj.ph_number.clear()
            self.main_obj.address.clear()
            # todo calls the load function for updation
            self.load_data()

    def search(self):
        self.txt=self.main_obj.search_bar.text()

      #todo if nothing is searched then load the whole file
        if self.txt == "":
           self.load_data()
           return

        else:
            # todo reading file
            self.file_data = self.read_file()

            self.searched_data = list()

            #todo matching values and saving the matched ones (searching)
            for x in self.file_data:
                if self.txt.casefold() in x[1].casefold() and x[1] != "NAME":
                #if x[1].casefold().startswith(self.txt.casefold()):
                    self.searched_data.append(x)

            #todo writing in table
            self.main_obj.table.setRowCount(0)
            for row, rd in enumerate(self.searched_data):
                self.main_obj.table.insertRow(row)
                for col, data in enumerate(rd):
                    self.main_obj.table.setItem(row, col, QtWidgets.QTableWidgetItem(data))

            #todo releasing memory
            del self.file_data
            del self.searched_data
            del self.txt

    def make_sure(self):
        if self.main_obj.table.selectedItems() != []:
            self.del_dia.show()
            self.del_obj.del_buttonBox.accepted.connect(self.delete_row)
            self.del_obj.del_buttonBox.rejected.connect(self.main_obj.table.clearSelection)
        else:
            self.select_dia.show()

    def delete_row(self):
        if self.main_obj.table.selectedItems() != []:
           # todo selected row
           self.row=self.main_obj.table.selectedItems()
           # todo ID number
           self.index = self.row[0].text()
           #todo reading data from file.
           self.file_data=self.read_file()
           #todo find the selected one and delete it.
           for i, x in enumerate(self.file_data):
               # todo both are strings.
               if self.index == x[0]:
                   self.deleted_row=self.file_data.pop(i)
                   break
               else: pass
           #todo overwite the file
           self.write_file(self.file_data)

           return self.deleted_row

    def open_update_win(self):
        if self.main_obj.table.selectedItems()!=[]:
            self.row = self.main_obj.table.selectedItems()
            # todo fill exixting values
            self.update_obj.updated_name.setText(self.row[1].text())
            self.update_obj.updated_age.setText(self.row[2].text())

            if self.row[3].text() == "MALE":
                self.update_obj.updated_gender.setCurrentIndex(0)
            elif self.row[3].text() == "FEMALE":
                self.update_obj.updated_gender.setCurrentIndex(1)

            self.update_obj.updated_number.setText(self.row[4].text())
            self.update_obj.updated_address.setText(self.row[5].text())

            self.update_window.show()
            self.update_obj.update.clicked.connect(self.update_values)
            self.update_obj.cancel.clicked.connect(self.main_obj.table.clearSelection)
        else:
            self.select_dia.show()
            return

    def update_values(self):
        if self.main_obj.table.selectedItems() !=[]:
            self.row = list()
            # todo making list of updated values
            self.row.append(self.main_obj.table.selectedItems()[0].text())
            self.row.append(self.update_obj.updated_name.text().upper())
            self.row.append(self.update_obj.updated_age.text().upper())
            self.row.append(self.update_obj.updated_gender.currentText())
            self.row.append(self.update_obj.updated_number.text().upper())
            self.row.append(self.update_obj.updated_address.text().upper())

            # todo checking validation
            if "" in self.row:
                self.fill_dia.show()
                return
            else:
                self.file_data = self.read_file()

                for i, x in enumerate(self.file_data):
                    if x[0] == self.row[0]:
                        self.file_data[i] = self.row
                        break
                    else:
                        pass
                # todo overwite the file
                self.write_file(self.file_data)


                self.update_window.close()

    def check(self):
        if (not os.path.exists("subjects_data.csv")):
            with open("subjects_data.csv", "w") as f:
                self.wo = csv.writer(f, lineterminator='\n')
                self.wo.writerow(["ID", "NAME", "AGE", "GENDER", "PHONE NO#", "ADDRESS"])
                del self.wo
            return False
        else:
            return True

    def main_function(self):
        #todo        ____________  buttons connections  ____________
        """indexes
        new=1
        select=2
        train=3
        track=4
        report=5
        """
        #todo page1
        #todo with current widget
        self.main_obj.select1.clicked.connect(lambda :self.main_obj.stackedWidget.setCurrentWidget(self.main_obj.page3))
         # todo with current index
        self.main_obj.new1.clicked.connect(lambda :self.main_obj.stackedWidget.setCurrentIndex(1))

        #todo page2
        self.main_obj.new2.clicked.connect(lambda :self.main_obj.stackedWidget.setCurrentIndex(1))
        self.main_obj.select2.clicked.connect(lambda :self.main_obj.stackedWidget.setCurrentIndex(2))
        self.main_obj.train2.clicked.connect(lambda :self.main_obj.stackedWidget.setCurrentIndex(3))
        self.main_obj.track2.clicked.connect(lambda :self.main_obj.stackedWidget.setCurrentIndex(4))
        self.main_obj.report2.clicked.connect(lambda :self.main_obj.stackedWidget.setCurrentIndex(5))
        self.main_obj.back2.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(2))  # back to select

        # todo page3
        self.main_obj.new3.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(1))
        self.main_obj.select3.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(2))
        self.main_obj.train3.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(3))
        self.main_obj.track3.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(4))
        self.main_obj.report3.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(5))
        self.main_obj.back3.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(0))  # back to start

        # todo page4
        self.main_obj.new4.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(1))
        self.main_obj.select4.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(2))
        self.main_obj.train4.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(3))
        self.main_obj.track4.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(4))
        self.main_obj.report4.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(5))
        self.main_obj.back4.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(1))  # back to new

        # todo page5
        self.main_obj.new5.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(1))
        self.main_obj.select5.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(2))
        self.main_obj.train5.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(3))
        self.main_obj.track5.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(4))
        self.main_obj.report5.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(5))
        self.main_obj.back5.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(3))  # back to train

        # todo page6
        self.main_obj.new6.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(1))
        self.main_obj.select6.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(2))
        self.main_obj.train6.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(3))
        self.main_obj.track6.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(4))
        self.main_obj.report6.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(5))
        self.main_obj.back6.clicked.connect(lambda: self.main_obj.stackedWidget.setCurrentIndex(4))  # back to track

        # todo        ____________  submitting new person  ____________
        self.main_obj.submit.clicked.connect(self.insert)

        # todo        ____________  searching  ____________
        self.main_obj.search_bar.textChanged.connect(self.search)

        # todo        ____________  deleting  ____________
        self.main_obj.delete3.clicked.connect(self.make_sure)

        # todo        ____________  updating  ____________
        self.main_obj.update3.clicked.connect(self.open_update_win)

        # todo        ____________  training progress_bar  ____________
        self.main_obj.train4_1.clicked.connect(self.start)

if __name__ == '__main__':
   import sys
   app=QtWidgets.QApplication(sys.argv)
   obj=Main()
   obj.main_function()
   sys.exit(app.exec_())


