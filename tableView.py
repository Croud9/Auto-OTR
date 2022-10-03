# import sys
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *

# class Table(QWidget):
#     def __init__(self,parent=None):
#         super(Table, self).__init__(parent)
#         # Установить заголовок и начальный размер
#         self.setWindowTitle('«Пример представления таблицы QTableView»')
#         self.resize(500,300)

#         # Установить иерархию данных, 4 строки и 4 столбца
#         self.model=QStandardItemModel(4,4)
#         # Установить текстовое содержимое четырех меток заголовка в горизонтальном направлении
#         self.model.setHorizontalHeaderLabels(['«Название 1»','«Название 2»','«Название 3»','«Название 4»'])


#         # Тодо оптимизации 2 добавить данные
#         self.model.appendRow([
#             QStandardItem('row %s,column %s' % (11,11)),
#             QStandardItem('row %s,column %s' % (11,11)),
#             QStandardItem('row %s,column %s' % (11,11)),
#             QStandardItem('row %s,column %s' % (11,11)),
#         ])

#         for row in range(4):
#             for column in range(4):
#                 item=QStandardItem('row %s,column %s'%(row,column))
#                 # Установить текстовое значение каждой позиции
#                 self.model.setItem(row,column,item)

#         # Создать представление таблицы, установить модель на пользовательскую модель
#         self.tableView=QTableView()
#         self.tableView.setModel(self.model)



#         #todo Оптимизация 1 Форма заполняет окно
#         #Горизонтальная метка расширяет остальную часть окна и заполняет форму
#         self.tableView.horizontalHeader().setStretchLastSection(True)
#         # Горизонтальное направление, размер таблицы увеличивается до соответствующего размера
#         self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
#         #TODO Optimization 3 Удалить текущие выбранные данные
#         indexs=self.tableView.selectionModel().selection().indexes()
#         print(indexs)
#         if len(indexs)>0:
#             index=indexs[0]
#             self.model.removeRows(index.row(),1)


#         # Установить макет
#         layout=QVBoxLayout()
#         layout.addWidget(self.tableView)
#         self.setLayout(layout)
# if __name__ == '__main__':
#     app=QApplication(sys.argv)
#     table=Table()
#     table.show()
#     sys.exit(app.exec_())



import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtCore


class WrapHeader(QtWidgets.QHeaderView):
    def sectionSizeFromContents(self, logicalIndex):
        size = super().sectionSizeFromContents(logicalIndex)
        if self.model():
            if size.width() > self.sectionSize(logicalIndex):
                text = self.model().headerData(logicalIndex, 
                    self.orientation(), QtCore.Qt.DisplayRole)
                if not text:
                    return size
                text = str(text)

                option = QtWidgets.QStyleOptionHeader()
                self.initStyleOption(option)
                alignment = self.model().headerData(logicalIndex, 
                    self.orientation(), QtCore.Qt.TextAlignmentRole)
                if alignment is None:
                    alignment = option.textAlignment

                margin = self.style().pixelMetric(
                    QtWidgets.QStyle.PM_HeaderMargin, option, self)
                maxWidth = self.sectionSize(logicalIndex) - margin * 2
                rect = option.fontMetrics.boundingRect(
                    QtCore.QRect(0, 0, maxWidth, 10000), 
                    alignment | QtCore.Qt.TextWordWrap, 
                    text)

                # add vertical margins to the resulting height
                height = rect.height() + margin * 2
                if height >= size.height():
                    return QtCore.QSize(rect.width(), height)
        return size

# Main Window
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 - QTableWidget'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show window
        self.show()

    # Create table
    def createTable(self):
        self.tableWidget = QTableWidget()
        # self.tableWidget.setHorizontalHeader(
        #     WrapHeader(QtCore.Qt.Horizontal, self.tableWidget))

        # Row count
        self.tableWidget.setRowCount(3)

        # Column count
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setHorizontalHeaderLabels(["Maximum Variation Coefficient", "Maximum Variation Coefficient"])
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.tableWidget.setItem(0, 0, QTableWidgetItem("3.44"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("5.3"))
        self.tableWidget.setItem(1, 0, QTableWidgetItem("4.6"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("1.2"))
        self.tableWidget.setItem(2, 0, QTableWidgetItem("2.2"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("4.4"))

        # Table will fit the screen horizontally
        
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

        self.tableWidget.setHorizontalHeader(
            WrapHeader(QtCore.Qt.Horizontal, self.tableWidget))
        model = self.tableWidget.model()
        default = self.tableWidget.horizontalHeader().defaultAlignment()
        default |= QtCore.Qt.TextWordWrap
        for col in range(self.tableWidget.columnCount()):
            alignment = model.headerData(
                col, QtCore.Qt.Horizontal, QtCore.Qt.TextAlignmentRole)
            if alignment:
                alignment |= QtCore.Qt.TextWordWrap
            else:
                alignment = default
            model.setHeaderData(
                col, QtCore.Qt.Horizontal, alignment, QtCore.Qt.TextAlignmentRole)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = App()
    sys.exit(app.exec_())