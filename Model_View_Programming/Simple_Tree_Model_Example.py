# https://doc.qt.io/qt-5/qtwidgets-itemviews-simpletreemodel-example.html
import sys

from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt, QFile, QIODevice, QByteArray
from PySide2.QtWidgets import QApplication, QTreeView


class TreeItem:
    def __init__(self, data, parent_item=None):
        self.m_child_items = []
        self.m_item_data = data
        self.m_parent_item = parent_item

    def append_child(self, item):
        self.m_child_items.append(item)
        item.m_parent_item = self

    def child(self, row):
        if row < 0 or row >= len(self.m_child_items):
            return None
        return self.m_child_items[row]

    def child_count(self):
        return len(self.m_child_items)

    def column_count(self):
        return len(self.m_item_data)

    def data(self, column):
        if column < 0 or column >= len(self.m_item_data):
            return None
        return self.m_item_data[column]

    def row(self):
        if self.m_parent_item:
            return self.m_parent_item.m_child_items.index(self)
        return 0

    def parent_item(self):
        return self.m_parent_item


class TreeModel(QAbstractItemModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.root_item = TreeItem(['Title', 'Summary'])
        self.setupModelData(data, self.root_item)

    def data(self, index: QModelIndex, role=None):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(index.column())

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.NoItemFlags
        return super().flags(index)

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.root_item.data(section)
        return None

    def index(self, row, column, parent: QModelIndex = None, *args, **kwargs):
        # QAbstractItemModel.hasIndex()
        # Returns true if the model returns a valid QModelIndex for row and column with parent, otherwise returns false
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        # QModelIndex.isValid()
        # Returns true if this model index is valid; otherwise returns false.
        # A valid index belongs to a model, and has non - negative row and column numbers.
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QModelIndex()

    def parent(self, index: QModelIndex):
        if not index.isValid():
            return QModelIndex()
        child_item = index.internalPointer()
        parent_item = child_item.parent_item()
        if parent_item == self.root_item:
            return QModelIndex()
        print(child_item)
        print(parent_item)
        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
        return parent_item.child_count()

    def columnCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return parent.internalPointer().column_count()
        return self.root_item.column_count()

    def setupModelData(self, data: list, parent):
        data = [ii for ii in data if ii != '']  # 删除空字符串
        number = 0
        while number < len(data):
            position = 0
            while position < len(data[number]):
                if data[number][position] != ' ':
                    break
                position += 1
            print('number=', number, '   position=', position)
            line_data = data[number].strip()  # 去除前后空格
            print(line_data)
            if len(line_data) != 0:
                # split()函数默认可以按空格分割，并且把结果中的空字符串删除掉，留下有用信息
                # 此处按照制表符\t分割
                column_strings = line_data.split('\t')
                # 删除空字符串
                column_strings = [ii for ii in column_strings if ii != '']
                print(column_strings)
                item = TreeItem(column_strings)
            if position == 0:
                self.root_item.append_child(item)
                zero_level_item = item
            elif position == 4:
                zero_level_item.append_child(item)
                four_level_item = item
            elif position == 8:
                four_level_item.append_child(item)

            number += 1


if __name__ == '__main__':
    qt_app = QApplication(sys.argv)
    # file = QFile("default.txt")
    # file.open(QIODevice.ReadOnly);
    # print(file.readAll())
    data = []
    with open("default.txt", "r") as f:
        for line in f.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            data.append(line)
    model = TreeModel(data)
    view = QTreeView()
    view.setModel(model)
    view.setWindowTitle('Simple Tree Model')
    view.expandAll()
    view.show()
    sys.exit(qt_app.exec_())
