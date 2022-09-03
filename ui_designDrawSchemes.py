# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\PythonPRJCT\autoReportPdf\designDrawSchemes.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WindowDrawSchemes(object):
    def setupUi(self, WindowDrawSchemes):
        WindowDrawSchemes.setObjectName("WindowDrawSchemes")
        WindowDrawSchemes.setEnabled(True)
        WindowDrawSchemes.resize(767, 458)
        font = QtGui.QFont()
        font.setFamily("Arial")
        WindowDrawSchemes.setFont(font)
        WindowDrawSchemes.setFocusPolicy(QtCore.Qt.NoFocus)
        WindowDrawSchemes.setStyleSheet("QMainWindow {\n"
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
        WindowDrawSchemes.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(WindowDrawSchemes)
        self.centralwidget.setStyleSheet("background-color: #fff;")
        self.centralwidget.setObjectName("centralwidget")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setEnabled(True)
        self.label_8.setGeometry(QtCore.QRect(20, 12, 151, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.inputCount_mppt = QtWidgets.QLineEdit(self.centralwidget)
        self.inputCount_mppt.setGeometry(QtCore.QRect(20, 60, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.inputCount_mppt.setFont(font)
        self.inputCount_mppt.setStyleSheet("QLineEdit{\n"
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
        self.inputCount_mppt.setInputMask("")
        self.inputCount_mppt.setText("")
        self.inputCount_mppt.setPlaceholderText("")
        self.inputCount_mppt.setObjectName("inputCount_mppt")
        self.textConsoleDraw = QtWidgets.QTextBrowser(self.centralwidget)
        self.textConsoleDraw.setEnabled(True)
        self.textConsoleDraw.setGeometry(QtCore.QRect(380, 60, 371, 241))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.textConsoleDraw.setFont(font)
        self.textConsoleDraw.setStyleSheet("QTextBrowser{\n"
"    background-color:rgba(229,229,234,1); \n"
"    border-radius: 6;\n"
"    border: none;\n"
"    padding: 8 4 8 8;\n"
"}\n"
"")
        self.textConsoleDraw.setObjectName("textConsoleDraw")
        self.label_status = QtWidgets.QLabel(self.centralwidget)
        self.label_status.setGeometry(QtCore.QRect(420, 10, 41, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(19)
        self.label_status.setFont(font)
        self.label_status.setText("")
        self.label_status.setObjectName("label_status")
        self.btnDraw = QtWidgets.QPushButton(self.centralwidget)
        self.btnDraw.setGeometry(QtCore.QRect(20, 390, 151, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.btnDraw.setFont(font)
        self.btnDraw.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnDraw.setStyleSheet("QPushButton{\n"
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
        self.btnDraw.setObjectName("btnDraw")
        self.inputCount_input_mppt = QtWidgets.QLineEdit(self.centralwidget)
        self.inputCount_input_mppt.setGeometry(QtCore.QRect(20, 112, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.inputCount_input_mppt.setFont(font)
        self.inputCount_input_mppt.setStyleSheet("QLineEdit{\n"
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
        self.inputCount_input_mppt.setInputMask("")
        self.inputCount_input_mppt.setText("")
        self.inputCount_input_mppt.setPlaceholderText("")
        self.inputCount_input_mppt.setObjectName("inputCount_input_mppt")
        self.inputSolar_count_on_the_chain = QtWidgets.QLineEdit(self.centralwidget)
        self.inputSolar_count_on_the_chain.setGeometry(QtCore.QRect(20, 164, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.inputSolar_count_on_the_chain.setFont(font)
        self.inputSolar_count_on_the_chain.setStyleSheet("QLineEdit{\n"
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
        self.inputSolar_count_on_the_chain.setInputMask("")
        self.inputSolar_count_on_the_chain.setText("")
        self.inputSolar_count_on_the_chain.setPlaceholderText("")
        self.inputSolar_count_on_the_chain.setObjectName("inputSolar_count_on_the_chain")
        self.inputAll_chain = QtWidgets.QLineEdit(self.centralwidget)
        self.inputAll_chain.setGeometry(QtCore.QRect(20, 216, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.inputAll_chain.setFont(font)
        self.inputAll_chain.setStyleSheet("QLineEdit{\n"
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
        self.inputAll_chain.setInputMask("")
        self.inputAll_chain.setText("")
        self.inputAll_chain.setPlaceholderText("")
        self.inputAll_chain.setObjectName("inputAll_chain")
        self.checkUse_y_connector = QtWidgets.QCheckBox(self.centralwidget)
        self.checkUse_y_connector.setGeometry(QtCore.QRect(20, 257, 151, 17))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.checkUse_y_connector.setFont(font)
        self.checkUse_y_connector.setObjectName("checkUse_y_connector")
        self.checkUse_all_mppt = QtWidgets.QCheckBox(self.centralwidget)
        self.checkUse_all_mppt.setGeometry(QtCore.QRect(20, 291, 171, 17))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.checkUse_all_mppt.setFont(font)
        self.checkUse_all_mppt.setStyleSheet("")
        self.checkUse_all_mppt.setObjectName("checkUse_all_mppt")
        self.checkUse_different_mppt = QtWidgets.QCheckBox(self.centralwidget)
        self.checkUse_different_mppt.setGeometry(QtCore.QRect(210, 402, 111, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.checkUse_different_mppt.setFont(font)
        self.checkUse_different_mppt.setObjectName("checkUse_different_mppt")
        self.btnAdd_new_mppt = QtWidgets.QPushButton(self.centralwidget)
        self.btnAdd_new_mppt.setGeometry(QtCore.QRect(320, 397, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btnAdd_new_mppt.setFont(font)
        self.btnAdd_new_mppt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnAdd_new_mppt.setStyleSheet("QPushButton{\n"
"    background-color: rgba(229,229,234,1);\n"
"    color: #196dff;\n"
"    border: none;\n"
"    border-radius: 6;\n"
"    border-style: outset;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: #dceaff; \n"
"}\n"
"QPushButton:pressed{\n"
"    color: rgba(25, 109, 255, 0.7); \n"
"    border-radius: 6;\n"
"}")
        self.btnAdd_new_mppt.setObjectName("btnAdd_new_mppt")
        self.inputName_invertor = QtWidgets.QLineEdit(self.centralwidget)
        self.inputName_invertor.setGeometry(QtCore.QRect(210, 60, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.inputName_invertor.setFont(font)
        self.inputName_invertor.setStyleSheet("QLineEdit{\n"
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
        self.inputName_invertor.setInputMask("")
        self.inputName_invertor.setText("")
        self.inputName_invertor.setPlaceholderText("")
        self.inputName_invertor.setObjectName("inputName_invertor")
        self.inputTitle_grid_line = QtWidgets.QLineEdit(self.centralwidget)
        self.inputTitle_grid_line.setGeometry(QtCore.QRect(210, 164, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.inputTitle_grid_line.setFont(font)
        self.inputTitle_grid_line.setStyleSheet("QLineEdit{\n"
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
        self.inputTitle_grid_line.setInputMask("")
        self.inputTitle_grid_line.setText("")
        self.inputTitle_grid_line.setPlaceholderText("")
        self.inputTitle_grid_line.setObjectName("inputTitle_grid_line")
        self.inputTitle_grid_top = QtWidgets.QLineEdit(self.centralwidget)
        self.inputTitle_grid_top.setGeometry(QtCore.QRect(210, 270, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.inputTitle_grid_top.setFont(font)
        self.inputTitle_grid_top.setStyleSheet("QLineEdit{\n"
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
        self.inputTitle_grid_top.setInputMask("")
        self.inputTitle_grid_top.setText("")
        self.inputTitle_grid_top.setPlaceholderText("")
        self.inputTitle_grid_top.setObjectName("inputTitle_grid_top")
        self.inputNumber_invertor = QtWidgets.QLineEdit(self.centralwidget)
        self.inputNumber_invertor.setGeometry(QtCore.QRect(210, 112, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.inputNumber_invertor.setFont(font)
        self.inputNumber_invertor.setStyleSheet("QLineEdit{\n"
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
        self.inputNumber_invertor.setInputMask("")
        self.inputNumber_invertor.setText("")
        self.inputNumber_invertor.setPlaceholderText("")
        self.inputNumber_invertor.setObjectName("inputNumber_invertor")
        self.inputTitle_grid_switch = QtWidgets.QLineEdit(self.centralwidget)
        self.inputTitle_grid_switch.setGeometry(QtCore.QRect(210, 322, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.inputTitle_grid_switch.setFont(font)
        self.inputTitle_grid_switch.setStyleSheet("QLineEdit{\n"
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
        self.inputTitle_grid_switch.setInputMask("")
        self.inputTitle_grid_switch.setText("")
        self.inputTitle_grid_switch.setPlaceholderText("")
        self.inputTitle_grid_switch.setObjectName("inputTitle_grid_switch")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setEnabled(True)
        self.label_9.setGeometry(QtCore.QRect(210, 10, 111, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.checkUse_CloneInvertor = QtWidgets.QCheckBox(self.centralwidget)
        self.checkUse_CloneInvertor.setGeometry(QtCore.QRect(210, 365, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.checkUse_CloneInvertor.setFont(font)
        self.checkUse_CloneInvertor.setObjectName("checkUse_CloneInvertor")
        self.spinBox_CloneInvertor = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_CloneInvertor.setGeometry(QtCore.QRect(320, 360, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.spinBox_CloneInvertor.setFont(font)
        self.spinBox_CloneInvertor.setStyleSheet("QSpinBox{\n"
"    background-color:rgba(229,229,234,1); \n"
"    border-radius: 6;\n"
"    border: none;\n"
"    padding-left: 8px\n"
"}\n"
"QSpinBox:hover{\n"
"    background-color:rgba(242,242,247,1);\n"
"}\n"
"QSpinBox:up-button:hover{\n"
"    background-color:rgba(25,109,255, 0.7);\n"
"    border-top-right-radius: 6;\n"
"}\n"
"QSpinBox:up-button:pressed{\n"
"    background-color:rgba(25,109,255, 0.5);\n"
"    border-top-right-radius: 6;\n"
"}\n"
"QSpinBox:up-button{\n"
"    background-color:rgba(229,229,234,1); \n"
"    border-top-right-radius: 6;\n"
"    border: none;\n"
"    border-left: 1px solid rgba(0,0,0,0.3);\n"
"}\n"
"\n"
"QSpinBox:down-button:hover{\n"
"    background-color:rgba(25,109,255, 0.7);\n"
"    border-bottom-right-radius: 6;\n"
"}\n"
"QSpinBox:down-button:pressed{\n"
"    background-color:rgba(25,109,255, 0.5);\n"
"    border-bottom-right-radius: 6;\n"
"}\n"
"QSpinBox:down-button{\n"
"    background-color:rgba(229,229,234,1); \n"
"    border-bottom-right-radius: 6;\n"
"    border-left: 1px solid rgba(0,0,0,0.3);\n"
"\n"
"}")
        self.spinBox_CloneInvertor.setObjectName("spinBox_CloneInvertor")
        self.textConsoleMPPT = QtWidgets.QTextBrowser(self.centralwidget)
        self.textConsoleMPPT.setEnabled(True)
        self.textConsoleMPPT.setGeometry(QtCore.QRect(380, 20, 331, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.textConsoleMPPT.setFont(font)
        self.textConsoleMPPT.setStyleSheet("QTextBrowser{\n"
"    background-color:rgba(229,229,234,1); \n"
"    border-radius: 6;\n"
"    border: none;\n"
"    padding-left: 8px;\n"
"    padding-top: 4px;\n"
"}\n"
"")
        self.textConsoleMPPT.setObjectName("textConsoleMPPT")
        self.btnUpdateMppt = QtWidgets.QPushButton(self.centralwidget)
        self.btnUpdateMppt.setGeometry(QtCore.QRect(720, 20, 30, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnUpdateMppt.setFont(font)
        self.btnUpdateMppt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnUpdateMppt.setStyleSheet("QPushButton{\n"
"    background-color: rgba(229,229,234,1);\n"
"    color: #196dff;\n"
"    border: none;\n"
"    border-radius: 6;\n"
"    border-style: outset;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: #dceaff; \n"
"}\n"
"QPushButton:pressed{\n"
"    color: rgba(25, 109, 255, 0.7); \n"
"    border-radius: 6;\n"
"}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("c:\\PythonPRJCT\\autoReportPdf\\Data/icon_update.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnUpdateMppt.setIcon(icon)
        self.btnUpdateMppt.setObjectName("btnUpdateMppt")
        self.btnUpdateConsole = QtWidgets.QPushButton(self.centralwidget)
        self.btnUpdateConsole.setGeometry(QtCore.QRect(720, 60, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnUpdateConsole.setFont(font)
        self.btnUpdateConsole.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnUpdateConsole.setStyleSheet("QPushButton{\n"
"    background-color: rgba(229,229,234,1);\n"
"    color: #196dff;\n"
"    border: none;\n"
"    border-radius: 6;\n"
"    border-style: outset;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: #dceaff; \n"
"}\n"
"QPushButton:pressed{\n"
"    color: rgba(25, 109, 255, 0.7); \n"
"    border-radius: 6;\n"
"}")
        self.btnUpdateConsole.setIcon(icon)
        self.btnUpdateConsole.setObjectName("btnUpdateConsole")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setEnabled(True)
        self.label_10.setGeometry(QtCore.QRect(210, 40, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setEnabled(True)
        self.label_11.setGeometry(QtCore.QRect(20, 40, 151, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setEnabled(True)
        self.label_12.setGeometry(QtCore.QRect(20, 92, 161, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setEnabled(True)
        self.label_13.setGeometry(QtCore.QRect(20, 144, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setEnabled(True)
        self.label_14.setGeometry(QtCore.QRect(20, 196, 171, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setEnabled(True)
        self.label_15.setGeometry(QtCore.QRect(210, 92, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setEnabled(True)
        self.label_16.setGeometry(QtCore.QRect(210, 144, 161, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setEnabled(True)
        self.label_17.setGeometry(QtCore.QRect(210, 250, 151, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setEnabled(True)
        self.label_18.setGeometry(QtCore.QRect(210, 302, 161, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.checkUse_three_phase = QtWidgets.QCheckBox(self.centralwidget)
        self.checkUse_three_phase.setGeometry(QtCore.QRect(20, 326, 171, 17))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.checkUse_three_phase.setFont(font)
        self.checkUse_three_phase.setObjectName("checkUse_three_phase")
        self.checkUse_5or4_line = QtWidgets.QCheckBox(self.centralwidget)
        self.checkUse_5or4_line.setGeometry(QtCore.QRect(20, 360, 171, 17))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.checkUse_5or4_line.setFont(font)
        self.checkUse_5or4_line.setObjectName("checkUse_5or4_line")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setEnabled(True)
        self.label_19.setGeometry(QtCore.QRect(210, 196, 161, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.inputTitle_grid_line_length = QtWidgets.QLineEdit(self.centralwidget)
        self.inputTitle_grid_line_length.setGeometry(QtCore.QRect(210, 216, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.inputTitle_grid_line_length.setFont(font)
        self.inputTitle_grid_line_length.setStyleSheet("QLineEdit{\n"
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
        self.inputTitle_grid_line_length.setInputMask("")
        self.inputTitle_grid_line_length.setText("")
        self.inputTitle_grid_line_length.setPlaceholderText("")
        self.inputTitle_grid_line_length.setObjectName("inputTitle_grid_line_length")
        self.textConsoleCurrent = QtWidgets.QTextBrowser(self.centralwidget)
        self.textConsoleCurrent.setEnabled(True)
        self.textConsoleCurrent.setGeometry(QtCore.QRect(380, 310, 371, 118))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.textConsoleCurrent.setFont(font)
        self.textConsoleCurrent.setStyleSheet("QTextBrowser{\n"
"    background-color:rgba(229,229,234,1); \n"
"    border-radius: 6;\n"
"    border: none;\n"
"    padding: 8 4 8 8;\n"
"}\n"
"")
        self.textConsoleCurrent.setPlaceholderText("")
        self.textConsoleCurrent.setObjectName("textConsoleCurrent")
        self.btnReset = QtWidgets.QPushButton(self.centralwidget)
        self.btnReset.setGeometry(QtCore.QRect(174, 393, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btnReset.setFont(font)
        self.btnReset.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnReset.setStyleSheet("QPushButton{\n"
"    background-color:rgba(112, 215, 255, 0);\n"
"    color:rgba(0, 0, 0, 0.5);\n"
"    border: none;\n"
"    border-radius: 5;\n"
"    border-style: outset;\n"
"}\n"
"QPushButton:hover{\n"
"    color: black;\n"
"}\n"
"")
        self.btnReset.setObjectName("btnReset")
        self.label_8.raise_()
        self.inputCount_mppt.raise_()
        self.textConsoleDraw.raise_()
        self.label_status.raise_()
        self.btnDraw.raise_()
        self.inputCount_input_mppt.raise_()
        self.inputSolar_count_on_the_chain.raise_()
        self.inputAll_chain.raise_()
        self.checkUse_y_connector.raise_()
        self.checkUse_all_mppt.raise_()
        self.checkUse_different_mppt.raise_()
        self.inputName_invertor.raise_()
        self.inputTitle_grid_line.raise_()
        self.inputTitle_grid_top.raise_()
        self.inputNumber_invertor.raise_()
        self.inputTitle_grid_switch.raise_()
        self.label_9.raise_()
        self.checkUse_CloneInvertor.raise_()
        self.spinBox_CloneInvertor.raise_()
        self.textConsoleMPPT.raise_()
        self.btnUpdateMppt.raise_()
        self.btnUpdateConsole.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.label_12.raise_()
        self.label_13.raise_()
        self.label_14.raise_()
        self.label_15.raise_()
        self.label_16.raise_()
        self.label_17.raise_()
        self.label_18.raise_()
        self.checkUse_three_phase.raise_()
        self.checkUse_5or4_line.raise_()
        self.label_19.raise_()
        self.inputTitle_grid_line_length.raise_()
        self.textConsoleCurrent.raise_()
        self.btnReset.raise_()
        self.btnAdd_new_mppt.raise_()
        WindowDrawSchemes.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(WindowDrawSchemes)
        self.statusBar.setObjectName("statusBar")
        WindowDrawSchemes.setStatusBar(self.statusBar)

        self.retranslateUi(WindowDrawSchemes)
        QtCore.QMetaObject.connectSlotsByName(WindowDrawSchemes)

    def retranslateUi(self, WindowDrawSchemes):
        _translate = QtCore.QCoreApplication.translate
        WindowDrawSchemes.setWindowTitle(_translate("WindowDrawSchemes", "Схема инвертора"))
        self.label_8.setText(_translate("WindowDrawSchemes", "MPPT"))
        self.inputCount_mppt.setToolTip(_translate("WindowDrawSchemes", "Количество MPPT в инверторе"))
        self.textConsoleDraw.setPlaceholderText(_translate("WindowDrawSchemes", "Ход построения"))
        self.btnDraw.setText(_translate("WindowDrawSchemes", "Построить"))
        self.inputCount_input_mppt.setToolTip(_translate("WindowDrawSchemes", "Количество входов в одном MPPT"))
        self.inputSolar_count_on_the_chain.setToolTip(_translate("WindowDrawSchemes", "Количество ФЭМ на одну цепочку"))
        self.inputAll_chain.setToolTip(_translate("WindowDrawSchemes", "Общее количество цепочек в инверторе"))
        self.checkUse_y_connector.setToolTip(_translate("WindowDrawSchemes", "Применяет Y конекторы, если это допустимо "))
        self.checkUse_y_connector.setText(_translate("WindowDrawSchemes", "Y коннекторы"))
        self.checkUse_all_mppt.setToolTip(_translate("WindowDrawSchemes", "Распределяет цепочки по всем свободным MPPT, если кол-во цепочек не меньше кол-ва MPPT, если параметр неактивен, то цепочки полностью последовательно заполняют свободные MPPT"))
        self.checkUse_all_mppt.setText(_translate("WindowDrawSchemes", "Цепочки по всем MPPT"))
        self.checkUse_different_mppt.setToolTip(_translate("WindowDrawSchemes", "Позволяет добавлять разные MPPT в инвертор. Нажимая на кнопку \"+\" добавляются параметры для каждого MPPT"))
        self.checkUse_different_mppt.setText(_translate("WindowDrawSchemes", "Разные MPPT"))
        self.btnAdd_new_mppt.setToolTip(_translate("WindowDrawSchemes", "Добавить MPPT"))
        self.btnAdd_new_mppt.setText(_translate("WindowDrawSchemes", "+"))
        self.inputName_invertor.setToolTip(_translate("WindowDrawSchemes", "Название инвертора"))
        self.inputTitle_grid_line.setToolTip(_translate("WindowDrawSchemes", "Наименование расплогаемое на проводе до свича"))
        self.inputTitle_grid_top.setToolTip(_translate("WindowDrawSchemes", "Наименование распологаемое сверху после свича"))
        self.inputNumber_invertor.setToolTip(_translate("WindowDrawSchemes", "Тип инвертора"))
        self.label_9.setText(_translate("WindowDrawSchemes", "Инвертор"))
        self.checkUse_CloneInvertor.setToolTip(_translate("WindowDrawSchemes", "Формирует несколько одинаковых инверторов"))
        self.checkUse_CloneInvertor.setText(_translate("WindowDrawSchemes", "Несколько"))
        self.spinBox_CloneInvertor.setToolTip(_translate("WindowDrawSchemes", "Количество схем одинаковых инверторов"))
        self.textConsoleMPPT.setToolTip(_translate("WindowDrawSchemes", "Каждые 4 цифры - параметры одного MPPT"))
        self.textConsoleMPPT.setPlaceholderText(_translate("WindowDrawSchemes", "Параметры MPPT"))
        self.btnUpdateMppt.setToolTip(_translate("WindowDrawSchemes", "Показать актуальное состояние массива с параметрами MPPT, чтобы проверить какие параметры будут использованы для чертежа (Актуально при добавлении разных MPPT)"))
        self.btnUpdateMppt.setText(_translate("WindowDrawSchemes", "C"))
        self.btnUpdateConsole.setToolTip(_translate("WindowDrawSchemes", "Очистить консоль"))
        self.btnUpdateConsole.setText(_translate("WindowDrawSchemes", "D"))
        self.label_10.setText(_translate("WindowDrawSchemes", "Название"))
        self.label_11.setText(_translate("WindowDrawSchemes", "Кол-во MPPT"))
        self.label_12.setText(_translate("WindowDrawSchemes", "Кол-во входов на 1 MPPT "))
        self.label_13.setText(_translate("WindowDrawSchemes", "Кол-во ФЭМ в цепочке"))
        self.label_14.setText(_translate("WindowDrawSchemes", "Кол-во цепочек"))
        self.label_15.setText(_translate("WindowDrawSchemes", "Тип"))
        self.label_16.setText(_translate("WindowDrawSchemes", "Кабель подключения (к.п.)"))
        self.label_17.setText(_translate("WindowDrawSchemes", "Щитовое оборудование"))
        self.label_18.setText(_translate("WindowDrawSchemes", "Название переключателя"))
        self.checkUse_three_phase.setToolTip(_translate("WindowDrawSchemes", "Позволяет добавлять разные MPPT в инвертор. Нажимая на кнопку \"+\" добавляются параметры для каждого MPPT"))
        self.checkUse_three_phase.setText(_translate("WindowDrawSchemes", "Трёхфазная система"))
        self.checkUse_5or4_line.setToolTip(_translate("WindowDrawSchemes", "Позволяет добавлять разные MPPT в инвертор. Нажимая на кнопку \"+\" добавляются параметры для каждого MPPT"))
        self.checkUse_5or4_line.setText(_translate("WindowDrawSchemes", "Пятипроводная система"))
        self.label_19.setText(_translate("WindowDrawSchemes", "Длина к.п."))
        self.inputTitle_grid_line_length.setToolTip(_translate("WindowDrawSchemes", "Наименование распологаемое сверху после свича"))
        self.btnReset.setToolTip(_translate("WindowDrawSchemes", "Добавить MPPT"))
        self.btnReset.setText(_translate("WindowDrawSchemes", "⭯"))
