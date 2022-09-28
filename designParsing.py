# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designParsing.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WindowRP5(object):
    def setupUi(self, WindowRP5):
        WindowRP5.setObjectName("WindowRP5")
        WindowRP5.setEnabled(True)
        WindowRP5.resize(469, 428)
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        WindowRP5.setFont(font)
        WindowRP5.setFocusPolicy(QtCore.Qt.NoFocus)
        WindowRP5.setStyleSheet("QMainWindow {\n"
"    background-color: white\n"
"}\n"
"QScrollBar:vertical {              \n"
"    background: #e5e5ea;\n"
"    border-radius: 3;\n"
"    border: none;\n"
"    max-width: 8px;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background-color: #196dff;\n"
"    border-radius: 3;\n"
"}\n"
"QScrollBar::handle:vertical:hover {\n"
"    background-color: #3b83ff; \n"
"    min-height: 0px;\n"
"    border-radius: 3;\n"
"}\n"
"QScrollBar::add-line:vertical {\n"
"    height: 0px;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:vertical {\n"
"    height: 0 px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{\n"
"    background: #e5e5ea;\n"
"    border: none;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    background: transparent;\n"
"    border-radius: 6;\n"
"    border: none;\n"
"    outline:0px;\n"
"    selection-background-color: white;\n"
"    selection-color: #196dff;\n"
"    padding: 8 0 8 0;\n"
"}")
        WindowRP5.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(WindowRP5)
        self.centralwidget.setStyleSheet("background-color: #fff;")
        self.centralwidget.setObjectName("centralwidget")
        self.inputCity = QtWidgets.QLineEdit(self.centralwidget)
        self.inputCity.setGeometry(QtCore.QRect(20, 17, 341, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.inputCity.setFont(font)
        self.inputCity.setStyleSheet("QLineEdit{\n"
"    background-color:rgba(229,229,234,1); \n"
"    border-radius: 6;\n"
"    border: none;\n"
"    padding-left: 8px\n"
"}\n"
"QLineEdit:hover{\n"
"    background-color:rgba(242,242,247,1);\n"
"}\n"
"QLineEdit:pressed{\n"
"    background-color:rgba(188,188,192,1);\n"
"    border-radius: 12;\n"
"}")
        self.inputCity.setInputMask("")
        self.inputCity.setText("")
        self.inputCity.setObjectName("inputCity")
        self.textConsole = QtWidgets.QTextBrowser(self.centralwidget)
        self.textConsole.setEnabled(True)
        self.textConsole.setGeometry(QtCore.QRect(20, 219, 431, 110))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.textConsole.setFont(font)
        self.textConsole.setStyleSheet("QTextBrowser{\n"
"    background-color:rgba(229,229,234,1); \n"
"    border-radius: 6;\n"
"    border: none;\n"
"    padding: 8 4 8 8;\n"
"}\n"
"")
        self.textConsole.setObjectName("textConsole")
        self.btnParse = QtWidgets.QPushButton(self.centralwidget)
        self.btnParse.setGeometry(QtCore.QRect(20, 340, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.btnParse.setFont(font)
        self.btnParse.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnParse.setStyleSheet("QPushButton{\n"
"    background-color: rgba(229,229,234,1);\n"
"    color: #196dff;\n"
"    border: none;\n"
"    border-radius: 12;\n"
"    border-style: outset;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: #dceaff; \n"
"}\n"
"QPushButton:pressed{\n"
"    color: rgba(25, 109, 255, 0.7); \n"
"    border-radius: 12;\n"
"}")
        self.btnParse.setObjectName("btnParse")
        self.btnSearch = QtWidgets.QPushButton(self.centralwidget)
        self.btnSearch.setGeometry(QtCore.QRect(370, 16, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.btnSearch.setFont(font)
        self.btnSearch.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnSearch.setStyleSheet("QPushButton{\n"
"    background-color: #196dff;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 12;\n"
"    border-style: outset;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: #3b83ff; \n"
"}\n"
"QPushButton:pressed{\n"
"    color: rgba(255, 255, 255, 0.7);\n"
"    border-radius: 12;\n"
"}")
        self.btnSearch.setObjectName("btnSearch")
        self.btnDwnld_T = QtWidgets.QPushButton(self.centralwidget)
        self.btnDwnld_T.setGeometry(QtCore.QRect(160, 340, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.btnDwnld_T.setFont(font)
        self.btnDwnld_T.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnDwnld_T.setStyleSheet("QPushButton{\n"
"    background-color: rgb(60,178,0);\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 12;\n"
"    border-style: outset;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgba(60,178,0, 0.85); \n"
"}\n"
"QPushButton:pressed{\n"
"    color: rgba(255, 255, 255, 0.7);\n"
"    border-radius: 12;\n"
"}")
        self.btnDwnld_T.setObjectName("btnDwnld_T")
        self.listCity = QtWidgets.QComboBox(self.centralwidget)
        self.listCity.setGeometry(QtCore.QRect(20, 90, 431, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.listCity.setFont(font)
        self.listCity.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.listCity.setStyleSheet("QComboBox{\n"
"    background-color:rgba(229,229,234,1); \n"
"    border: none;\n"
"    border-radius: 6;\n"
"    padding-left: 8px;\n"
"}\n"
"\n"
"QComboBox:drop-down \n"
"{\n"
"    width: 0px;\n"
"    height: 0px;\n"
"    border: 0px;\n"
"}\n"
"QComboBox:hover{\n"
"    background-color:rgba(242,242,247,1);\n"
"}\n"
"")
        self.listCity.setInputMethodHints(QtCore.Qt.ImhNone)
        self.listCity.setEditable(False)
        self.listCity.setCurrentText("")
        self.listCity.setObjectName("listCity")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setEnabled(True)
        self.label_11.setGeometry(QtCore.QRect(20, 65, 431, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setEnabled(True)
        self.label_9.setGeometry(QtCore.QRect(21, 138, 211, 17))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setEnabled(True)
        self.label_10.setGeometry(QtCore.QRect(239, 138, 211, 17))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.dateEdit_start = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit_start.setGeometry(QtCore.QRect(21, 166, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.dateEdit_start.setFont(font)
        self.dateEdit_start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.dateEdit_start.setStyleSheet("QDateEdit{\n"
"    background-color:rgba(229,229,234,1); \n"
"    border-radius: 6;\n"
"    border: none;\n"
"    padding-left: 8px\n"
"}\n"
"QDateEdit:hover{\n"
"    background-color:rgba(242,242,247,1);\n"
"}\n"
"QDateEdit:pressed{\n"
"    background-color:rgba(188,188,192,1);\n"
"    border-radius: 6;\n"
"}\n"
"QDateEdit:up-button, QDateEdit:down-button{\n"
"    width: 0px;\n"
"    height: 0px;\n"
"    border: 0px;\n"
"}")
        self.dateEdit_start.setAlignment(QtCore.Qt.AlignCenter)
        self.dateEdit_start.setObjectName("dateEdit_start")
        self.dateEdit_end = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit_end.setGeometry(QtCore.QRect(239, 166, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.dateEdit_end.setFont(font)
        self.dateEdit_end.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.dateEdit_end.setMouseTracking(False)
        self.dateEdit_end.setStyleSheet("QDateEdit{\n"
"    background-color:rgba(229,229,234,1); \n"
"    border-radius: 6;\n"
"    border: none;\n"
"    padding-left: 8px\n"
"}\n"
"QDateEdit:hover{\n"
"    background-color:rgba(242,242,247,1);\n"
"}\n"
"QDateEdit:pressed{\n"
"    background-color:rgba(188,188,192,1);\n"
"    border-radius: 6;\n"
"}\n"
"QDateEdit:up-button, QDateEdit:down-button{\n"
"    width: 0px;\n"
"    height: 0px;\n"
"    border: 0px;\n"
"}")
        self.dateEdit_end.setAlignment(QtCore.Qt.AlignCenter)
        self.dateEdit_end.setObjectName("dateEdit_end")
        WindowRP5.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(WindowRP5)
        self.statusBar.setObjectName("statusBar")
        WindowRP5.setStatusBar(self.statusBar)

        self.retranslateUi(WindowRP5)
        QtCore.QMetaObject.connectSlotsByName(WindowRP5)

    def retranslateUi(self, WindowRP5):
        _translate = QtCore.QCoreApplication.translate
        WindowRP5.setWindowTitle(_translate("WindowRP5", "Загрузка погоды"))
        self.inputCity.setPlaceholderText(_translate("WindowRP5", "Название города"))
        self.textConsole.setPlaceholderText(_translate("WindowRP5", "Ход парсинга"))
        self.btnParse.setText(_translate("WindowRP5", "Скачать архив"))
        self.btnSearch.setText(_translate("WindowRP5", "Найти"))
        self.btnDwnld_T.setText(_translate("WindowRP5", " Подгрузить температуру"))
        self.listCity.setProperty("placeholderText", _translate("WindowRP5", "Выберите город из списка"))
        self.label_11.setText(_translate("WindowRP5", "Список городов"))
        self.label_9.setText(_translate("WindowRP5", "Начало выборки"))
        self.label_10.setText(_translate("WindowRP5", "Конец выборки"))
