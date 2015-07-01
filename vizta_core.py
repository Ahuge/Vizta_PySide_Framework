__author__ = 'Alex'

from PySide import QtGui, QtCore
from itertools import izip_longest
import collections

class Grid(QtGui.QWidget):

    def __init__(self, title=""):
        super(Grid, self).__init__()

        self.setWindowTitle(title)

        self.grid = QtGui.QGridLayout()
        self.widgetDict = {}

        self.initUI()
        self.grid.setSpacing(10)
        self.setLayout(self.grid)

    def addComboBox(self, label, options, userdata=[], index=0, height=1, width=1 ):

        comboBox = QtGui.QComboBox()
        for item, data in izip_longest(options, userdata):
            comboBox.addItem(item, userData=data)
        startIndex = index

        numItems = comboBox.count()
        if startIndex >= numItems:
            startIndex = numItems-1

        comboBox.setCurrentIndex(startIndex)

        return self.addItem(label, comboBox, height=height, width=width)

    def addTable(self, label, rows=None, cols=None, data=None, height=1, width=1, selectionMode=QtGui.QAbstractItemView.SingleSelection ):
        if rows is not None and cols is not None:
            table = ATableWidget(rows, cols)
        elif data is not None:
            rows, cols = self._getTableData( data )
            table = ATableWidget(rows, cols)
        else:
            table = ATableWidget(rows, cols)

        if data is not None:
            if isinstance(data, ViztaTableData):
                print "Data is a ViztaTableData object."
                table.setData(data, clear=True)
            else:
                print "Data is not a ViztaTableData Type, attempting raw parsing."
                table.setRawData(data, clear=True)

        table.setSelectionMode( selectionMode )
        return self.addItem(label, table, height=height, width=width)

    def addItem(self, label, item, height=1, width=1 ):
        labelItem = QtGui.QLabel(label)
        item = item

        listHeight = self.getHeight()

        self.grid.addWidget(labelItem  , listHeight+1, 0, 1        , 1)
        self.grid.addWidget(item        , listHeight+1, 1, height   , width)

        self.widgetDict[label] = {
            "height": height,
            "width": width,
            "widgets": [labelItem, item]
        }

        return (labelItem, item)

    def getHeight(self):
        totalHeight = 0
        for x in self.widgetDict:
            totalHeight += self.widgetDict[x]["height"]
        return totalHeight

    def _getTableData( self, data ):
        if not isinstance(data, ViztaTableData):
            return self._getRawTableData(data)

        rows = len(data["HEADER"]["ROWS"])
        cols = len(data["HEADER"]["COLUMNS"])
        return rows, cols

    def _getRawTableData( self, data ):

        rows = 0
        cols = 0
        for row, col in data.iteritems():
            rows += 1
            if len(col) > cols:
                cols = len(col)
        return rows, cols


class ATableWidget(QtGui.QTableWidget):

    def setRawData(self, data, clear=True):
        if clear:
            self.clear()

        rowNum = 0
        for row, columnDict in data.iteritems():
            rHeader = QtGui.QTableWidgetItem( row )
            self.setVerticalHeaderItem(rowNum, rHeader)
            columnNum = 0
            for column, cell in columnDict.iteritems():
                cHeader = QtGui.QTableWidgetItem( column )
                self.setHorizontalHeaderItem(columnNum, cHeader)

                item = QtGui.QTableWidgetItem( unicode(cell) )
                self.setItem(rowNum, columnNum, item)
                columnNum += 1
            rowNum += 1

        return True

    def setData(self, data, clear=True):
        if not isinstance(data, ViztaTableData):
            print "Data is not a ViztaTableData Type, attempting raw parsing."
            return self.setRawData(data, clear=True)

        if clear:
            self.clear()

        rows = data["HEADER"]["ROWS"]
        columns = data["HEADER"]["COLUMNS"]

        self.setVerticalHeaderLabels(rows)
        self.setHorizontalHeaderLabels(columns)

        rowNum = 0
        for row in data["PAYLOAD"]:
            columnNum = 0
            for cell in row:
                item = QtGui.QTableWidgetItem( unicode(cell) )
                self.setItem(rowNum, columnNum, item)

                columnNum += 1
            rowNum += 1
        return True

    def setItem(self, rowName, columnName, item):

        if isinstance(rowName, int) and isinstance(columnName, int):
            return super(ATableWidget, self).setItem(rowName, columnName, item)

        colIndex = None
        rowIndex = None
        for x in range(0, self.columnCount(), 1):
            headertext = self.horizontalHeaderItem(x).text()
            if columnName == headertext:
                colIndex = x
        for x in range(0, self.rowCount(), 1):
            headertext = self.verticalHeaderItem(x).text()
            if rowName == headertext:
                rowIndex = x

        if colIndex is not None and rowIndex is not None:
            return super(ATableWidget, self).setItem(rowIndex, colIndex, item)

        if rowIndex is None:
            raise ValueError("Your row header name was not found.")
        raise ValueError("Your column header name was not found.")


class ViztaTableData( collections.MutableMapping ):

    def __init__(self, rows, columns, payload,*args, **kwargs):

        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

        self.store["HEADER"] = {}
        self.store["HEADER"]["ROWS"] = rows
        self.store["HEADER"]["COLUMNS"] = columns

        self.store["PAYLOAD"] = payload

        self._rows = rows
        self._columns = columns
        self._payload = payload

    def __setitem__(self, key, value):
        if key == "ROWS":
            self._rows = value
        elif key == "COLUMNS":
            self._columns = value
        elif key == "PAYLOAD":
            self._payload = value

        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):

        if key == "ROWS":
            self._rows = []
        elif key == "COLUMNS":
            self._columns = []
        elif key == "PAYLOAD":
            self._payload = []

        del self.store[self.__keytransform__(key)]

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, value):
        self.store["HEADER"]["ROWS"] = value
        self._rows = value

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        self.store["HEADER"]["COLUMNS"] = value
        self._columns = value

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        self.store["PAYLOAD"] = value
        self._payload = value

