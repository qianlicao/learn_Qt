# Qt官网教程
# https://doc.qt.io/qt-5/modelview.html
import sys

from PySide2.QtCore import QAbstractTableModel, Qt, Signal
from PySide2.QtWidgets import QApplication, QTableView


class MyModel(QAbstractTableModel):
    edit_completed = Signal(list)

    def __init__(self):
        super().__init__()
        self.row = 2
        self.column = 3
        self.data_counter = 0
        self.row_counter = 0
        self.column_counter = 0
        # 二维数字存储数据
        self.m_gridData = [[a for a in range(self.column)] for b in range(self.row)]
        self.edit_completed.connect(self.slot_edit_completed)

    # When subclassing QAbstractTableModel , you must implement rowCount() , columnCount() , and data()
    def rowCount(self, parent=None, *args, **kwargs):
        print('rowCount() function called ' + str(self.row_counter) + ' times')
        self.row_counter += 1
        return self.row

    def columnCount(self, parent=None, *args, **kwargs):
        print('columnCount() function called ' + str(self.column_counter) + ' times')
        self.column_counter += 1
        return self.column

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            return self.m_gridData[index.row()][index.column()]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return 'first'
            elif section == 1:
                return 'second'
            elif section == 2:
                return 'third'

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled
        # return Qt.ItemIsEnabled # 激活item，否则item是灰色，不可被选中，不可被编辑
        # return Qt.ItemIsSelectable # item可选中
        # return Qt.ItemIsEditable # item可编辑
        # 为使item可编辑，需同时返回三者

    def setData(self, index, value, role):
        # QAbstractItemModel.checkIndex()，用于检查index是否有效，如果无效则退出
        if not self.checkIndex(index):
            return False
        if role == Qt.EditRole:
            self.m_gridData[index.row()][index.column()] = value
            self.edit_completed.emit(self.m_gridData)
            return True

    def slot_edit_completed(self,info):
        print('slot_edit_completed, data=',info)


if __name__ == '__main__':
    qt_app = QApplication(sys.argv)
    table_view = QTableView()
    my_model = MyModel()
    table_view.setModel(my_model)
    table_view.show()
    sys.exit(qt_app.exec_())
