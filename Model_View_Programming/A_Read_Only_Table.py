# Qt官网教程
# https://doc.qt.io/qt-5/modelview.html
import sys

from PySide2.QtCore import QAbstractTableModel, Qt, QTime, QTimer
from PySide2.QtGui import QFont, QBrush
from PySide2.QtWidgets import QApplication, QTableView


class MyModel(QAbstractTableModel):
    data_counter = 0
    row_counter = 0
    column_counter = 0

    def __init__(self):
        super().__init__()
        timer = QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(self.timer_hit)
        timer.start()

    # When subclassing QAbstractTableModel , you must implement rowCount() , columnCount() , and data()
    def rowCount(self, parent=None, *args, **kwargs):
        print('rowCount() function called ' + str(self.row_counter) + ' times')
        self.row_counter += 1
        return 2

    def columnCount(self, parent=None, *args, **kwargs):
        print('columnCount() function called ' + str(self.column_counter) + ' times')
        self.column_counter += 1
        return 3

    def data(self, index, role=None):
        print('data() function called ' + str(self.data_counter) + ' times')
        self.data_counter += 1
        row = index.row()
        column = index.column()
        if role == Qt.DisplayRole:
            if row == 0 and column == 1:
                return '<--left'
            elif row == 1 and column == 1:
                return 'right-->'
            elif row == 0 and column == 0:
                return QTime.currentTime().toString()
            else:
                return 'row' + str(row) + ',' + 'column' + str(column)
        elif role == Qt.FontRole:
            if row == 0 and column == 0:
                bold_font = QFont()
                bold_font.setBold(True)
                return bold_font
        elif role == Qt.BackgroundRole:
            if row == 1 and column == 2:
                return QBrush(Qt.red)
        elif role == Qt.TextAlignmentRole:
            if row == 1 and column == 1:
                return Qt.AlignRight | Qt.AlignVCenter
        elif role == Qt.CheckStateRole:
            if row == 1 and column == 0:
                return Qt.Checked

    def timer_hit(self):
        index = self.createIndex(0, 0)
        self.dataChanged.emit(index, index, Qt.DisplayRole)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return 'first'
            elif section == 1:
                return 'second'
            elif section == 2:
                return 'third'


if __name__ == '__main__':
    qt_app = QApplication(sys.argv)
    table_view = QTableView()
    my_model = MyModel()
    table_view.setModel(my_model)
    table_view.show()
    sys.exit(qt_app.exec_())
