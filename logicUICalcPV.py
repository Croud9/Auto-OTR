from email.policy import default
import sys, os   # sys нужен для передачи argv в QApplication
import math
from attr import fields_dict
import xlwt
import requests
import designCalcPV  # Это наш конвертированный файл дизайна
import pandas as pd
import gzip
import search_data
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QRegExpValidator
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer
filepath_to_pan_directory = "Data/PAN_files/"
path_to_pv = "Data/Modules/PV's"

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

class CalcPV(QtWidgets.QMainWindow, designCalcPV.Ui_MainWindow):
    def __init__(self, instance_of_main_window):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('Data/icons/solar-panels.png'))
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.input_data()
        self.validate()
        self.import_sp()
        self.chng(0)
        self.styles()
        self.set_wrap_header_table()
        self.comboBox_city.currentIndexChanged.connect(self.chng)
        self.comboBox_stcnoct.setCurrentIndex(0)
        self.btnResult.clicked.connect(self.cmbBX)
        self.btnSave.clicked.connect(self.savefile)
        self.listPV_folder.activated.connect(self.pv_select)
        self.listPV_file.activated.connect(self.pv_load)
        self.listPV_folder.addItem("Выберите")
        company_pv = sorted(os.listdir(path_to_pv))
        self.listPV_folder.addItems(company_pv)
        self.tableWidget.resize(669,450)
        self.tableWidget.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.resizeColumnsToContents()

    def set_wrap_header_table(self):
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
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

    def styles(self):
        self.default_style_input = 'QLineEdit{ background-color:rgba(229,229,234,1);\
                            border-radius: 6;\
                            border: none;\
                            padding-left: 8px }\
                        QLineEdit:hover{ background-color:rgba(242,242,247,1); }\
                        QLineEdit:pressed{ background-color:rgba(188,188,192,1);\
                            border-radius: 12; }'
        self.default_style_comboBox = 'QComboBox{ background-color:rgba(229,229,234,1);\
                                border: none;\
                                border-radius: 6;\
                                padding-left: 8px;}\
                            QComboBox:drop-down{ width: 0px;\
                                height: 0px;\
                                border: 0px; }\
                            QComboBox:hover{ background-color:rgba(242,242,247,1); }'
        self.warning_style_comboBox = 'QComboBox{background-color:rgba(229,229,234,1);\
                                    border: 1.45px solid red;\
                                    border-radius: 6;\
                                    padding-left: 6.55px;}\
                                QComboBox:drop-down {width: 0px;\
                                    height: 0px;\
                                    border: 0px;}'
        self.warning_style_input = 'border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);'

    def input_data(self):
        self.comboBox_stcnoct.addItem("Выберите систему")
        self.comboBox_stcnoct.addItem("STC")
        self.comboBox_stcnoct.addItem("NOCT")
        self.comboBox_city.addItem("Температура в городе: ")
        self.comboBox_city.setCurrentIndex(0) # видимый в списке элемент
        self.fields_text = [self.lineEdit_calcmintemp, self.lineEdit_calcmaxtemp, self.lineEdit_min, self.lineEdit_max, self.lineEdit_mintemp, 
                            self.lineEdit_countfem, self.lineEdit_countparallel, self.lineEdit_noct, self.lineEdit_irradiance, self.lineEdit_pnom, 
                            self.lineEdit_isc, self.lineEdit_voc, self.lineEdit_imp, self.lineEdit_vmp, self.lineEdit_muisc, self.lineEdit_muvocspec, 
                            self.lineEdit_vmaxiec, self.lineEdit_rshunt, self.lineEdit_ncels, self.lineEdit_umax_pogran, self.lineEdit_imax_pogran]
        
    def import_sp(self):
        nameCity = []
        cols = [0, 5, 17, 22]
        readFrame = pd.read_excel('Data/SP/SP_cold_and_hot.xlsx', usecols=cols, header=5)
        self.spDataFrame = readFrame.dropna()

        for row in self.spDataFrame.itertuples(index=False, name='City'):
            nameCity.append(row[0])
        nameCity.sort()
        self.comboBox_city.addItems(nameCity)

    def chng(self, i):
        currentCity = self.comboBox_city.currentText()
        currentCitydf = self.spDataFrame[self.spDataFrame['City'].str.contains(currentCity)]
        for row in currentCitydf.itertuples(index=False, name='CurrentData'):
            self.lineEdit_min.setText(str(row[3]).replace(",", "."))
            self.lineEdit_max.setText(str(row[1]).replace(",", "."))
            self.lineEdit_mintemp.setText(str(row[2]).replace(",", "."))

    def validate(self):
        reg_ex = QRegExp('^-?(0|[1-9]\d*)(\.[0-9]{1,4})?$')

        for field in self.fields_text:
            field.setValidator(QRegExpValidator(reg_ex, field))

    def cmbBX(self):
        if self.comboBox_stcnoct.currentText() == "Выберите систему":
            self.statusBar.showMessage('Выберите условия расчета!', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.comboBox_stcnoct.setStyleSheet(self.warning_style_comboBox)
        else:
            self.check_imput_params()
            self.comboBox_stcnoct.setStyleSheet(self.default_style_comboBox)

    def red_status(self):
        self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
        QTimer.singleShot(5000, lambda: self.statusBar.setStyleSheet("background-color: rgb(255,255,255)"))

    def valid_input_field(self, field):
        if field.text() == '':
            self.statusBar.showMessage('Введите значение в выделенное поле', 5000)
            self.red_status()
            field.setStyleSheet(self.warning_style_input)
            return False
        else:
            return True

    def check_imput_params(self): #Проверка ввел ли пользователь необходимые значения для расчета
        self.set_style_default()
                
        for field in self.fields_text:        
            if self.valid_input_field(field) == False:
                return
            else:
                self.valid_input_field(field)

        if self.imput_params() == 1:
            return

        if self.comboBox_stcnoct.currentText() == "STC":
            self.resultStc()
            self.statusBar.showMessage('Расчет выполнился при STC ', 10000)
        elif self.comboBox_stcnoct.currentText() == "NOCT":
            self.resultNoct()
            self.statusBar.showMessage('Расчет выполнился при NOCT ', 10000)
        # self.tableWidget.resizeColumnsToContents()
        self.set_style_default()
             
    def set_style_default(self):      
        self.lineEdit_calcmintemp.setStyleSheet(self.default_style_input)
        self.lineEdit_calcmaxtemp.setStyleSheet(self.default_style_input)
        self.lineEdit_min.setStyleSheet(self.default_style_input)
        self.lineEdit_max.setStyleSheet(self.default_style_input)
        self.lineEdit_mintemp.setStyleSheet(self.default_style_input)
        self.lineEdit_countfem.setStyleSheet(self.default_style_input)
        self.lineEdit_countparallel.setStyleSheet(self.default_style_input)
        self.lineEdit_noct.setStyleSheet(self.default_style_input)
        self.lineEdit_irradiance.setStyleSheet(self.default_style_input)
        self.lineEdit_pnom.setStyleSheet(self.default_style_input) #PAN or imput
        self.lineEdit_isc.setStyleSheet(self.default_style_input)
        self.lineEdit_voc.setStyleSheet(self.default_style_input)
        self.lineEdit_imp.setStyleSheet(self.default_style_input)
        self.lineEdit_vmp.setStyleSheet(self.default_style_input)
        self.lineEdit_muisc.setStyleSheet(self.default_style_input)
        self.lineEdit_muvocspec.setStyleSheet(self.default_style_input)
        self.lineEdit_vmaxiec.setStyleSheet(self.default_style_input)
        self.lineEdit_rshunt.setStyleSheet(self.default_style_input)
        self.lineEdit_ncels.setStyleSheet(self.default_style_input)
        self.lineEdit_umax_pogran.setStyleSheet(self.default_style_input)
        self.lineEdit_imax_pogran.setStyleSheet(self.default_style_input)

    def pv_select(self):
        self.listPV_file.clear()
        if self.listPV_folder.currentText() != "Выберите":
            self.select_title_pv = self.listPV_folder.currentText() 
            modules_file = f'{path_to_pv}/{self.select_title_pv}'
            self.type_pv_modules = sorted(os.listdir(modules_file))
            names_modules = []
            for name in self.type_pv_modules:
                names_modules.append(name.split(".")[0])
            self.listPV_file.addItems(names_modules)

    def pv_load(self):
        current_pv = self.listPV_file.currentText()
        for select_pv in self.type_pv_modules:
            if current_pv in select_pv: 
                self.found_pv = search_data.search_in_pv(f"{path_to_pv}/{self.select_title_pv}/{select_pv}") 
                self.lineEdit_pnom.setText(str(self.found_pv['p_nom_pv'])) #вывод в программу данных из файла
                self.lineEdit_isc.setText(str(self.found_pv['isc_pv']))
                self.lineEdit_voc.setText(str(self.found_pv['voc_pv']))
                self.lineEdit_imp.setText(str(self.found_pv['imp_pv']))
                self.lineEdit_vmp.setText(str(self.found_pv['vmp_pv']))
                self.lineEdit_muisc.setText(str(self.found_pv['mu_isc_pv']))
                self.lineEdit_muvocspec.setText(str(self.found_pv['mu_voc_spec_pv']))
                self.lineEdit_vmaxiec.setText(str(self.found_pv['v_max_iec_pv']))
                self.lineEdit_rshunt.setText(str(self.found_pv['r_shunt_pv']))
                self.lineEdit_ncels.setText(str(self.found_pv['ncels_pv']))    

    def imput_params(self): #считывание вводимых данных
        self.calcmintemp = float(self.lineEdit_calcmintemp.text()) #считывание данных, которые вводит пользователь
        self.calcmaxtemp = float(self.lineEdit_calcmaxtemp.text())
        self.min_v = float(self.lineEdit_min.text())
        self.max_v = float(self.lineEdit_max.text())
        self.mintemp = float(self.lineEdit_mintemp.text())
        self.countfem = float(self.lineEdit_countfem.text())
        self.countparallel = float(self.lineEdit_countparallel.text())
        self.irradiance = float(self.lineEdit_irradiance.text())
        if self.comboBox_stcnoct.currentText() == "NOCT":
            self.noct = float(self.lineEdit_noct.text())
        self.numpnom = float(self.lineEdit_pnom.text())
        self.numisc = float(self.lineEdit_isc.text())
        self.numvoc = float(self.lineEdit_voc.text())
        self.numimp = float(self.lineEdit_imp.text())
        self.numvmp = float(self.lineEdit_vmp.text())
        try:
            self.nummuisc = float(self.lineEdit_muisc.text())
        except ValueError:
            self.statusBar.showMessage('Недопустимое значение в muISC', 10000 )
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            return 1
        self.nummuvocspec = float(self.lineEdit_muvocspec.text())
        self.numvmaxiec = float(self.lineEdit_vmaxiec.text())
        self.numrshunt = float(self.lineEdit_rshunt.text())
        self.numncels = float(self.lineEdit_ncels.text())
        self.umaxpogran = float(self.lineEdit_umax_pogran.text())  #ПОГРАНИЧНЫЕ ЗНАЧЕНИЯ
        self.imaxpogran = float(self.lineEdit_imax_pogran.text())
        return 0

    def paint_borderline(self):
        setRedColor = QtGui.QBrush(QtGui.QColor(255, 114, 89)) # задание красного цвета ячейке
        setGreenColor = QtGui.QBrush(QtGui.QColor(51, 255, 146)) # задание зеленого цвета ячейке
        for i in range(self.tableWidget.rowCount()):
            data = self.tableWidget.item(i, 5)
            if not data: continue
            if self.tableWidget.item(i, 5).text() == '': continue
            cleardata = float(data.text())
            if cleardata > self.umaxpogran:
                data.setBackground(setRedColor)
            elif cleardata < self.umaxpogran:
                data.setBackground(setGreenColor)

        for i in range(self.tableWidget.rowCount()):
            data = self.tableWidget.item(i, 6)
            if not data: continue
            if self.tableWidget.item(i, 6).text() == '': continue
            cleardata = float(data.text())
            if cleardata > self.imaxpogran:
                data.setBackground(setRedColor)
            elif cleardata < self.imaxpogran:
                data.setBackground(setGreenColor)

    def resultStc(self):
        print(" !STC!")
        print("NCels = ", self.numncels)
        # self.imput_params()
#метод 1-1
        metdI1 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (self.calcmintemp - 25)))#расчет А 1 метод
        metdU1 = self.numvoc + (self.nummuvocspec * (self.calcmintemp - 25)) #расчет V
        metdImp1 = (self.irradiance/1000) * (self.numimp + (self.nummuisc * (self.calcmintemp - 25)))#расчет А 1 метод
        metdUmp1 = self.numvmp + (self.nummuvocspec * (self.calcmintemp - 25)) #расчет V
        p1 = metdImp1 * metdUmp1 #расчет мощности
        fem1 = metdU1 * self.countfem
        prll1 = metdI1 * self.countparallel

        metdI12 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (self.calcmaxtemp - 25)))
        metdU12 = self.numvoc + (self.nummuvocspec * (self.calcmaxtemp - 25))
        metdImp12 = (self.irradiance/1000) * (self.numimp + (self.nummuisc * (self.calcmaxtemp - 25)))#расчет А 1 метод
        metdUmp12 = self.numvmp + (self.nummuvocspec * (self.calcmaxtemp - 25)) #расчет V
        p2 = metdImp12 * metdUmp12
        fem12 = metdU12 * self.countfem
        prll12 = metdI12 * self.countparallel

        metdI13 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (self.min_v - 25)))
        metdU13 = self.numvoc + (self.nummuvocspec * (self.min_v - 25))
        metdImp13 = (self.irradiance/1000) * (self.numimp + (self.nummuisc * (self.min_v - 25)))#расчет А 1 метод
        metdUmp13 = self.numvmp + (self.nummuvocspec * (self.min_v - 25)) #расчет V
        p3 = metdImp13 * metdUmp13
        fem13 = metdU13 * self.countfem
        prll13 = metdI13 * self.countparallel

        metdI14 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (self.max_v - 25)))
        metdU14 = self.numvoc + (self.nummuvocspec * (self.max_v - 25))
        metdImp14 = (self.irradiance/1000) * (self.numimp + (self.nummuisc * (self.max_v - 25)))#расчет А 1 метод
        metdUmp14 = self.numvmp + (self.nummuvocspec * (self.max_v - 25)) #расчет V
        p4 = metdImp14 * metdUmp14
        fem14 = metdU14 * self.countfem
        prll14 = metdI14 * self.countparallel

        metdI15 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (self.mintemp - 25)))
        metdU15 = self.numvoc + (self.nummuvocspec * (self.mintemp - 25))
        metdImp15 = (self.irradiance/1000) * (self.numimp + (self.nummuisc * (self.mintemp - 25)))#расчет А 1 метод
        metdUmp15 = self.numvmp + (self.nummuvocspec * (self.mintemp - 25)) #расчет V
        p5 = metdImp15 * metdUmp15
        fem15 = metdU15 * self.countfem
        prll15 = metdI15 * self.countparallel

        # вывод результатов расчета метода 1 для разных температур
        self.tableWidget.item(0, 0).setText(str(round(metdI1, 3)))
        self.tableWidget.item(0, 1).setText(str(round(metdU1, 3)))
        self.tableWidget.item(0, 2).setText(str(round(p1, 3)))
        self.tableWidget.item(0, 3).setText(str(self.calcmintemp))
        self.tableWidget.item(0, 5).setText(str(round(fem1, 3)))
        self.tableWidget.item(0, 6).setText(str(round(prll1, 3)))

        self.tableWidget.item(1, 0).setText(str(round(metdI12, 3)))
        self.tableWidget.item(1, 1).setText(str(round(metdU12, 3)))
        self.tableWidget.item(1, 2).setText(str(round(p2, 3)))
        self.tableWidget.item(1, 3).setText(str(self.calcmaxtemp))
        self.tableWidget.item(1, 5).setText(str(round(fem12, 3)))
        self.tableWidget.item(1, 6).setText(str(round(prll12, 3)))

        self.tableWidget.item(2, 0).setText(str(round(metdI13, 3)))
        self.tableWidget.item(2, 1).setText(str(round(metdU13, 3)))
        self.tableWidget.item(2, 2).setText(str(round(p3, 3)))
        self.tableWidget.item(2, 3).setText(str(self.min_v))
        self.tableWidget.item(2, 5).setText(str(round(fem13, 3)))
        self.tableWidget.item(2, 6).setText(str(round(prll13, 3)))

        self.tableWidget.item(3, 0).setText(str(round(metdI14, 3)))
        self.tableWidget.item(3, 1).setText(str(round(metdU14, 3)))
        self.tableWidget.item(3, 2).setText(str(round(p4, 3)))
        self.tableWidget.item(3, 3).setText(str(self.max_v))
        self.tableWidget.item(3, 5).setText(str(round(fem14, 3)))
        self.tableWidget.item(3, 6).setText(str(round(prll14, 3)))

        self.tableWidget.item(4, 0).setText(str(round(metdI15, 3)))
        self.tableWidget.item(4, 1).setText(str(round(metdU15, 3)))
        self.tableWidget.item(4, 2).setText(str(round(p5, 3)))
        self.tableWidget.item(4, 3).setText(str(self.mintemp))
        self.tableWidget.item(4, 5).setText(str(round(fem15, 3)))
        self.tableWidget.item(4, 6).setText(str(round(prll15, 3)))

# метод 1-3
        q = 1.602 * pow(10, -19)
        k = 1.3806503 * pow(10, -23)
        logirradiance = math.log(self.irradiance/1000)

        metdU31 = self.numvoc + (((self.numncels * k * (273 + self.calcmintemp) * 1)/q) * logirradiance) + (self.nummuvocspec * (self.calcmintemp - 25)) #расчет V
        metdUmp31 = self.numvmp + (((self.numncels * k * (273 + self.calcmintemp) * 1)/q) * logirradiance) + (self.nummuvocspec * (self.calcmintemp - 25)) #расчет V
        p11 = metdImp1 * metdUmp31 #расчет мощности

        metdU32 = self.numvoc + (((self.numncels * k * (273 + self.calcmaxtemp) * 1)/q) * logirradiance) + (self.nummuvocspec * (self.calcmaxtemp - 25))
        metdUmp32 = self.numvmp + (((self.numncels * k * (273 + self.calcmaxtemp) * 1)/q) * logirradiance) + (self.nummuvocspec * (self.calcmaxtemp - 25)) #расчет V
        p12 = metdImp12 * metdUmp32

        metdU33 = self.numvoc + (((self.numncels * k * (273 + self.min_v) * 1)/q) * logirradiance) + (self.nummuvocspec * (self.min_v - 25))
        metdUmp33 = self.numvmp + (((self.numncels * k * (273 + self.min_v) * 1)/q) * logirradiance) + (self.nummuvocspec * (self.min_v - 25)) #расчет V
        p13 = metdImp13 * metdUmp33

        metdU34 = self.numvoc + (((self.numncels * k * (273 + self.max_v) * 1)/q) * logirradiance) + (self.nummuvocspec * (self.max_v - 25))
        metdUmp34 = self.numvmp + (((self.numncels * k * (273 + self.max_v) * 1)/q) * logirradiance) + (self.nummuvocspec * (self.max_v - 25)) #расчет V
        p14 = metdImp14 * metdUmp34

        metdU35 = self.numvoc + (((self.numncels * k * (273 + self.mintemp) * 1)/q) * logirradiance) + (self.nummuvocspec * (self.mintemp - 25))
        metdUmp35 = self.numvmp + (((self.numncels * k * (273 + self.mintemp) * 1)/q) * logirradiance) + (self.nummuvocspec * (self.mintemp - 25)) #расчет V
        p15 = metdImp15 * metdUmp35

        self.tableWidget.item(6, 0).setText(str(round(metdI1, 3)))
        self.tableWidget.item(6, 1).setText(str(round(metdU31, 3)))
        self.tableWidget.item(6, 2).setText(str(round(p11, 3)))
        self.tableWidget.item(6, 3).setText(str(self.calcmintemp))

        self.tableWidget.item(7, 0).setText(str(round(metdI12, 3)))
        self.tableWidget.item(7, 1).setText(str(round(metdU32, 3)))
        self.tableWidget.item(7, 2).setText(str(round(p12, 3)))
        self.tableWidget.item(7, 3).setText(str(self.calcmaxtemp))

        self.tableWidget.item(8, 0).setText(str(round(metdI13, 3)))
        self.tableWidget.item(8, 1).setText(str(round(metdU33, 3)))
        self.tableWidget.item(8, 2).setText(str(round(p13, 3)))
        self.tableWidget.item(8, 3).setText(str(self.min_v))

        self.tableWidget.item(9, 0).setText(str(round(metdI14, 3)))
        self.tableWidget.item(9, 1).setText(str(round(metdU34, 3)))
        self.tableWidget.item(9, 2).setText(str(round(p14, 3)))
        self.tableWidget.item(9, 3).setText(str(self.max_v))

        self.tableWidget.item(10, 0).setText(str(round(metdI15, 3)))
        self.tableWidget.item(10, 1).setText(str(round(metdU35, 3)))
        self.tableWidget.item(10, 2).setText(str(round(p15, 3)))
        self.tableWidget.item(10, 3).setText(str(self.mintemp))

        fem31 = metdU31 * self.countfem
        prll31 = metdI1 * self.countparallel
        fem32 = metdU32 * self.countfem
        prll32 = metdI12 * self.countparallel
        fem33 = metdU33 * self.countfem
        prll33 = metdI13 * self.countparallel
        fem34 = metdU34 * self.countfem
        prll34 = metdI14 * self.countparallel
        fem35 = metdU35 * self.countfem
        prll35 = metdI15 * self.countparallel
        self.tableWidget.item(6, 5).setText(str(round(fem31, 3)))
        self.tableWidget.item(6, 6).setText(str(round(prll31, 3)))
        self.tableWidget.item(7, 5).setText(str(round(fem32, 3)))
        self.tableWidget.item(7, 6).setText(str(round(prll32, 3)))
        self.tableWidget.item(8, 5).setText(str(round(fem33, 3)))
        self.tableWidget.item(8, 6).setText(str(round(prll33, 3)))
        self.tableWidget.item(9, 5).setText(str(round(fem34, 3)))
        self.tableWidget.item(9, 6).setText(str(round(prll34, 3)))
        self.tableWidget.item(10, 5).setText(str(round(fem35, 3)))
        self.tableWidget.item(10, 6).setText(str(round(prll35, 3)))

# метод 1-4
        c1 = 5.468511 * pow(10, -2)
        c2 = 5.973869 * pow(10, -3)
        c3 = 7.616178 * pow(10, -4)
        metdU41 = self.numvoc + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (self.calcmintemp - 25)) #расчет V
        metdUmp41 = self.numvmp + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (self.calcmintemp - 25)) #расчет V
        p16 = metdImp1 * metdUmp41 #расчет мощности

        metdU42 = self.numvoc + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (self.calcmaxtemp - 25))
        metdUmp42 = self.numvmp + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (self.calcmaxtemp - 25)) #расчет V
        p17 = metdImp12 * metdUmp42

        metdU43 = self.numvoc + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (self.min_v - 25))
        metdUmp43 = self.numvmp + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (self.min_v - 25)) #расчет V
        p18 = metdImp13 * metdUmp43

        metdU44 = self.numvoc + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (self.max_v - 25))
        metdUmp44 = self.numvmp + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (self.max_v - 25)) #расчет V
        p19 = metdImp14 * metdUmp44

        metdU45 = self.numvoc + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (self.mintemp - 25))
        metdUmp45 = self.numvmp + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (self.mintemp - 25)) #расчет V
        p20 = metdImp15 * metdUmp45

        self.tableWidget.item(12, 0).setText(str(round(metdI1, 3)))
        self.tableWidget.item(12, 1).setText(str(round(metdU41, 3)))
        self.tableWidget.item(12, 2).setText(str(round(p16, 3)))
        self.tableWidget.item(12, 3).setText(str(self.calcmintemp))

        self.tableWidget.item(13, 0).setText(str(round(metdI12, 3)))
        self.tableWidget.item(13, 1).setText(str(round(metdU42, 3)))
        self.tableWidget.item(13, 2).setText(str(round(p17, 3)))
        self.tableWidget.item(13, 3).setText(str(self.calcmaxtemp))

        self.tableWidget.item(14, 0).setText(str(round(metdI13, 3)))
        self.tableWidget.item(14, 1).setText(str(round(metdU43, 3)))
        self.tableWidget.item(14, 2).setText(str(round(p18, 3)))
        self.tableWidget.item(14, 3).setText(str(self.min_v))

        self.tableWidget.item(15, 0).setText(str(round(metdI14, 3)))
        self.tableWidget.item(15, 1).setText(str(round(metdU44, 3)))
        self.tableWidget.item(15, 2).setText(str(round(p19, 3)))
        self.tableWidget.item(15, 3).setText(str(self.max_v))

        self.tableWidget.item(16, 0).setText(str(round(metdI15, 3)))
        self.tableWidget.item(16, 1).setText(str(round(metdU45, 3)))
        self.tableWidget.item(16, 2).setText(str(round(p20, 3)))
        self.tableWidget.item(16, 3).setText(str(self.mintemp))

        fem41 = metdU41 * self.countfem
        prll41 = metdI1 * self.countparallel
        fem42 = metdU42 * self.countfem
        prll42 = metdI12 * self.countparallel
        fem43 = metdU43 * self.countfem
        prll43 = metdI13 * self.countparallel
        fem44 = metdU44 * self.countfem
        prll44 = metdI14 * self.countparallel
        fem45 = metdU45 * self.countfem
        prll45 = metdI15 * self.countparallel
        self.tableWidget.item(12, 5).setText(str(round(fem41, 3)))
        self.tableWidget.item(12, 6).setText(str(round(prll41, 3)))
        self.tableWidget.item(13, 5).setText(str(round(fem42, 3)))
        self.tableWidget.item(13, 6).setText(str(round(prll42, 3)))
        self.tableWidget.item(14, 5).setText(str(round(fem43, 3)))
        self.tableWidget.item(14, 6).setText(str(round(prll43, 3)))
        self.tableWidget.item(15, 5).setText(str(round(fem44, 3)))
        self.tableWidget.item(15, 6).setText(str(round(prll44, 3)))
        self.tableWidget.item(16, 5).setText(str(round(fem45, 3)))
        self.tableWidget.item(16, 6).setText(str(round(prll45, 3)))

# метод 1-5                                                                                                                             логарифмы от отрицательных чисел!!
        # metdU51 = (self.numvoc/1 + ((((self.numvoc/metdU1) - 1) / math.log(1000/self.irradiance)) * math.log(1000/self.irradiance))) * (25/self.calcmintemp)**(math.log(self.numvoc/metdU1) / math.log(self.calcmintemp/25))
        # p21 = metdI1 * metdU51 #расчет мощности
        #
        # metdU52 = (self.numvoc/1 + ((((self.numvoc/metdU12) - 1) / math.log(1000/self.irradiance)) * math.log(1000/self.irradiance))) * (25/self.calcmaxtemp)**(math.log(self.numvoc/metdU12) / math.log(self.calcmaxtemp/25))
        # p22 = metdI12 * metdU52
        #
        # metdU53 = (self.numvoc/1 + ((((self.numvoc/metdU13) - 1) / math.log(1000/self.irradiance)) * math.log(1000/self.irradiance))) * (25/self.min_v)**(math.log(self.numvoc/metdU13) / math.log(self.min_v/25))
        # p23 = metdI13 * metdU53
        #
        # metdU54 = (self.numvoc/1 + ((((self.numvoc/metdU14) - 1) / math.log(1000/self.irradiance)) * math.log(1000/self.irradiance))) * (25/self.max_v)**(math.log(self.numvoc/metdU14) / math.log(self.max_v/25))
        # p24 = metdI14 * metdU54
        #
        # metdU55 = (self.numvoc/1 + ((((self.numvoc/metdU15) - 1) / math.log(1000/self.irradiance)) * math.log(1000/self.irradiance))) * (25/self.mintemp)**(math.log(self.numvoc/metdU15) / math.log(self.mintemp/25))
        # p25 = metdI15 * metdU55
        #
        # self.tableWidget.item(18, 0).setText(str(round(metdI1, 3)))
        # self.tableWidget.item(18, 1).setText(str(round(metdU51, 3)))
        # self.tableWidget.item(18, 2).setText(str(round(p21, 3)))
        # self.tableWidget.item(18, 3).setText(str(self.calcmintemp))
        #
        # self.tableWidget.item(19, 0).setText(str(round(metdI12, 3)))
        # self.tableWidget.item(19, 1).setText(str(round(metdU52, 3)))
        # self.tableWidget.item(19, 2).setText(str(round(p22, 3)))
        # self.tableWidget.item(19, 3).setText(str(self.calcmaxtemp))
        #
        # self.tableWidget.item(20, 0).setText(str(round(metdI13, 3)))
        # self.tableWidget.item(20, 1).setText(str(round(metdU53, 3)))
        # self.tableWidget.item(20, 2).setText(str(round(p23, 3)))
        # self.tableWidget.item(20, 3).setText(str(self.min_v))
        #
        # self.tableWidget.item(21, 0).setText(str(round(metdI14, 3)))
        # self.tableWidget.item(21, 1).setText(str(round(metdU54, 3)))
        # self.tableWidget.item(21, 2).setText(str(round(p24, 3)))
        # self.tableWidget.item(21, 3).setText(str(self.max_v))
        #
        # self.tableWidget.item(22, 0).setText(str(round(metdI15, 3)))
        # self.tableWidget.item(22, 1).setText(str(round(metdU55, 3)))
        # self.tableWidget.item(22, 2).setText(str(round(p25, 3)))
        # self.tableWidget.item(22, 3).setText(str(self.mintemp))

# 2
# метод 2-1
        if self.irradiance == 1000:
            metdI2 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (self.calcmintemp - 25)))#расчет А 1 метод
            metdI22 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (self.calcmaxtemp - 25)))
            metdI23 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (self.min_v - 25)))
            metdI24 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (self.max_v - 25)))
            metdI25 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (self.mintemp - 25)))

            metdImp2 = (self.irradiance/1000) * (self.numimp + (self.nummuisc * (self.calcmintemp - 25)))#расчет А 1 метод
            metdImp22 = (self.irradiance/1000) * (self.numimp + (self.nummuisc * (self.calcmaxtemp - 25)))
            metdImp23 = (self.irradiance/1000) * (self.numimp + (self.nummuisc * (self.min_v - 25)))
            metdImp24 = (self.irradiance/1000) * (self.numimp+ (self.nummuisc * (self.max_v - 25)))
            metdImp25 = (self.irradiance/1000) * (self.numimp + (self.nummuisc * (self.mintemp - 25)))
        else:
            iscG = (self.irradiance/1000) * self.numisc
            a = float((math.log(self.numisc/iscG))/(math.log(1000/self.irradiance)))
            print("a =",a)
            metdI2 = ((self.irradiance/1000)**a) * (self.numisc + (self.nummuisc * (self.calcmintemp - 25))) #расчет А 2 метод
            metdI22 = ((self.irradiance/1000)**a) * (self.numisc + (self.nummuisc * (self.calcmaxtemp - 25)))
            metdI23 = ((self.irradiance/1000)**a) * (self.numisc + (self.nummuisc * (self.min_v - 25)))
            metdI24 = ((self.irradiance/1000)**a) * (self.numisc + (self.nummuisc * (self.max_v - 25)))
            metdI25 = ((self.irradiance/1000)**a) * (self.numisc + (self.nummuisc * (self.mintemp - 25)))

            iscmpG = (self.irradiance/1000) * self.numimp
            amp = float((math.log(self.numimp/iscmpG))/(math.log(1000/self.irradiance)))
            print("a =",amp)
            metdImp2 = ((self.irradiance/1000)**amp) * (self.numimp + (self.nummuisc * (self.calcmintemp - 25))) #расчет А 2 метод
            metdImp22 = ((self.irradiance/1000)**amp) * (self.numimp + (self.nummuisc * (self.calcmaxtemp - 25)))
            metdImp23 = ((self.irradiance/1000)**amp) * (self.numimp + (self.nummuisc * (self.min_v - 25)))
            metdImp24 = ((self.irradiance/1000)**amp) * (self.numimp + (self.nummuisc * (self.max_v - 25)))
            metdImp25 = ((self.irradiance/1000)**amp) * (self.numimp + (self.nummuisc * (self.mintemp - 25)))

        p26 = metdImp2 * metdUmp1 #расчет мощности
        p27 = metdImp22 * metdUmp12
        p28 = metdImp23 * metdUmp13
        p29 = metdImp24 * metdUmp14
        p30 = metdImp25 * metdUmp15

        # вывод результатов расчета метода 1 для разных температур
        self.tableWidget.item(24, 0).setText(str(round(metdI2, 3)))
        self.tableWidget.item(24, 1).setText(str(round(metdU1, 3)))
        self.tableWidget.item(24, 2).setText(str(round(p26, 3)))
        self.tableWidget.item(24, 3).setText(str(self.calcmintemp))

        self.tableWidget.item(25, 0).setText(str(round(metdI22, 3)))
        self.tableWidget.item(25, 1).setText(str(round(metdU12, 3)))
        self.tableWidget.item(25, 2).setText(str(round(p27, 3)))
        self.tableWidget.item(25, 3).setText(str(self.calcmaxtemp))

        self.tableWidget.item(26, 0).setText(str(round(metdI23, 3)))
        self.tableWidget.item(26, 1).setText(str(round(metdU13, 3)))
        self.tableWidget.item(26, 2).setText(str(round(p28, 3)))
        self.tableWidget.item(26, 3).setText(str(self.min_v))

        self.tableWidget.item(27, 0).setText(str(round(metdI24, 3)))
        self.tableWidget.item(27, 1).setText(str(round(metdU14, 3)))
        self.tableWidget.item(27, 2).setText(str(round(p29, 3)))
        self.tableWidget.item(27, 3).setText(str(self.max_v))

        self.tableWidget.item(28, 0).setText(str(round(metdI25, 3)))
        self.tableWidget.item(28, 1).setText(str(round(metdU15, 3)))
        self.tableWidget.item(28, 2).setText(str(round(p30, 3)))
        self.tableWidget.item(28, 3).setText(str(self.mintemp))

        prll21 = metdI2 * self.countparallel
        prll22 = metdI22 * self.countparallel
        prll23 = metdI23 * self.countparallel
        prll24 = metdI24 * self.countparallel
        prll25 = metdI25 * self.countparallel

        self.tableWidget.item(24, 5).setText(str(round(fem1, 3)))
        self.tableWidget.item(24, 6).setText(str(round(prll21, 3)))
        self.tableWidget.item(25, 5).setText(str(round(fem12, 3)))
        self.tableWidget.item(25, 6).setText(str(round(prll22, 3)))
        self.tableWidget.item(26, 5).setText(str(round(fem13, 3)))
        self.tableWidget.item(26, 6).setText(str(round(prll23, 3)))
        self.tableWidget.item(27, 5).setText(str(round(fem14, 3)))
        self.tableWidget.item(27, 6).setText(str(round(prll24, 3)))
        self.tableWidget.item(28, 5).setText(str(round(fem15, 3)))
        self.tableWidget.item(28, 6).setText(str(round(prll25, 3)))

# метод 2-3
        p36 = metdImp2 * metdUmp31 #расчет мощности
        p37 = metdImp22 * metdUmp32
        p38 = metdImp23 * metdUmp33
        p39 = metdImp24 * metdUmp34
        p40 = metdImp25 * metdUmp35

        # вывод результатов расчета метода 1 для разных температур
        self.tableWidget.item(30, 0).setText(str(round(metdI2, 3)))
        self.tableWidget.item(30, 1).setText(str(round(metdU31, 3)))
        self.tableWidget.item(30, 2).setText(str(round(p36, 3)))
        self.tableWidget.item(30, 3).setText(str(self.calcmintemp))

        self.tableWidget.item(31, 0).setText(str(round(metdI22, 3)))
        self.tableWidget.item(31, 1).setText(str(round(metdU32, 3)))
        self.tableWidget.item(31, 2).setText(str(round(p37, 3)))
        self.tableWidget.item(31, 3).setText(str(self.calcmaxtemp))

        self.tableWidget.item(32, 0).setText(str(round(metdI23, 3)))
        self.tableWidget.item(32, 1).setText(str(round(metdU33, 3)))
        self.tableWidget.item(32, 2).setText(str(round(p38, 3)))
        self.tableWidget.item(32, 3).setText(str(self.min_v))

        self.tableWidget.item(33, 0).setText(str(round(metdI24, 3)))
        self.tableWidget.item(33, 1).setText(str(round(metdU34, 3)))
        self.tableWidget.item(33, 2).setText(str(round(p39, 3)))
        self.tableWidget.item(33, 3).setText(str(self.max_v))

        self.tableWidget.item(34, 0).setText(str(round(metdI25, 3)))
        self.tableWidget.item(34, 1).setText(str(round(metdU35, 3)))
        self.tableWidget.item(34, 2).setText(str(round(p40, 3)))
        self.tableWidget.item(34, 3).setText(str(self.mintemp))

        self.tableWidget.item(30, 5).setText(str(round(fem31, 3)))
        self.tableWidget.item(30, 6).setText(str(round(prll21, 3)))
        self.tableWidget.item(31, 5).setText(str(round(fem32, 3)))
        self.tableWidget.item(31, 6).setText(str(round(prll22, 3)))
        self.tableWidget.item(32, 5).setText(str(round(fem33, 3)))
        self.tableWidget.item(32, 6).setText(str(round(prll23, 3)))
        self.tableWidget.item(33, 5).setText(str(round(fem34, 3)))
        self.tableWidget.item(33, 6).setText(str(round(prll24, 3)))
        self.tableWidget.item(34, 5).setText(str(round(fem35, 3)))
        self.tableWidget.item(34, 6).setText(str(round(prll25, 3)))

# метод 2-4
        p41 = metdImp2 * metdUmp41 #расчет мощности
        p42 = metdImp22 * metdUmp42
        p43 = metdImp23 * metdUmp43
        p44 = metdImp24 * metdUmp44
        p45 = metdImp25 * metdUmp45

        # вывод результатов расчета метода 1 для разных температур
        self.tableWidget.item(36, 0).setText(str(round(metdI2, 3)))
        self.tableWidget.item(36, 1).setText(str(round(metdU41, 3)))
        self.tableWidget.item(36, 2).setText(str(round(p41, 3)))
        self.tableWidget.item(36, 3).setText(str(self.calcmintemp))

        self.tableWidget.item(37, 0).setText(str(round(metdI22, 3)))
        self.tableWidget.item(37, 1).setText(str(round(metdU42, 3)))
        self.tableWidget.item(37, 2).setText(str(round(p42, 3)))
        self.tableWidget.item(37, 3).setText(str(self.calcmaxtemp))

        self.tableWidget.item(38, 0).setText(str(round(metdI23, 3)))
        self.tableWidget.item(38, 1).setText(str(round(metdU43, 3)))
        self.tableWidget.item(38, 2).setText(str(round(p43, 3)))
        self.tableWidget.item(38, 3).setText(str(self.min_v))

        self.tableWidget.item(39, 0).setText(str(round(metdI24, 3)))
        self.tableWidget.item(39, 1).setText(str(round(metdU44, 3)))
        self.tableWidget.item(39, 2).setText(str(round(p44, 3)))
        self.tableWidget.item(39, 3).setText(str(self.max_v))

        self.tableWidget.item(40, 0).setText(str(round(metdI25, 3)))
        self.tableWidget.item(40, 1).setText(str(round(metdU45, 3)))
        self.tableWidget.item(40, 2).setText(str(round(p45, 3)))
        self.tableWidget.item(40, 3).setText(str(self.mintemp))

        self.tableWidget.item(36, 5).setText(str(round(fem41, 3)))
        self.tableWidget.item(36, 6).setText(str(round(prll21, 3)))
        self.tableWidget.item(37, 5).setText(str(round(fem42, 3)))
        self.tableWidget.item(37, 6).setText(str(round(prll22, 3)))
        self.tableWidget.item(38, 5).setText(str(round(fem43, 3)))
        self.tableWidget.item(38, 6).setText(str(round(prll23, 3)))
        self.tableWidget.item(39, 5).setText(str(round(fem44, 3)))
        self.tableWidget.item(39, 6).setText(str(round(prll24, 3)))
        self.tableWidget.item(40, 5).setText(str(round(fem45, 3)))
        self.tableWidget.item(40, 6).setText(str(round(prll25, 3)))

# метод 2-5
        # p46 = metdI2 * metdU51 #расчет мощности
        # p47 = metdI22 * metdU52
        # p48 = metdI23 * metdU53
        # p49 = metdI24 * metdU54
        # p50 = metdI25 * metdU55
        #
        # # вывод результатов расчета метода 1 для разных температур
        # self.tableWidget.item(42, 0).setText(str(round(metdI2, 3)))
        # self.tableWidget.item(42, 1).setText(str(round(metdU51, 3)))
        # self.tableWidget.item(42, 2).setText(str(round(p46, 3)))
        # self.tableWidget.item(42, 3).setText(str(self.calcmintemp))
        #
        # self.tableWidget.item(43, 0).setText(str(round(metdI22, 3)))
        # self.tableWidget.item(43, 1).setText(str(round(metdU52, 3)))
        # self.tableWidget.item(43, 2).setText(str(round(p47, 3)))
        # self.tableWidget.item(43, 3).setText(str(self.calcmaxtemp))
        #
        # self.tableWidget.item(44, 0).setText(str(round(metdI23, 3)))
        # self.tableWidget.item(44, 1).setText(str(round(metdU53, 3)))
        # self.tableWidget.item(44, 2).setText(str(round(p48, 3)))
        # self.tableWidget.item(44, 3).setText(str(self.min_v))
        #
        # self.tableWidget.item(45, 0).setText(str(round(metdI24, 3)))
        # self.tableWidget.item(45, 1).setText(str(round(metdU54, 3)))
        # self.tableWidget.item(45, 2).setText(str(round(p49, 3)))
        # self.tableWidget.item(45, 3).setText(str(self.max_v))
        #
        # self.tableWidget.item(46, 0).setText(str(round(metdI25, 3)))
        # self.tableWidget.item(46, 1).setText(str(round(metdU55, 3)))
        # self.tableWidget.item(46, 2).setText(str(round(p50, 3)))
        # self.tableWidget.item(46, 3).setText(str(self.mintemp))


        self.paint_borderline()

    def resultNoct(self):
        print(" !NOCT!")
        print("NCels = ", self.numncels)
        self.imput_params()

        noctT1 = self.calcmintemp + ((self.noct - 20)/800)*self.irradiance
        noctT2 = self.calcmaxtemp + ((self.noct - 20)/800)*self.irradiance
        noctT3 = self.min_v + ((self.noct - 20)/800)*self.irradiance
        noctT4 = self.max_v + ((self.noct - 20)/800)*self.irradiance
        noctT5 = self.mintemp + ((self.noct - 20)/800)*self.irradiance

# 1
#метод 1-1
        metdI1 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (noctT1 - 25)))#расчет А 1 метод
        metdU1 = self.numvoc + (self.nummuvocspec * (noctT1 - 25)) #расчет V
        metdImp1 = (self.irradiance/1000) * (self.numimp + (self.nummuisc * (noctT1 - 25)))#расчет А 1 метод
        metdUmp1 = self.numvmp + (self.nummuvocspec * (noctT1 - 25)) #расчет V
        p1 = metdImp1 * metdUmp1 #расчет мощности
        fem1 = metdU1 * self.countfem
        prll1 = metdI1 * self.countparallel

        metdI12 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (noctT2 - 25)))
        metdU12 = self.numvoc + (self.nummuvocspec * (noctT2 - 25))
        metdImp12 = (self.irradiance/1000) * (self.numimp + (self.nummuisc * (noctT2 - 25)))#расчет А 1 метод
        metdUmp12 = self.numvmp + (self.nummuvocspec * (noctT2 - 25)) #расчет V
        p2 = metdImp12 * metdUmp12
        fem12 = metdU12 * self.countfem
        prll12 = metdI12 * self.countparallel

        metdI13 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (noctT3 - 25)))
        metdU13 = self.numvoc + (self.nummuvocspec * (noctT3 - 25))
        metdImp13 = (self.irradiance/1000) * (self.numimp + (self.nummuisc * (noctT3 - 25)))#расчет А 1 метод
        metdUmp13 = self.numvmp + (self.nummuvocspec * (noctT3 - 25)) #расчет V
        p3 = metdImp13 * metdUmp13
        fem13 = metdU13 * self.countfem
        prll13 = metdI13 * self.countparallel

        metdI14 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (noctT4 - 25)))
        metdU14 = self.numvoc + (self.nummuvocspec * (noctT4 - 25))
        metdImp14 = (self.irradiance/1000) * (self.numimp + (self.nummuisc * (noctT4 - 25)))#расчет А 1 метод
        metdUmp14 = self.numvmp + (self.nummuvocspec * (noctT4 - 25)) #расчет V
        p4 = metdImp14 * metdUmp14
        fem14 = metdU14 * self.countfem
        prll14 = metdI14 * self.countparallel

        metdI15 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (noctT5 - 25)))
        metdU15 = self.numvoc + (self.nummuvocspec * (noctT5 - 25))
        metdImp15 = (self.irradiance/1000) * (self.numimp + (self.nummuisc * (noctT5 - 25)))#расчет А 1 метод
        metdUmp15 = self.numvmp + (self.nummuvocspec * (noctT5 - 25)) #расчет V
        p5 = metdImp15 * metdUmp15
        fem15 = metdU15 * self.countfem
        prll15 = metdI15 * self.countparallel

        # вывод результатов расчета метода 1 для разных температур
        self.tableWidget.item(0, 0).setText(str(round(metdI1, 3)))
        self.tableWidget.item(0, 1).setText(str(round(metdU1, 3)))
        self.tableWidget.item(0, 2).setText(str(round(p1, 3)))
        self.tableWidget.item(0, 3).setText(str(self.calcmintemp))
        self.tableWidget.item(0, 5).setText(str(round(fem1, 3)))
        self.tableWidget.item(0, 6).setText(str(round(prll1, 3)))

        self.tableWidget.item(1, 0).setText(str(round(metdI12, 3)))
        self.tableWidget.item(1, 1).setText(str(round(metdU12, 3)))
        self.tableWidget.item(1, 2).setText(str(round(p2, 3)))
        self.tableWidget.item(1, 3).setText(str(self.calcmaxtemp))
        self.tableWidget.item(1, 5).setText(str(round(fem12, 3)))
        self.tableWidget.item(1, 6).setText(str(round(prll12, 3)))

        self.tableWidget.item(2, 0).setText(str(round(metdI13, 3)))
        self.tableWidget.item(2, 1).setText(str(round(metdU13, 3)))
        self.tableWidget.item(2, 2).setText(str(round(p3, 3)))
        self.tableWidget.item(2, 3).setText(str(self.min_v))
        self.tableWidget.item(2, 5).setText(str(round(fem13, 3)))
        self.tableWidget.item(2, 6).setText(str(round(prll13, 3)))

        self.tableWidget.item(3, 0).setText(str(round(metdI14, 3)))
        self.tableWidget.item(3, 1).setText(str(round(metdU14, 3)))
        self.tableWidget.item(3, 2).setText(str(round(p4, 3)))
        self.tableWidget.item(3, 3).setText(str(self.max_v))
        self.tableWidget.item(3, 5).setText(str(round(fem14, 3)))
        self.tableWidget.item(3, 6).setText(str(round(prll14, 3)))

        self.tableWidget.item(4, 0).setText(str(round(metdI15, 3)))
        self.tableWidget.item(4, 1).setText(str(round(metdU15, 3)))
        self.tableWidget.item(4, 2).setText(str(round(p5, 3)))
        self.tableWidget.item(4, 3).setText(str(self.mintemp))
        self.tableWidget.item(4, 5).setText(str(round(fem15, 3)))
        self.tableWidget.item(4, 6).setText(str(round(prll15, 3)))

# метод 1-3
        q = 1.602 * pow(10, -19)
        k = 1.3806503 * pow(10, -23)
        logirradiance = math.log(self.irradiance/1000)

        metdU31 = self.numvoc + (((self.numncels * k * (273 + noctT1) * 1)/q) * logirradiance) + (self.nummuvocspec * (noctT1 - 25)) #расчет V
        metdUmp31 = self.numvmp + (((self.numncels * k * (273 + noctT1) * 1)/q) * logirradiance) + (self.nummuvocspec * (noctT1 - 25)) #расчет V
        p11 = metdImp1 * metdUmp31 #расчет мощности

        metdU32 = self.numvoc + (((self.numncels * k * (273 + noctT2) * 1)/q) * logirradiance) + (self.nummuvocspec * (noctT2 - 25))
        metdUmp32 = self.numvmp + (((self.numncels * k * (273 + noctT1) * 1)/q) * logirradiance) + (self.nummuvocspec * (noctT2 - 25)) #расчет V
        p12 = metdImp12 * metdUmp32

        metdU33 = self.numvoc + (((self.numncels * k * (273 + noctT3) * 1)/q) * logirradiance) + (self.nummuvocspec * (noctT3 - 25))
        metdUmp33 = self.numvmp + (((self.numncels * k * (273 + noctT1) * 1)/q) * logirradiance) + (self.nummuvocspec * (noctT3 - 25)) #расчет V
        p13 = metdImp13 * metdUmp33

        metdU34 = self.numvoc + (((self.numncels * k * (273 + noctT4) * 1)/q) * logirradiance) + (self.nummuvocspec * (noctT4 - 25))
        metdUmp34 = self.numvmp + (((self.numncels * k * (273 + noctT1) * 1)/q) * logirradiance) + (self.nummuvocspec * (noctT4 - 25)) #расчет V
        p14 = metdImp14 * metdUmp34

        metdU35 = self.numvoc + (((self.numncels * k * (273 + noctT5) * 1)/q) * logirradiance) + (self.nummuvocspec * (noctT5 - 25))
        metdUmp35 = self.numvmp + (((self.numncels * k * (273 + noctT1) * 1)/q) * logirradiance) + (self.nummuvocspec * (noctT5 - 25)) #расчет V
        p15 = metdImp15 * metdUmp35

        self.tableWidget.item(6, 0).setText(str(round(metdI1, 3)))
        self.tableWidget.item(6, 1).setText(str(round(metdU31, 3)))
        self.tableWidget.item(6, 2).setText(str(round(p11, 3)))
        self.tableWidget.item(6, 3).setText(str(self.calcmintemp))

        self.tableWidget.item(7, 0).setText(str(round(metdI12, 3)))
        self.tableWidget.item(7, 1).setText(str(round(metdU32, 3)))
        self.tableWidget.item(7, 2).setText(str(round(p12, 3)))
        self.tableWidget.item(7, 3).setText(str(self.calcmaxtemp))

        self.tableWidget.item(8, 0).setText(str(round(metdI13, 3)))
        self.tableWidget.item(8, 1).setText(str(round(metdU33, 3)))
        self.tableWidget.item(8, 2).setText(str(round(p13, 3)))
        self.tableWidget.item(8, 3).setText(str(self.min_v))

        self.tableWidget.item(9, 0).setText(str(round(metdI14, 3)))
        self.tableWidget.item(9, 1).setText(str(round(metdU34, 3)))
        self.tableWidget.item(9, 2).setText(str(round(p14, 3)))
        self.tableWidget.item(9, 3).setText(str(self.max_v))

        self.tableWidget.item(10, 0).setText(str(round(metdI15, 3)))
        self.tableWidget.item(10, 1).setText(str(round(metdU35, 3)))
        self.tableWidget.item(10, 2).setText(str(round(p15, 3)))
        self.tableWidget.item(10, 3).setText(str(self.mintemp))

        fem31 = metdU31 * self.countfem
        prll31 = metdI1 * self.countparallel
        fem32 = metdU32 * self.countfem
        prll32 = metdI12 * self.countparallel
        fem33 = metdU33 * self.countfem
        prll33 = metdI13 * self.countparallel
        fem34 = metdU34 * self.countfem
        prll34 = metdI14 * self.countparallel
        fem35 = metdU35 * self.countfem
        prll35 = metdI15 * self.countparallel
        self.tableWidget.item(6, 5).setText(str(round(fem31, 3)))
        self.tableWidget.item(6, 6).setText(str(round(prll31, 3)))
        self.tableWidget.item(7, 5).setText(str(round(fem32, 3)))
        self.tableWidget.item(7, 6).setText(str(round(prll32, 3)))
        self.tableWidget.item(8, 5).setText(str(round(fem33, 3)))
        self.tableWidget.item(8, 6).setText(str(round(prll33, 3)))
        self.tableWidget.item(9, 5).setText(str(round(fem34, 3)))
        self.tableWidget.item(9, 6).setText(str(round(prll34, 3)))
        self.tableWidget.item(10, 5).setText(str(round(fem35, 3)))
        self.tableWidget.item(10, 6).setText(str(round(prll35, 3)))

# метод 1-4
        c1 = 5.468511 * pow(10, -2)
        c2 = 5.973869 * pow(10, -3)
        c3 = 7.616178 * pow(10, -4)
        metdU41 = self.numvoc + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (noctT1 - 25)) #расчет V
        metdUmp41 = self.numvmp + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (noctT1 - 25)) #расчет V
        p16 = metdI1 * metdU41 #расчет мощности

        metdU42 = self.numvoc + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (noctT2 - 25))
        metdUmp42 = self.numvmp + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (noctT2 - 25)) #расчет V
        p17 = metdImp12 * metdUmp42

        metdU43 = self.numvoc + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (noctT3 - 25))
        metdUmp43 = self.numvmp + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (noctT3 - 25)) #расчет V
        p18 = metdImp13 * metdUmp43

        metdU44 = self.numvoc + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (noctT4 - 25))
        metdUmp44 = self.numvmp + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (noctT4 - 25)) #расчет V
        p19 = metdImp14 * metdUmp44

        metdU45 = self.numvoc + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (noctT5- 25))
        metdUmp45 = self.numvmp + (c1 * logirradiance) + (c2 * ((logirradiance)**2)) + (c3 * ((logirradiance)**3)) + (self.nummuvocspec * (noctT5 - 25)) #расчет V
        p20 = metdImp15 * metdUmp45

        self.tableWidget.item(12, 0).setText(str(round(metdI1, 3)))
        self.tableWidget.item(12, 1).setText(str(round(metdU41, 3)))
        self.tableWidget.item(12, 2).setText(str(round(p16, 3)))
        self.tableWidget.item(12, 3).setText(str(self.calcmintemp))

        self.tableWidget.item(13, 0).setText(str(round(metdI12, 3)))
        self.tableWidget.item(13, 1).setText(str(round(metdU42, 3)))
        self.tableWidget.item(13, 2).setText(str(round(p17, 3)))
        self.tableWidget.item(13, 3).setText(str(self.calcmaxtemp))

        self.tableWidget.item(14, 0).setText(str(round(metdI13, 3)))
        self.tableWidget.item(14, 1).setText(str(round(metdU43, 3)))
        self.tableWidget.item(14, 2).setText(str(round(p18, 3)))
        self.tableWidget.item(14, 3).setText(str(self.min_v))

        self.tableWidget.item(15, 0).setText(str(round(metdI14, 3)))
        self.tableWidget.item(15, 1).setText(str(round(metdU44, 3)))
        self.tableWidget.item(15, 2).setText(str(round(p19, 3)))
        self.tableWidget.item(15, 3).setText(str(self.max_v))

        self.tableWidget.item(16, 0).setText(str(round(metdI15, 3)))
        self.tableWidget.item(16, 1).setText(str(round(metdU45, 3)))
        self.tableWidget.item(16, 2).setText(str(round(p20, 3)))
        self.tableWidget.item(16, 3).setText(str(self.mintemp))

        fem41 = metdU41 * self.countfem
        prll41 = metdI1 * self.countparallel
        fem42 = metdU42 * self.countfem
        prll42 = metdI12 * self.countparallel
        fem43 = metdU43 * self.countfem
        prll43 = metdI13 * self.countparallel
        fem44 = metdU44 * self.countfem
        prll44 = metdI14 * self.countparallel
        fem45 = metdU45 * self.countfem
        prll45 = metdI15 * self.countparallel
        self.tableWidget.item(12, 5).setText(str(round(fem41, 3)))
        self.tableWidget.item(12, 6).setText(str(round(prll41, 3)))
        self.tableWidget.item(13, 5).setText(str(round(fem42, 3)))
        self.tableWidget.item(13, 6).setText(str(round(prll42, 3)))
        self.tableWidget.item(14, 5).setText(str(round(fem43, 3)))
        self.tableWidget.item(14, 6).setText(str(round(prll43, 3)))
        self.tableWidget.item(15, 5).setText(str(round(fem44, 3)))
        self.tableWidget.item(15, 6).setText(str(round(prll44, 3)))
        self.tableWidget.item(16, 5).setText(str(round(fem45, 3)))
        self.tableWidget.item(16, 6).setText(str(round(prll45, 3)))

# метод 1-5                                                                                                                             логарифмы от отрицательных чисел!!
        # metdU51 = (self.numvoc/1 + ((((self.numvoc/metdU1) - 1) / math.log(1000/self.irradiance)) * math.log(1000/self.irradiance))) * (25/self.calcmintemp)**(math.log(self.numvoc/metdU1) / math.log(self.calcmintemp/25))
        # p21 = metdI1 * metdU51 #расчет мощности
        #
        # metdU52 = (self.numvoc/1 + ((((self.numvoc/metdU12) - 1) / math.log(1000/self.irradiance)) * math.log(1000/self.irradiance))) * (25/self.calcmaxtemp)**(math.log(self.numvoc/metdU12) / math.log(self.calcmaxtemp/25))
        # p22 = metdI12 * metdU52
        #
        # metdU53 = (self.numvoc/1 + ((((self.numvoc/metdU13) - 1) / math.log(1000/self.irradiance)) * math.log(1000/self.irradiance))) * (25/self.min_v)**(math.log(self.numvoc/metdU13) / math.log(self.min_v/25))
        # p23 = metdI13 * metdU53
        #
        # metdU54 = (self.numvoc/1 + ((((self.numvoc/metdU14) - 1) / math.log(1000/self.irradiance)) * math.log(1000/self.irradiance))) * (25/self.max_v)**(math.log(self.numvoc/metdU14) / math.log(self.max_v/25))
        # p24 = metdI14 * metdU54
        #
        # metdU55 = (self.numvoc/1 + ((((self.numvoc/metdU15) - 1) / math.log(1000/self.irradiance)) * math.log(1000/self.irradiance))) * (25/self.mintemp)**(math.log(self.numvoc/metdU15) / math.log(self.mintemp/25))
        # p25 = metdI15 * metdU55
        #
        # self.tableWidget.item(18, 0).setText(str(round(metdI1, 3)))
        # self.tableWidget.item(18, 1).setText(str(round(metdU51, 3)))
        # self.tableWidget.item(18, 2).setText(str(round(p21, 3)))
        # self.tableWidget.item(18, 3).setText(str(self.calcmintemp))
        #
        # self.tableWidget.item(19, 0).setText(str(round(metdI12, 3)))
        # self.tableWidget.item(19, 1).setText(str(round(metdU52, 3)))
        # self.tableWidget.item(19, 2).setText(str(round(p22, 3)))
        # self.tableWidget.item(19, 3).setText(str(self.calcmaxtemp))
        #
        # self.tableWidget.item(20, 0).setText(str(round(metdI13, 3)))
        # self.tableWidget.item(20, 1).setText(str(round(metdU53, 3)))
        # self.tableWidget.item(20, 2).setText(str(round(p23, 3)))
        # self.tableWidget.item(20, 3).setText(str(self.min_v))
        #
        # self.tableWidget.item(21, 0).setText(str(round(metdI14, 3)))
        # self.tableWidget.item(21, 1).setText(str(round(metdU54, 3)))
        # self.tableWidget.item(21, 2).setText(str(round(p24, 3)))
        # self.tableWidget.item(21, 3).setText(str(self.max_v))
        #
        # self.tableWidget.item(22, 0).setText(str(round(metdI15, 3)))
        # self.tableWidget.item(22, 1).setText(str(round(metdU55, 3)))
        # self.tableWidget.item(22, 2).setText(str(round(p25, 3)))
        # self.tableWidget.item(22, 3).setText(str(self.mintemp))

# 2
# метод 2-1
        if self.irradiance == 1000:
            metdI2 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (noctT1 - 25)))#расчет А 1 метод
            metdI22 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (noctT2 - 25)))
            metdI23 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (noctT3 - 25)))
            metdI24 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (noctT4 - 25)))
            metdI25 = (self.irradiance/1000) * (self.numisc + (self.nummuisc * (noctT5 - 25)))

            metdImp2 = (self.irradiance/1000) * (self.numimp + (self.nummuisc * (noctT1 - 25)))#расчет А 1 метод
            metdImp22 = (self.irradiance/1000) * (self.numimp + (self.nummuisc * (noctT2 - 25)))
            metdImp23 = (self.irradiance/1000) * (self.numimp + (self.nummuisc * (noctT3 - 25)))
            metdImp24 = (self.irradiance/1000) * (self.numimp+ (self.nummuisc * (noctT4 - 25)))
            metdImp25 = (self.irradiance/1000) * (self.numimp + (self.nummuisc * (noctT5 - 25)))
        else:
            iscG = (self.irradiance/1000) * self.numisc
            a = float((math.log(self.numisc/iscG))/(math.log(1000/self.irradiance)))
            print("a =",a)
            metdI2 = ((self.irradiance/1000)**a) * (self.numisc + (self.nummuisc * (noctT1 - 25))) #расчет А 2 метод
            metdI22 = ((self.irradiance/1000)**a) * (self.numisc + (self.nummuisc * (noctT2 - 25)))
            metdI23 = ((self.irradiance/1000)**a) * (self.numisc + (self.nummuisc * (noctT3 - 25)))
            metdI24 = ((self.irradiance/1000)**a) * (self.numisc + (self.nummuisc * (noctT4 - 25)))
            metdI25 = ((self.irradiance/1000)**a) * (self.numisc + (self.nummuisc * (noctT5 - 25)))

            iscmpG = (self.irradiance/1000) * self.numimp
            amp = float((math.log(self.numimp/iscmpG))/(math.log(1000/self.irradiance)))
            print("a =",amp)
            metdImp2 = ((self.irradiance/1000)**amp) * (self.numimp + (self.nummuisc * (noctT1 - 25))) #расчет А 2 метод
            metdImp22 = ((self.irradiance/1000)**amp) * (self.numimp + (self.nummuisc * (noctT2 - 25)))
            metdImp23 = ((self.irradiance/1000)**amp) * (self.numimp + (self.nummuisc * (noctT3 - 25)))
            metdImp24 = ((self.irradiance/1000)**amp) * (self.numimp + (self.nummuisc * (noctT4- 25)))
            metdImp25 = ((self.irradiance/1000)**amp) * (self.numimp + (self.nummuisc * (noctT5 - 25)))

        p26 = metdImp2 * metdUmp1 #расчет мощности
        p27 = metdImp22 * metdUmp12
        p28 = metdImp23 * metdUmp13
        p29 = metdImp24 * metdUmp14
        p30 = metdImp25 * metdUmp15

        # вывод результатов расчета метода 1 для разных температур
        self.tableWidget.item(24, 0).setText(str(round(metdI2, 3)))
        self.tableWidget.item(24, 1).setText(str(round(metdU1, 3)))
        self.tableWidget.item(24, 2).setText(str(round(p26, 3)))
        self.tableWidget.item(24, 3).setText(str(self.calcmintemp))

        self.tableWidget.item(25, 0).setText(str(round(metdI22, 3)))
        self.tableWidget.item(25, 1).setText(str(round(metdU12, 3)))
        self.tableWidget.item(25, 2).setText(str(round(p27, 3)))
        self.tableWidget.item(25, 3).setText(str(self.calcmaxtemp))

        self.tableWidget.item(26, 0).setText(str(round(metdI23, 3)))
        self.tableWidget.item(26, 1).setText(str(round(metdU13, 3)))
        self.tableWidget.item(26, 2).setText(str(round(p28, 3)))
        self.tableWidget.item(26, 3).setText(str(self.min_v))

        self.tableWidget.item(27, 0).setText(str(round(metdI24, 3)))
        self.tableWidget.item(27, 1).setText(str(round(metdU14, 3)))
        self.tableWidget.item(27, 2).setText(str(round(p29, 3)))
        self.tableWidget.item(27, 3).setText(str(self.max_v))

        self.tableWidget.item(28, 0).setText(str(round(metdI25, 3)))
        self.tableWidget.item(28, 1).setText(str(round(metdU15, 3)))
        self.tableWidget.item(28, 2).setText(str(round(p30, 3)))
        self.tableWidget.item(28, 3).setText(str(self.mintemp))

        prll21 = metdI2 * self.countparallel
        prll22 = metdI22 * self.countparallel
        prll23 = metdI23 * self.countparallel
        prll24 = metdI24 * self.countparallel
        prll25 = metdI25 * self.countparallel

        self.tableWidget.item(24, 5).setText(str(round(fem1, 3)))
        self.tableWidget.item(24, 6).setText(str(round(prll21, 3)))
        self.tableWidget.item(25, 5).setText(str(round(fem12, 3)))
        self.tableWidget.item(25, 6).setText(str(round(prll22, 3)))
        self.tableWidget.item(26, 5).setText(str(round(fem13, 3)))
        self.tableWidget.item(26, 6).setText(str(round(prll23, 3)))
        self.tableWidget.item(27, 5).setText(str(round(fem14, 3)))
        self.tableWidget.item(27, 6).setText(str(round(prll24, 3)))
        self.tableWidget.item(28, 5).setText(str(round(fem15, 3)))
        self.tableWidget.item(28, 6).setText(str(round(prll25, 3)))

# метод 2-3
        p36 = metdImp2 * metdUmp31 #расчет мощности
        p37 = metdImp22 * metdUmp32
        p38 = metdImp23 * metdUmp33
        p39 = metdImp24 * metdUmp34
        p40 = metdImp25 * metdUmp35

        # вывод результатов расчета метода 1 для разных температур
        self.tableWidget.item(30, 0).setText(str(round(metdI2, 3)))
        self.tableWidget.item(30, 1).setText(str(round(metdU31, 3)))
        self.tableWidget.item(30, 2).setText(str(round(p36, 3)))
        self.tableWidget.item(30, 3).setText(str(self.calcmintemp))

        self.tableWidget.item(31, 0).setText(str(round(metdI22, 3)))
        self.tableWidget.item(31, 1).setText(str(round(metdU32, 3)))
        self.tableWidget.item(31, 2).setText(str(round(p37, 3)))
        self.tableWidget.item(31, 3).setText(str(self.calcmaxtemp))

        self.tableWidget.item(32, 0).setText(str(round(metdI23, 3)))
        self.tableWidget.item(32, 1).setText(str(round(metdU33, 3)))
        self.tableWidget.item(32, 2).setText(str(round(p38, 3)))
        self.tableWidget.item(32, 3).setText(str(self.min_v))

        self.tableWidget.item(33, 0).setText(str(round(metdI24, 3)))
        self.tableWidget.item(33, 1).setText(str(round(metdU34, 3)))
        self.tableWidget.item(33, 2).setText(str(round(p39, 3)))
        self.tableWidget.item(33, 3).setText(str(self.max_v))

        self.tableWidget.item(34, 0).setText(str(round(metdI25, 3)))
        self.tableWidget.item(34, 1).setText(str(round(metdU35, 3)))
        self.tableWidget.item(34, 2).setText(str(round(p40, 3)))
        self.tableWidget.item(34, 3).setText(str(self.mintemp))

        self.tableWidget.item(30, 5).setText(str(round(fem31, 3)))
        self.tableWidget.item(30, 6).setText(str(round(prll21, 3)))
        self.tableWidget.item(31, 5).setText(str(round(fem32, 3)))
        self.tableWidget.item(31, 6).setText(str(round(prll22, 3)))
        self.tableWidget.item(32, 5).setText(str(round(fem33, 3)))
        self.tableWidget.item(32, 6).setText(str(round(prll23, 3)))
        self.tableWidget.item(33, 5).setText(str(round(fem34, 3)))
        self.tableWidget.item(33, 6).setText(str(round(prll24, 3)))
        self.tableWidget.item(34, 5).setText(str(round(fem35, 3)))
        self.tableWidget.item(34, 6).setText(str(round(prll25, 3)))

# метод 2-4
        p41 = metdImp2 * metdUmp41 #расчет мощности
        p42 = metdImp22 * metdUmp42
        p43 = metdImp23 * metdUmp43
        p44 = metdImp24 * metdUmp44
        p45 = metdImp25 * metdUmp45

        # вывод результатов расчета метода 1 для разных температур
        self.tableWidget.item(36, 0).setText(str(round(metdI2, 3)))
        self.tableWidget.item(36, 1).setText(str(round(metdU41, 3)))
        self.tableWidget.item(36, 2).setText(str(round(p41, 3)))
        self.tableWidget.item(36, 3).setText(str(self.calcmintemp))

        self.tableWidget.item(37, 0).setText(str(round(metdI22, 3)))
        self.tableWidget.item(37, 1).setText(str(round(metdU42, 3)))
        self.tableWidget.item(37, 2).setText(str(round(p42, 3)))
        self.tableWidget.item(37, 3).setText(str(self.calcmaxtemp))

        self.tableWidget.item(38, 0).setText(str(round(metdI23, 3)))
        self.tableWidget.item(38, 1).setText(str(round(metdU43, 3)))
        self.tableWidget.item(38, 2).setText(str(round(p43, 3)))
        self.tableWidget.item(38, 3).setText(str(self.min_v))

        self.tableWidget.item(39, 0).setText(str(round(metdI24, 3)))
        self.tableWidget.item(39, 1).setText(str(round(metdU44, 3)))
        self.tableWidget.item(39, 2).setText(str(round(p44, 3)))
        self.tableWidget.item(39, 3).setText(str(self.max_v))

        self.tableWidget.item(40, 0).setText(str(round(metdI25, 3)))
        self.tableWidget.item(40, 1).setText(str(round(metdU45, 3)))
        self.tableWidget.item(40, 2).setText(str(round(p45, 3)))
        self.tableWidget.item(40, 3).setText(str(self.mintemp))

        self.tableWidget.item(36, 5).setText(str(round(fem41, 3)))
        self.tableWidget.item(36, 6).setText(str(round(prll21, 3)))
        self.tableWidget.item(37, 5).setText(str(round(fem42, 3)))
        self.tableWidget.item(37, 6).setText(str(round(prll22, 3)))
        self.tableWidget.item(38, 5).setText(str(round(fem43, 3)))
        self.tableWidget.item(38, 6).setText(str(round(prll23, 3)))
        self.tableWidget.item(39, 5).setText(str(round(fem44, 3)))
        self.tableWidget.item(39, 6).setText(str(round(prll24, 3)))
        self.tableWidget.item(40, 5).setText(str(round(fem45, 3)))
        self.tableWidget.item(40, 6).setText(str(round(prll25, 3)))

# метод 2-5
        # p46 = metdI2 * metdU51 #расчет мощности
        # p47 = metdI22 * metdU52
        # p48 = metdI23 * metdU53
        # p49 = metdI24 * metdU54
        # p50 = metdI25 * metdU55
        #
        # # вывод результатов расчета метода 1 для разных температур
        # self.tableWidget.item(42, 0).setText(str(round(metdI2, 3)))
        # self.tableWidget.item(42, 1).setText(str(round(metdU51, 3)))
        # self.tableWidget.item(42, 2).setText(str(round(p46, 3)))
        # self.tableWidget.item(42, 3).setText(str(self.calcmintemp))
        #
        # self.tableWidget.item(43, 0).setText(str(round(metdI22, 3)))
        # self.tableWidget.item(43, 1).setText(str(round(metdU52, 3)))
        # self.tableWidget.item(43, 2).setText(str(round(p47, 3)))
        # self.tableWidget.item(43, 3).setText(str(self.calcmaxtemp))
        #
        # self.tableWidget.item(44, 0).setText(str(round(metdI23, 3)))
        # self.tableWidget.item(44, 1).setText(str(round(metdU53, 3)))
        # self.tableWidget.item(44, 2).setText(str(round(p48, 3)))
        # self.tableWidget.item(44, 3).setText(str(self.min_v))
        #
        # self.tableWidget.item(45, 0).setText(str(round(metdI24, 3)))
        # self.tableWidget.item(45, 1).setText(str(round(metdU54, 3)))
        # self.tableWidget.item(45, 2).setText(str(round(p49, 3)))
        # self.tableWidget.item(45, 3).setText(str(self.max_v))
        #
        # self.tableWidget.item(46, 0).setText(str(round(metdI25, 3)))
        # self.tableWidget.item(46, 1).setText(str(round(metdU55, 3)))
        # self.tableWidget.item(46, 2).setText(str(round(p50, 3)))
        # self.tableWidget.item(46, 3).setText(str(self.mintemp))

        self.paint_borderline()

    def savefile(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)")[0]
        if filename != '':
            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
            self.addlabel(sheet)
            self.adddata(sheet)
            wbk.save(filename)
            self.statusBar.showMessage('Файл успешно сохранен!', 10000)
            self.statusBar.setStyleSheet("background-color:rgb(48, 219, 91)")

    def adddata(self, sheet):
        for currentColumn in range(self.tableWidget.columnCount()):
            for currentRow in range(self.tableWidget.rowCount()):
                try:
                    teext = str(self.tableWidget.item(currentRow, currentColumn).text()).replace(".", ",")
                    sheet.write(1 + currentRow, 1 + currentColumn, teext)
                except AttributeError:
                    pass

    def addlabel(self, sheet):
        for currentColumn in range(self.tableWidget.columnCount()):
            for currentRow in range(self.tableWidget.rowCount()):
                try:
                    teext = str(self.tableWidget.verticalHeaderItem(currentRow).text())
                    tet = str(self.tableWidget.horizontalHeaderItem(currentColumn).text())
                    sheet.write(1 + currentRow, 0, teext)
                    sheet.write(0, 1 + currentColumn, tet)
                except AttributeError:
                    pass
