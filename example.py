__author__ = 'Alex'

from PySide import QtGui, QtCore
import sys
import vizta_core
from vizta_core import ViztaTableWidget

class Example(vizta_core.Grid):

    def initUI(self):

        titleEdit = QtGui.QLineEdit()
        authorEdit = QtGui.QLineEdit()
        reviewEdit = QtGui.QTextEdit()
        checkbox = QtGui.QCheckBox()

        data = { "Alex": { "a": 1, "b": 2, "c": 3, }, "Tom": { "a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, }, "Mike": { "a": 1, "b": 2, }, }

        self.addItem("Title", titleEdit)
        self.addComboBox("Box", ["Hi", "Two", "3", "Fore"], index=411 )
        self.addItem("Author", authorEdit)
        self.addItem("Review", reviewEdit)
        self.addItem("Options", checkbox)
        self.addCheckBox("Options2", state=1)

        # Adding a table with the "Raw" format for data, meaning it is not in a ViztaTableData format
        # Since it is a dict, you cant always count on the data being in the right order.
        data = {
            "Alex": {
                "a": 1, "b": 2, "c": 3,
                },
            "Tom": {
                "a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6,
                },
            "Mike": {
                "a": 1, "b": 2,
                },
            }

        self.addTable("Table", data=data)

        # Constructing a Table without any data, then adding it with setData
        myTable = self.addTable("My Table", rows=3, cols=6)
        myTable[1].setData(data, clear=True)


        # Adding a table via the ViztaTableData data structure
        # Then inserting a new QTableWidgetItem into the table by header names instead of index
        datagen = vizta_core.ViztaTableData(["Mike", "Alex", "Ron"],
                                  ["a", "b", "c", "d", "e", "f"],
                                  [ ["one", "two"], ["one", "two", "three"], ["one", "two", "three", "four", "five", "six"], ]
                                  )

        self.addTable("ViztaTable", data=datagen)
        viztaTable = self.widgetDict["ViztaTable"][1]
        newCell = QtGui.QTableWidgetItem( "TEST" )
        viztaTable.setTableItem( "Mike", "f", newCell)


        testTable = self.addTable("TestTable")


        self.setGeometry(300, 300, 705, 400)

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()

def ViztaTableDataTest():

    data = vizta_core.ViztaTableData(["Mike", "Alex", "Tom"],
                              ["a", "b", "c", "d", "e", "f"],
                              [ [1, 2], [1, 2, 3], [1, 2, 3, 4, 5, 6], ]
                              )
    
    print "---------------------------------"
    print data["HEADER"]["ROWS"]
    print data["HEADER"]["COLUMNS"]
    print data["PAYLOAD"]
    
    print "---------------------------------"
    
    data["HEADER"]["ROWS"] = ["Danny", "Ron", "Smithy"]
    print data["HEADER"]["ROWS"]
    
    data["HEADER"]["COLUMNS"] = [1, 2, 3, 4, 5, 6]
    print data["HEADER"]["COLUMNS"]
    
    data["PAYLOAD"] = [ ["one", "two"], ["one", "two", "three"], ["one", "two", "three", "four", "five", "six"], ]
    print data["PAYLOAD"]













if __name__ == '__main__':
    main()
    ViztaTableDataTest()

