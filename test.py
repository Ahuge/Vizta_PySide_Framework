__author__ = 'Alex'

import cProfile

def _getAddTableData(  ):
    rows = 0
    cols = 0
    for row in dd:
        rows += 1
        rowCols = 0
        for col in dd[row]:
            rowCols += 1
        if rowCols > cols:
            cols = rowCols
    return(rows, cols)

def _getAddTableDataNew(  ):

    rows = 0
    cols = 0
    for row, col in dd.iteritems():
        rows += 1
        if len(col) > cols:
            cols = len(col)
    return(rows, cols)

def main():
    global dd
    dd = {}
    for x in xrange(30):
        dd[x] = {}
        for y in xrange(4):
            dd[x][y] = y

    dd = {
        "Alex": {
            "a": 1,
            "b": 2,
            "c": 3,
            },
        "Tom": {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
            },
        "Mike": {
            "a": 1,
            "b": 2,
            },
        }


main()



pr = cProfile.Profile()
pr.run("_getAddTableData()")
pr.print_stats()

pr2 = cProfile.Profile()
pr2.run("_getAddTableDataNew()")
pr2.print_stats()
print _getAddTableDataNew()
print _getAddTableData()

for row, col in dd.iteritems():
    print row
    for column, cell in col.iteritems():
        print "\t", column, ": ", cell