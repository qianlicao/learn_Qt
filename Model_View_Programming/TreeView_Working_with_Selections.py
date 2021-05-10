# Qt官网教程
# https://doc.qt.io/qt-5/modelview.html
import sys

from PySide2.QtCore import Qt, QModelIndex
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QApplication, QTableView, QMainWindow, QTreeView


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.tree_view = QTreeView(self)
        self.setCentralWidget(self.tree_view)
        self.standard_model = QStandardItemModel(parent=self)
        root_item = self.standard_model.invisibleRootItem()
        first_row = self.prepare_row("first", "second", "third")
        root_item.appendRow(first_row)
        second_row = self.prepare_row("111", "222", "333")
        first_row[0].appendRow(second_row)

        americaItem = QStandardItem("America")
        mexicoItem = QStandardItem("Canada")
        usaItem = QStandardItem("USA")
        bostonItem = QStandardItem("Boston")
        europeItem = QStandardItem("Europe")
        italyItem = QStandardItem("Italy")
        romeItem = QStandardItem("Rome")
        veronaItem = QStandardItem("Verona")

        root_item.appendRow(americaItem)
        root_item.appendRow(europeItem)
        americaItem.appendRow(mexicoItem)
        americaItem.appendRow(usaItem)
        usaItem.appendRow(bostonItem)
        europeItem.appendRow(italyItem)
        italyItem.appendRow(romeItem)
        italyItem.appendRow(veronaItem)

        self.tree_view.setModel(self.standard_model)
        self.tree_view.expandAll()

        selection_model = self.tree_view.selectionModel()
        selection_model.selectionChanged.connect(self.slot_selection_changed)

    def prepare_row(self, first, second, third):
        return [
            QStandardItem(first),
            QStandardItem(second),
            QStandardItem(third)
        ]

    def slot_selection_changed(self, new_selection, old_selection):
        index = self.tree_view.selectionModel().currentIndex()
        select_text = index.data(Qt.DisplayRole)
        hierarchy_level = 1
        seek_root = index
        while seek_root.parent() != QModelIndex():
            seek_root = seek_root.parent()
            hierarchy_level += 1
        self.setWindowTitle(select_text + ', level ' + str(hierarchy_level))


if __name__ == '__main__':
    qt_app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(qt_app.exec_())
