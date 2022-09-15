# перевод дизайна
# cd "C:\PythonPRJCT\autoReportPdf"
# pyuic5 designRepPDF.ui -o designRepPDF.py
# pyuic5 designParsing.ui -o designParsing.py
# pyuic5 designDrawSchemes.ui -o designDrawSchemes.py
# pyuic5 designDrawSchemesTwo.ui -o designDrawSchemesTwo.py

import designRepPDF # загрузка файлов
import designParsing
import designDrawSchemes
import designDrawSchemesTwo
import parsingSelenium
import draw_schemes
import draw_schemes2
import pdf_builder
import encode_file
import glob, fitz, re, requests, sys, os # загрузка модулей
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from PyPDF2 import PdfFileMerger
from pathlib import Path
from os.path import isfile, join
from chardet import detect
from datetime import date
from PyQt5.Qt import QApplication
from PyQt5.QtCore import QRegExp, QTimer
from PyQt5.QtGui import QRegExpValidator, QIcon
from PyQt5 import QtWidgets, QtGui, QtCore, QtGui
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import subprocess
import shutil


path_to_pdf_pvsyst = "Data/PDF in/PVsyst"
path_to_pdf_schemes = "Data/PDF in/Shemes"
path_to_schemes = "Data/Schemes"
path_to_invertors = "Data/Modules/Invertors"
path_to_PV = "Data/Modules/PV's"
path_to_KTP = "Data/Modules/KTP's" 
csv = ""
img = ""
data = ""
graf = ""
        
class DrawOne(QThread):
    def __init__(self, params, parametrs, i, gost_frame_params):
        super().__init__()
        self.params = params
        self.parametrs = parametrs
        self.i = i
        self.gost_frame_params = gost_frame_params

    def run(self):
        self.num_error = draw_schemes.draw(self.params, self.parametrs , self.i, self.gost_frame_params)

class DrawTwo(QThread):
    def __init__(self, params, gost_frame_params):
        super().__init__()
        self.params = params
        self.gost_frame_params = gost_frame_params

    def run(self):
        draw_schemes2.draw(self.params, self.gost_frame_params)
        
class BuildDoc(QThread):
    def __init__(self, params_1, params_2, params_3):
        super().__init__()
        self.params = {**params_1, **params_2, **params_3}
        print('potok: ',self.params)

    def run(self):
        pdf_doc = pdf_builder.docPDF()
        pdf_doc.build(**self.params)
        del pdf_doc
        
class СonvertFiles(QThread):
    def __init__(self, path, flag):
        super().__init__()
        self.paths = path
        self.flag = flag

    def run(self):
        if self.flag == 'general':
            # srcfile = 'Data/Schemes/connect_system.svg'
            # trgfile = 'Data/Schemes/connect_system_codec.svg'
            # encode_file.to_utf8(srcfile, trgfile)
            rew = pdf_builder.docPDF()
            rew.convert_to_pdf(self.paths[0], path_to_pdf_schemes +"/General/generalScheme.pdf")
            # renderPDF.drawToFile(svg2rlg(self.paths[0]), path_to_pdf_schemes +"/General/generalScheme.pdf")
        elif self.flag == 'detailed':
            for i in range(len(self.paths)):
                renderPDF.drawToFile(svg2rlg(self.paths[i]), path_to_pdf_schemes + f"/Detailed/detailed{i}.pdf")
                # srcfile = path_to_pdf_schemes + f"/Detailed/detailed{i}.pdf"
                # trgfile = path_to_pdf_schemes + f"/Detailed/detailed{i}-codec.pdf"
                # encode_file.to_utf8(srcfile, trgfile)
        elif self.flag == 'pvsyst':
            # To get better resolution
            zoom_x = 2.0  # horizontal zoom
            zoom_y = 2.0  # vertical zoom
            mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension         
            all_files = glob.glob(self.paths)
            for filename in all_files:
                with fitz.open(filename) as doc:  
                    for page in doc:  # iterate through the pages
                        pix = page.get_pixmap(matrix=mat)  # render page to an image #matrix=mat
                        pix.save(f"Data/Images/PVsyst/page-{page.number + 1}.png")  # store image as a PNG  
                                         
class Parsing(QThread):
    def __init__(self, params, data, method):
        super().__init__()
        self.params = params
        self.data = data
        self.method = method

    def run(self):
        if self.method == "close":
            fp_general = path_to_pdf_schemes + "/General"
            fp_detailed = path_to_pdf_schemes + "/Detailed"
            patch_imgs_pvsyst = "Data/Images/PVsyst"
            img_files_pvsyst = [f for f in os.listdir(patch_imgs_pvsyst) if os.path.isfile(os.path.join(patch_imgs_pvsyst, f))]
            files_in_general = [f for f in os.listdir(fp_general) if isfile(join(fp_general, f))]
            files_in_detailed = [f for f in os.listdir(fp_detailed) if isfile(join(fp_detailed, f))]
            if len(files_in_general) != 0:
                os.remove(fp_general + f"/{files_in_general[0]}")
            if len(files_in_detailed ) != 0:
                for file in files_in_detailed:
                    os.remove(fp_detailed + f"/{file}")   
            if len(img_files_pvsyst) != 0:
                for file in img_files_pvsyst:
                    os.remove(patch_imgs_pvsyst + f"/{file}")  
            parsingSelenium.close_browser()
        elif self.method == "search":
            self.return_search = parsingSelenium.search(self.params)
        elif self.method == "load":
            self.return_download = parsingSelenium.load()
        elif self.method == "download":
            self.return_download = parsingSelenium.download()
        elif self.method == "data":
            self.current_city = parsingSelenium.result_list(self.params)
        elif self.method == "open":
            self.browser_status = parsingSelenium.ones()

class MainApp(QtWidgets.QMainWindow, designRepPDF.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('Data/icons/graficon.png'))
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.hide()
        self.input_data()
        self.btnDevice.clicked.connect(self.show_and_hide_device_button)
        self.btnSchemes.clicked.connect(self.show_and_hide_schemes_button)
        self.btnOpenPDF.clicked.connect(self.open_result_doc)
        self.btnOne.clicked.connect(self.pvsyst)
        self.btnTwo.clicked.connect(self.in_two_block)
        self.btnThree.clicked.connect(self.in_three_block)
        self.btnFour.clicked.connect(self.in_four_block)
        self.btnForm.clicked.connect(self.create_document)
        self.btnRP5.clicked.connect(self.show_window_parse)
        self.btnDrawScheme.clicked.connect(self.show_window_draw)
        self.btnDrawSchemeTwo.clicked.connect(self.show_window_draw_two)
        self.checkBox_3.clicked.connect(self.show_and_hide_cbox3)
        self.checkBox_5.clicked.connect(self.show_and_hide_cbox5)
        self.checkBox_8.clicked.connect(self.show_and_hide_cbox8)
        self.btnShow3.clicked.connect(self.show_btn_cbox3)
        self.btnShow5.clicked.connect(self.show_btn_cbox5)
        self.btnShow8.clicked.connect(self.show_btn_cbox8)
        self.btnSlideMenu.clicked.connect(self.slide_menu)
        self.btnLoadScheme1.clicked.connect(self.load_scheme_one)
        self.btnLoadScheme2.clicked.connect(self.load_scheme_two)
        # self.btnForm.hover.connect(self.validation)
        self.listRoof.activated.connect(self.roof_select)
        self.listInvertor_folder.activated.connect(self.invertor_select)
        self.listPV_folder.activated.connect(self.pv_select)
        self.listKTP_folder.activated.connect(self.ktp_select)
        self.listInvertor_file.activated.connect(self.invertor_load)
        self.w2 = WindowParse()
        self.w3 = WindowDraw()
        self.w4 = WindowDrawTwo()
        
    def input_data(self):
        self.path_pvsyst = " "
        self.pathes_detail_schemes = " "
        self.path_general_schemes = " "
        self.browser_status = None
        # self.module, self.mppt = "Н/Д"
        # self.in_height, self.in_width, self.in_depth = "Н/Д"
        # self.weight, self.v_mpp_min, self.v_mpp_max = "Н/Д"
        
        self.inputTitleProject.setText("ШЛЮМБЕРЖЕ. ЛИПЕЦК. СЭС 363,4 КВТ")
        self.inputCodeProject.setText("2215ШЛБ-СЭС-ОТР")
        self.inputClient.setText("ООО «Рэдалит Шлюмберже»")
        
        self.inputUDotIn.setText("0.4")
        self.inputAddress.setText("г. Екатеринбург, ул. Анатолия Мехренцева, 36.")
        self.inputAddressLat.setText("55.587562")
        self.inputAddressLong.setText("37.908986")
        self.inputObjectType.setText("Многоквартирный жилой дом")
        
        self.listRoof.addItem("Выберите")
        roofs = ["Плоская", "Скатная", "Фикс"]
        self.listRoof.addItems(roofs)

        self.listInvertor_folder.addItem("Выберите")
        self.listPV_folder.addItem("Выберите")
        self.listKTP_folder.addItem("Выберите")
        company_invertor = sorted(os.listdir(path_to_invertors))
        company_pv = sorted(os.listdir(path_to_PV))
        company_ktp = sorted(os.listdir(path_to_KTP))
        self.listInvertor_folder.addItems(company_invertor)
        self.listPV_folder.addItems(company_pv)
        self.listKTP_folder.addItems(company_ktp)
        
    def open_result_doc(self):
        os.startfile("Data\Report\Auto-OTR.pdf")
      
    def validation(self):
        if self.listRoof.currentText() == "Выберите":
            self.statusBar.showMessage('Выберите тип крыши', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.listRoof.setStyleSheet("QComboBox{background-color:rgba(229,229,234,1); border: 1.45px solid red; border-radius: 6; padding-left: 6.55px;} QComboBox:drop-down {width: 0px; height: 0px; border: 0px;}")
            return 0
        else:
            self.set_style_default()

    def set_style_default(self):
        self.listRoof.setStyleSheet("QComboBox{\n	background-color:rgba(229,229,234,1); \n	border: none;\n	border-radius: 6;\n	padding-left: 8px;\n}\n\nQComboBox:drop-down \n{\n    width: 0px;\n    height: 0px;\n    border: 0px;\n}\nQComboBox:hover{\n	background-color:rgba(242,242,247,1);\n}\n")
        self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.statusBar.showMessage('', 100)
 
    def closeEvent(self, event):
        self.statusBar.showMessage('Браузер закрывается, пожалуйста, подождите...')
        self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
        QtWidgets.QApplication.processEvents()
        
        self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
        
        # Выполнение загрузки в новом потоке.
        self.parser_close = Parsing(0, 0, "close")
        self.parser_close.finished.connect(self.closeFinished)
        self.parser_close.start()    
        
    def closeFinished(self):
        # Удаление потока после его использования.
        del self.parser_close   
        
    def hide(self):
        self.btnOpenPDF.hide()
        self.btnTwo.hide()
        self.btnThree.hide()
        self.btnFour.hide()
        self.btnDrawScheme.hide()
        self.btnDrawSchemeTwo.hide()
        self.label_slide_title.hide()
        self.checkBox_1.hide()
        self.checkBox_2.hide()
        self.checkBox_3.hide()
        self.checkBox_4.hide()
        self.checkBox_5.hide()
        self.checkBox_6.hide()
        self.checkBox_7.hide()
        self.checkBox_8.hide()
        self.btnShow3.hide()
        self.btnShow5.hide()
        self.btnShow8.hide()
        self.checkBox_3_1.hide()
        self.checkBox_3_2.hide()
        self.checkBox_3_3.hide()
        self.checkBox_3_4.hide()
        self.checkBox_5_1.hide()
        self.checkBox_5_1_1.hide()
        self.checkBox_5_1_2.hide()
        self.checkBox_5_1_3.hide()
        self.checkBox_5_1_4.hide()
        self.checkBox_5_2.hide()
        self.checkBox_5_3.hide()
        self.checkBox_5_4.hide()
        self.checkBox_5_5.hide()
        self.checkBox_5_6.hide()
        self.checkBox_8_1.hide()
        self.checkBox_8_2.hide()
        self.checkBox_8_3.hide()
        self.checkBox_8_4.hide()
        self.checkBox_8_5.hide()
        self.checkBox_8_6.hide()
        self.btnLoadScheme1.hide()
        self.btnLoadScheme2.hide()
        # Паспорт объекта
        self.inputUDotIn.hide()
        self.inputAddress.hide()
        self.inputAddressLat.hide()
        self.inputAddressLong.hide()
        self.inputObjectType.hide()
        self.inputTitleProject.hide()
        self.inputCodeProject.hide()
        self.inputClient.hide()
        self.label_6.hide()
        # Оборудование
        self.spinBox_numInvertor.hide()
        self.spinBox_numPV.hide()
        self.spinBox_numKTP.hide()

    def slide_menu(self):
        if self.label_for_slide.text() == "Паспорт объекта":
            self.btnSlideMenu.setText("⮂")
            self.label_for_slide.setText("Удаление раздела")
            # Паспорт объекта
            self.label_2.hide()
            self.label_3.hide()
            self.label_4.hide()
            self.label_5.hide()
            self.label_6.hide()
            self.inputUDotIn.hide()
            self.inputAddress.hide()
            self.inputAddressLat.hide()
            self.inputAddressLong.hide()
            self.inputObjectType.hide()
            self.inputTitleProject.hide()
            self.inputCodeProject.hide()
            self.inputClient.hide()
            # Оборудование
            self.listInvertor_folder.hide()
            self.listInvertor_file.hide()
            self.listPV_folder.hide()
            self.listPV_file.hide()
            self.listKTP_folder.hide()
            self.listKTP_file.hide()
            self.listRoof.hide()
            self.spinBox_numInvertor.hide()
            self.spinBox_numPV.hide()
            self.spinBox_numKTP.hide()
            self.btnAddInvertor.hide()
            self.btnAddPV.hide()
            self.btnAddKTP.hide()
            # Удаление разделов
            self.checkBox_1.show()
            self.checkBox_2.show()
            self.checkBox_3.show()
            self.checkBox_4.show()
            self.checkBox_5.show()
            self.checkBox_6.show()
            self.checkBox_7.show()
            self.checkBox_8.show()
            self.btnShow3.show()
            self.btnShow5.show()
            self.btnShow8.show()
            if self.btnShow3.text() == "▲":
                self.checkBox_3_1.show()
                self.checkBox_3_2.show()
                self.checkBox_3_3.show()
                self.checkBox_3_4.show()
            if self.btnShow5.text() == "▲":
                self.checkBox_5_1.show()
                self.checkBox_5_1_1.show()
                self.checkBox_5_1_2.show()
                self.checkBox_5_1_3.show()
                self.checkBox_5_1_4.show()
                self.checkBox_5_2.show()
                self.checkBox_5_3.show()
                self.checkBox_5_4.show()
                self.checkBox_5_5.show()
                self.checkBox_5_6.show()
            if self.btnShow8.text() == "▲":
                self.checkBox_8_1.show()
                self.checkBox_8_2.show()
                self.checkBox_8_3.show()
                self.checkBox_8_4.show()
                self.checkBox_8_5.show()
                self.checkBox_8_6.show()  
            self.label_slide_title.show()
            self.label_slide_title.setText("Номер раздела")
        elif self.label_for_slide.text() == "Удаление раздела":
            self.btnSlideMenu.setText("⮂")
            self.label_for_slide.setText("Оборудование")
            # Удаление разделов
            self.label_slide_title.hide()
            self.checkBox_1.hide()
            self.checkBox_2.hide()
            self.checkBox_3.hide()
            self.checkBox_4.hide()
            self.checkBox_5.hide()
            self.checkBox_6.hide()
            self.checkBox_7.hide()
            self.checkBox_8.hide()
            self.btnShow3.hide()
            self.btnShow5.hide()
            self.btnShow8.hide()
            self.checkBox_3_1.hide()
            self.checkBox_3_2.hide()
            self.checkBox_3_3.hide()
            self.checkBox_3_4.hide()
            self.checkBox_5_1.hide()
            self.checkBox_5_1_1.hide()
            self.checkBox_5_1_2.hide()
            self.checkBox_5_1_3.hide()
            self.checkBox_5_1_4.hide()
            self.checkBox_5_2.hide()
            self.checkBox_5_3.hide()
            self.checkBox_5_4.hide()
            self.checkBox_5_5.hide()
            self.checkBox_5_6.hide()
            self.checkBox_8_1.hide()
            self.checkBox_8_2.hide()
            self.checkBox_8_3.hide()
            self.checkBox_8_4.hide()
            self.checkBox_8_5.hide()
            self.checkBox_8_6.hide()
            # Паспорт объекта
            self.inputUDotIn.hide()
            self.inputAddress.hide()
            self.inputAddressLat.hide()
            self.inputAddressLong.hide()
            self.inputObjectType.hide()
            self.inputTitleProject.hide()
            self.inputCodeProject.hide()
            self.inputClient.hide()
            self.label_6.hide()
            # Оборудование
            self.btnAddInvertor.show()
            self.btnAddPV.show()
            self.btnAddKTP.show()
            self.label_2.setText("Инвертор")
            self.label_2.show()
            self.label_3.setText("ФЭМ")
            self.label_3.show()
            self.label_4.setText("КТП")
            self.label_4.show()
            self.label_5.setText("Тип крыши")
            self.label_5.show()
            self.listRoof.show()
            self.listInvertor_folder.show()
            self.listInvertor_file.show()
            self.listPV_folder.show()
            self.listPV_file.show()
            self.listKTP_folder.show()
            self.listKTP_file.show()
            self.listRoof.show()
        elif self.label_for_slide.text() == "Оборудование":
            self.btnSlideMenu.setText("⮀")
            self.label_for_slide.setText("Паспорт объекта")
            # Удаление разделов
            self.label_slide_title.hide()
            self.checkBox_1.hide()
            self.checkBox_2.hide()
            self.checkBox_3.hide()
            self.checkBox_4.hide()
            self.checkBox_5.hide()
            self.checkBox_6.hide()
            self.checkBox_7.hide()
            self.checkBox_8.hide()
            self.btnShow3.hide()
            self.btnShow5.hide()
            self.btnShow8.hide()
            self.checkBox_3_1.hide()
            self.checkBox_3_2.hide()
            self.checkBox_3_3.hide()
            self.checkBox_3_4.hide()
            self.checkBox_5_1.hide()
            self.checkBox_5_1_1.hide()
            self.checkBox_5_1_2.hide()
            self.checkBox_5_1_3.hide()
            self.checkBox_5_1_4.hide()
            self.checkBox_5_2.hide()
            self.checkBox_5_3.hide()
            self.checkBox_5_4.hide()
            self.checkBox_5_5.hide()
            self.checkBox_5_6.hide()
            self.checkBox_8_1.hide()
            self.checkBox_8_2.hide()
            self.checkBox_8_3.hide()
            self.checkBox_8_4.hide()
            self.checkBox_8_5.hide()
            self.checkBox_8_6.hide()
            # Оборудование
            self.listInvertor_folder.hide()
            self.listInvertor_file.hide()
            self.listPV_folder.hide()
            self.listPV_file.hide()
            self.listKTP_folder.hide()
            self.listKTP_file.hide()
            self.listRoof.hide()
            self.spinBox_numInvertor.hide()
            self.spinBox_numPV.hide()
            self.spinBox_numKTP.hide()
            self.btnAddInvertor.hide()
            self.btnAddPV.hide()
            self.btnAddKTP.hide()   
            # Паспорт объекта
            self.label_2.setText("Название проекта")
            self.label_2.show()
            self.label_3.setText("Тип объекта")
            self.label_3.show()
            self.label_4.setText("Заказчик")
            self.label_4.show()
            self.label_5.setText("Адрес")
            self.label_5.show()
            self.label_6.setText("U подключения, кВ")
            self.label_6.show()
            self.inputUDotIn.show()
            self.inputAddress.show()
            self.inputAddressLat.show()
            self.inputAddressLong.show()
            self.inputObjectType.show()
            self.inputTitleProject.show()
            self.inputCodeProject.show()
            self.inputClient.show()
            
    def show_btn_cbox3(self):
        if self.checkBox_3_1.isHidden():
            self.btnShow3.setText("▲")
            self.checkBox_3_1.show()
            self.checkBox_3_2.show()
            self.checkBox_3_3.show()
            self.checkBox_3_4.show()
        else:
            self.btnShow3.setText("▼")
            self.checkBox_3_1.hide()
            self.checkBox_3_2.hide()
            self.checkBox_3_3.hide()
            self.checkBox_3_4.hide()
            
    def show_btn_cbox5(self):
        if self.checkBox_5_1.isHidden():
            self.btnShow5.setText("▲")
            self.checkBox_5_1.show()
            self.checkBox_5_1_1.show()
            self.checkBox_5_1_2.show()
            self.checkBox_5_1_3.show()
            self.checkBox_5_1_4.show()
            self.checkBox_5_2.show()
            self.checkBox_5_3.show()
            self.checkBox_5_4.show()
            self.checkBox_5_5.show()
            self.checkBox_5_6.show()
        else:
            self.btnShow5.setText("▼")
            self.checkBox_5_1.hide()
            self.checkBox_5_1_1.hide()
            self.checkBox_5_1_2.hide()
            self.checkBox_5_1_3.hide()
            self.checkBox_5_1_4.hide()
            self.checkBox_5_2.hide()
            self.checkBox_5_3.hide()
            self.checkBox_5_4.hide()
            self.checkBox_5_5.hide()
            self.checkBox_5_6.hide()
            
    def show_btn_cbox8(self):
        if self.checkBox_8_1.isHidden():
            self.btnShow8.setText("▲")
            self.checkBox_8_1.show()
            self.checkBox_8_2.show()
            self.checkBox_8_3.show()
            self.checkBox_8_4.show()
            self.checkBox_8_5.show()
            self.checkBox_8_6.show()
        else:
            self.btnShow8.setText("▼")
            self.checkBox_8_1.hide()
            self.checkBox_8_2.hide()
            self.checkBox_8_3.hide()
            self.checkBox_8_4.hide()
            self.checkBox_8_5.hide()
            self.checkBox_8_6.hide()
              
    def show_and_hide_cbox3(self):
        if self.checkBox_3.isChecked():
            self.btnShow3.setText("▲")
            self.checkBox_3_1.show()
            self.checkBox_3_2.show()
            self.checkBox_3_3.show()
            self.checkBox_3_4.show()
            self.checkBox_3_1.setCheckState(2)
            self.checkBox_3_2.setCheckState(2)
            self.checkBox_3_3.setCheckState(2)
            self.checkBox_3_4.setCheckState(2)
        else:
            self.checkBox_3_1.setCheckState(0)
            self.checkBox_3_2.setCheckState(0)
            self.checkBox_3_3.setCheckState(0)
            self.checkBox_3_4.setCheckState(0)
            
    def show_and_hide_cbox5(self):
        if self.checkBox_5.isChecked():
            self.btnShow5.setText("▲")
            self.checkBox_5_1.show()
            self.checkBox_5_1_1.show()
            self.checkBox_5_1_2.show()
            self.checkBox_5_1_3.show()
            self.checkBox_5_1_4.show()
            self.checkBox_5_2.show()
            self.checkBox_5_3.show()
            self.checkBox_5_4.show()
            self.checkBox_5_5.show()
            self.checkBox_5_6.show()
            self.checkBox_5_1.setCheckState(2)
            self.checkBox_5_1_1.setCheckState(2)
            self.checkBox_5_1_2.setCheckState(2)
            self.checkBox_5_1_3.setCheckState(2)
            self.checkBox_5_1_4.setCheckState(2)
            self.checkBox_5_2.setCheckState(2)
            self.checkBox_5_3.setCheckState(2)
            self.checkBox_5_4.setCheckState(2)
            self.checkBox_5_5.setCheckState(2)
            self.checkBox_5_6.setCheckState(2)
        else:
            self.checkBox_5_1.setCheckState(0)
            self.checkBox_5_1_1.setCheckState(0)
            self.checkBox_5_1_2.setCheckState(0)
            self.checkBox_5_1_3.setCheckState(0)
            self.checkBox_5_1_4.setCheckState(0)
            self.checkBox_5_2.setCheckState(0)
            self.checkBox_5_3.setCheckState(0)
            self.checkBox_5_4.setCheckState(0)
            self.checkBox_5_5.setCheckState(0)
            self.checkBox_5_6.setCheckState(0)
                   
    def show_and_hide_cbox8(self):           
        if self.checkBox_8.isChecked():
            self.btnShow8.setText("▲")
            self.checkBox_8_1.show()
            self.checkBox_8_2.show()
            self.checkBox_8_3.show()
            self.checkBox_8_4.show()
            self.checkBox_8_5.show()
            self.checkBox_8_6.show()
            self.checkBox_8_1.setCheckState(2)
            self.checkBox_8_2.setCheckState(2)
            self.checkBox_8_3.setCheckState(2)
            self.checkBox_8_4.setCheckState(2)
            self.checkBox_8_5.setCheckState(2)
            self.checkBox_8_6.setCheckState(2)
        else:
            self.checkBox_8_1.setCheckState(0)
            self.checkBox_8_2.setCheckState(0)
            self.checkBox_8_3.setCheckState(0)
            self.checkBox_8_4.setCheckState(0)
            self.checkBox_8_5.setCheckState(0)
            self.checkBox_8_6.setCheckState(0)
        
    def show_window_parse(self):  # открытие 2  окна
        QtWidgets.QApplication.processEvents()
        internet = self.checkNet()
        if internet == 0:
            return
        if self.w2.isHidden():
            # self.w2.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.w2.setWindowIcon(QtGui.QIcon('Data/icons/graficon.png'))
            self.w2.show()
            self.w2.setFixedSize(470, 430)
            # Выполнение загрузки в новом потоке.
            if self.browser_status == None:
                self.parser_open = Parsing(0, 0, "open")
                self.parser_open.finished.connect(self.showParserFinished)
                self.parser_open.start()
    
    def showParserFinished(self):
        self.browser_status = self.parser_open.browser_status
        del self.parser_open

    def show_window_draw(self):  # открытие   окна рисования первой схемы
        self.w3.setWindowIcon(QtGui.QIcon('Data/icons/graficon.png'))
        self.w3.show()
        self.w3.setFixedSize(770, 475)

    def show_window_draw_two(self):  # открытие   окна рисования первой схемы
        self.w4.setWindowIcon(QtGui.QIcon('Data/icons/graficon.png'))
        self.w4.show()
        self.w4.setFixedSize(950, 335)

    def show_and_hide_device_button(self):
        if self.btnTwo.isHidden():
            self.btnTwo.show()
            self.btnThree.show()
            self.btnFour.show()
        else:
            self.btnTwo.hide()
            self.btnThree.hide()
            self.btnFour.hide()
            
    def show_and_hide_schemes_button(self):
        if self.btnDrawScheme.isHidden():
            self.btnDrawScheme.show()
            self.btnDrawSchemeTwo.show()
            self.btnLoadScheme1.show()
            self.btnLoadScheme2.show()
        else:   
            self.btnDrawScheme.hide()
            self.btnDrawSchemeTwo.hide()
            self.btnLoadScheme1.hide()
            self.btnLoadScheme2.hide()
            
    def checkNet(self):
        num_error = 0
        try:
            response = requests.get("http://www.google.com")
            self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)")
            num_error += 1
            return num_error
        except requests.ConnectionError:
            self.statusBar.showMessage('Нет подключения к интернету', 10000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            return num_error

    def roof_select(self):
        self.current_roof = self.listRoof.currentIndex()
 
    def search_invertor_data(self, path_folder, path_file):
        with open(rf"{path_to_invertors}/{path_folder}/{path_file}", 'r') as fp:
            for l_no, line in enumerate(fp):
                # search string
                if 'Model=' in line:
                    model = line.split('=')[1].replace('\n', '') #Модель 
                if 'Manufacturer=' in line:
                    title = line.split('=')[1].replace('\n', '') #Фирма 
                if 'NbInputs=' in line:
                    inputs_x_2 = int(line.split('=')[1].replace('\n', '')) #Кол-во входов до деления 
                if 'NbMPPT=' in line:  
                    self.mppt = int(line.split('=')[1].replace('\n', '')) #Кол-во мппт 
                if 'PMaxOUT=' in line:  
                    self.p_max = float(line.split('=')[1].replace('\n', '')) #Максимальная мощность
                if 'IMaxAC=' in line:  
                    self.i_max = float(line.split('=')[1].replace('\n', '')) #Максимальный ток
                if 'Width=' in line:  
                    self.in_width = float(line.split('=')[1].replace('\n', '')) * 1000 #ширина
                if 'Height=' in line:  
                    self.in_height = float(line.split('=')[1].replace('\n', '')) * 1000 #высота
                if 'Depth=' in line:  
                    self.in_depth = float(line.split('=')[1].replace('\n', '')) * 1000 #глубина
                if 'Weight=' in line:  
                    self.weight = float(line.split('=')[1].replace('\n', '')) #вес
                if 'VMppMin=' in line:  
                    self.v_mpp_min = int(line.split('=')[1].replace('\n', '')) #напряжение минимальное
                if 'VMPPMax=' in line:  
                    self.v_mpp_max = int(line.split('=')[1].replace('\n', '')) #напряжение максимальное
         
        self.module = " ".join([title, model])
        self.inputs = inputs_x_2 // self.mppt
         
        self.w3.set_invertor_params(self.module, self.mppt, self.inputs) # вставка параметров в окно первой схемы
        self.w4.set_invertor_params(self.module, self.p_max, self.i_max) # вставка параметров в окно второй схемы
              
    def invertor_select(self):
        self.listInvertor_file.clear()
        if self.listInvertor_folder.currentText() != "Выберите":
            self.select_title_invertor = self.listInvertor_folder.currentText() 
            modules_file = f'{path_to_invertors}/{self.select_title_invertor}'
            self.type_modules = sorted(os.listdir(modules_file))
            names_modules = []
            for name in self.type_modules:
                names_modules.append(name.split(".")[0])
            self.listInvertor_file.addItems(names_modules)
            
    def pv_select(self):
        self.listPV_file.clear()
        if self.listPV_folder.currentText() != "Выберите":
            self.select_title_pv = self.listPV_folder.currentText() 
            modules_file = f'{path_to_PV}/{self.select_title_pv}'
            self.type_pv_modules = sorted(os.listdir(modules_file))
            names_modules = []
            for name in self.type_pv_modules:
                names_modules.append(name.split(".")[0])
            self.listPV_file.addItems(names_modules)
            
    def ktp_select(self):
        self.listKTP_file.clear()
        if self.listInvertor_folder.currentText() != "Выберите":
            self.select_title_ktp = self.listKTP_folder.currentText() 
            modules_file = f'{path_to_KTP}/{self.select_title_ktp}'
            self.type_ktp_modules = sorted(os.listdir(modules_file))
            names_modules = []
            for name in self.type_ktp_modules:
                names_modules.append(name.split(".")[0])
            self.listKTP_file.addItems(names_modules)
            
    def invertor_load(self):
        current_invertor = self.listInvertor_file.currentText()
        for select_invertor in self.type_modules:
            if current_invertor in select_invertor: 
                self.search_invertor_data(self.select_title_invertor, select_invertor)
                
    def delete_pdf(self, method):
        fp_general = path_to_pdf_schemes + "/General"
        fp_detailed = path_to_pdf_schemes + "/Detailed"
        patch_imgs_pvsyst = "Data/Images/PVsyst"
        img_files_pvsyst = [f for f in os.listdir(patch_imgs_pvsyst) if os.path.isfile(os.path.join(patch_imgs_pvsyst, f))]
        files_in_general = [f for f in os.listdir(fp_general) if isfile(join(fp_general, f))]
        files_in_detailed = [f for f in os.listdir(fp_detailed) if isfile(join(fp_detailed, f))]

        if len(files_in_general) != 0 and method == 'general':
            os.remove(fp_general + f"/{files_in_general[0]}")
        if len(files_in_detailed ) != 0 and method == 'detailed':
            for file in files_in_detailed:
                os.remove(fp_detailed + f"/{file}")   
        if len(img_files_pvsyst) != 0 and method == 'pvsyst':
            for file in img_files_pvsyst:
                os.remove(patch_imgs_pvsyst + f"/{file}")  
                           
    def pvsyst(self):
        self.path_pvsyst = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', path_to_pdf_pvsyst, "*.pdf")[0] #открытие диалога для выбора файла
        print(self.path_pvsyst)
        if len(self.path_pvsyst) != 0:
            self.delete_pdf('pvsyst')
            self.textConsole.append("- Загружен отчет PVsyst")
            self.btnOne.setEnabled(False)
            self.converter_pvsyst = СonvertFiles(self.path_pvsyst, 'pvsyst')
            self.converter_pvsyst.finished.connect(self.convertPvsystFinished)
            self.converter_pvsyst.start()

    def load_scheme_one(self):
        self.pathes_detail_schemes = QtWidgets.QFileDialog.getOpenFileNames(self, 'Выберите файл', path_to_schemes, "*.svg")[0] #открытие диалога для выбора файла
        print(self.pathes_detail_schemes)
        if len(self.pathes_detail_schemes) != 0:
            self.delete_pdf('detailed')
            self.textConsole.append("- Загружена принципиальная эл.схема")
            self.btnLoadScheme1.setEnabled(False)
            self.converter1 = СonvertFiles(self.pathes_detail_schemes, 'detailed')
            self.converter1.finished.connect(self.convertOneFinished)
            self.converter1.start()
        
    def load_scheme_two(self):
        self.path_general_schemes = [QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', path_to_schemes, "*.svg")[0]] #открытие диалога для выбора файла
        print( self.path_general_schemes)
        if len(self.path_general_schemes[0]) != 0:
            self.delete_pdf('general')
            self.textConsole.append("- Загружена структурная эл.схема ")
            self.btnLoadScheme2.setEnabled(False)
            self.converter2 = СonvertFiles(self.path_general_schemes, 'general')
            self.converter2.finished.connect(self.convertTwoFinished)
            self.converter2.start()
        
    def convertOneFinished(self):
        self.btnLoadScheme1.setEnabled(True)
        del self.converter1
        
    def convertTwoFinished(self):
        self.btnLoadScheme2.setEnabled(True)
        del self.converter2
                       
    def convertPvsystFinished(self):
        self.btnOne.setEnabled(True)
        # self.images_pvsyst = self.converter_pvsyst.images_pvsyst.copy()
        del self.converter_pvsyst
        
    def in_two_block(self):
        global img

        img_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', path_to_pdf_pvsyst, "*.png *.jpg")[0] #открытие диалога для выбора файла

    def in_three_block(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', path_to_pdf_pvsyst, "*.PAN *.txt")[0] #открытие диалога для выбора файла

        if fname != '':
            with open(fname, 'r') as file: #поиск в файле нужных нам данных
                for line in file:
                    pass

    def in_four_block(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', path_to_pdf_pvsyst, "*.PAN *.txt")[0] #открытие диалога для выбора файла

        if fname != '':
            with open(fname, 'r') as file: #поиск в файле нужных нам данных
                for line in file:
                    pass

    def four_block_content(self, story):
        if self.checkBox_4.isChecked():
            self.textConsole.append("Блок №4 исключен из отчета")
        elif graf == "":
            self.textConsole.append("Блок №4 не загружен")
        else:
            self.textConsole.append("Блок №4 сформирован")
            return story

    def merge_pdf(self):
        pdf_merger = PdfFileMerger()
        fp_general = path_to_pdf_schemes + "/General"
        fp_detailed = path_to_pdf_schemes + "/Detailed"
        files_in_general = [f for f in os.listdir(fp_general) if isfile(join(fp_general, f))]
        files_in_detailed = [f for f in os.listdir(fp_detailed) if isfile(join(fp_detailed, f))]
        with open("Data/Report/Report.pdf", 'rb') as report: 
            pdf_merger.append(report)
        if len(files_in_general) != 0 and self.path_general_schemes != " ":
            with open(fp_general + f"/{files_in_general[0]}", 'rb') as image_fd: 
                pdf_merger.append(image_fd)
        if len(files_in_detailed ) != 0 and self.pathes_detail_schemes != " ":
            for i in range(len(files_in_detailed)):
                with open(fp_detailed + f"/{files_in_detailed[i]}", 'rb') as image_fd: 
                    pdf_merger.append(image_fd)
        with open("Data/Report/Auto-OTR.pdf", 'wb') as output_file:
            pdf_merger.write(output_file)
        del pdf_merger  
        os.remove("Data/Report/Report.pdf")      
        
    def out_params(self):
        self.block_1 = True if self.checkBox_1.isChecked() else False
        self.block_2 = True if self.checkBox_2.isChecked() else False
        self.block_3 = True if self.checkBox_3.isChecked() else False
        self.block_3_1 = True if self.checkBox_3_1.isChecked() else False
        self.block_3_2 = True if self.checkBox_3_2.isChecked() else False
        self.block_3_3 = True if self.checkBox_3_3.isChecked() else False
        self.block_3_4 = True if self.checkBox_3_4.isChecked() else False
        self.block_4 = True if self.checkBox_4.isChecked() else False
        self.block_5 = True if self.checkBox_5.isChecked() else False
        self.block_5_1 = True if self.checkBox_5_1.isChecked() else False
        self.block_5_1_1 = True if self.checkBox_5_1_1.isChecked() else False
        self.block_5_1_2 = True if self.checkBox_5_1_2.isChecked() else False
        self.block_5_1_3 = True if self.checkBox_5_1_3.isChecked() else False
        self.block_5_1_4 = True if self.checkBox_5_1_4.isChecked() else False
        self.block_5_2 = True if self.checkBox_5_2.isChecked() else False
        self.block_5_3 = True if self.checkBox_5_3.isChecked() else False
        self.block_5_4 = True if self.checkBox_5_4.isChecked() else False
        self.block_5_5 = True if self.checkBox_5_5.isChecked() else False
        self.block_5_6 = True if self.checkBox_5_6.isChecked() else False
        self.block_6 = True if self.checkBox_6.isChecked() else False
        self.block_7 = True if self.checkBox_7.isChecked() else False
        self.block_8 = True if self.checkBox_8.isChecked() else False
        self.block_8_1 = True if self.checkBox_8_1.isChecked() else False
        self.block_8_2 = True if self.checkBox_8_2.isChecked() else False
        self.block_8_3 = True if self.checkBox_8_3.isChecked() else False
        self.block_8_4 = True if self.checkBox_8_4.isChecked() else False
        self.block_8_5 = True if self.checkBox_8_5.isChecked() else False
        self.block_8_6 = True if self.checkBox_8_6.isChecked() else False
        self.title_project = self.inputTitleProject.text()
        self.code_project = self.inputCodeProject.text()
        self.client = self.inputClient.text()
        
    def create_document(self):
        try:
            with open("Data/Report/Report.pdf", 'w') as fp:
                pass
            with open("Data/Report/Auto-OTR.pdf", 'w') as fp:
                pass
        except PermissionError:
            self.statusBar.showMessage('Открыт pdf файл отчета, закройте его и повторите попытку', 4000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))
            return

        if self.validation() == 0:
            return
        else:
            self.btnOpenPDF.hide()
            QtWidgets.QApplication.processEvents()
            self.out_params()
            main_params = {'block_1': self.block_1, 'block_2': self.block_2, 'block_3': self.block_3, 
                        'block_3_1': self.block_3_1, 'block_3_2': self.block_3_2, 'block_3_3': self.block_3_3, 'block_3_4': self.block_3_4, 
                        'block_4': self.block_4, 'block_5': self.block_5, 
                        'block_5_1': self.block_5_1, 'block_5_1_1': self.block_5_1_1, 'block_5_1_2': self.block_5_1_2, 
                        'block_5_1_3': self.block_5_1_3, 'block_5_1_4': self.block_5_1_4, 'block_5_2': self.block_5_2, 
                        'block_5_3': self.block_5_3, 'block_5_4': self.block_5_4, 'block_5_5': self.block_5_5, 'block_5_6': self.block_5_6,
                        'block_6': self.block_6, 'block_7': self.block_7, 'block_8': self.block_8,
                        'block_8_1': self.block_8_1, 'block_8_2': self.block_8_2, 'block_8_3': self.block_8_3, 
                        'block_8_4': self.block_8_4, 'block_8_5': self.block_8_5, 'block_8_6': self.block_8_6,
                        'path_to_pvsyst': self.path_pvsyst, 'module': self.module, 'mppt': self.mppt,
                        'height': self.in_height, 'width': self.in_width, 'depth': self.in_depth, 'weight': self.weight,
                        'v_mpp_min': self.v_mpp_min, 'v_mpp_max': self.v_mpp_max, 'roof': self.current_roof,
                        'title_project': self.title_project, 'code_project': self.code_project, 'client': self.client}
                        # 'images_pvsyst': self.images_pvsyst
            
            parse_params = {'num_error': "Н/Д", 'min_temp': "Н/Д", 'date_min_temp': "Н/Д", 'num_weather_station': "Н/Д",
                'max_temp': "Н/Д", 'date_max_temp': "Н/Д", 'all_range': "Н/Д", 'average_temp': "Н/Д",
                'number_of_observations': "Н/Д", 'average_pressure': "Н/Д", 'average_humidity': "Н/Д", 'main_wind': "Н/Д", 
                'average_speed_wind': "Н/Д", 'max_speed_wind': "Н/Д", 'precipitation_on_12_hour': "Н/Д",
                'average_height_snow': "Н/Д", 'max_height_snow': "Н/Д", 'first_date_snow': "Н/Д", 'last_date_snow': "Н/Д"}
            
            weather_station_params = {'view_city': "Н/Д", 'strt_monit': "Н/Д", 'num_weather_station': "Н/Д"}
            
            weather_station = self.w2.parse_params_current_city if hasattr(self.w2, 'parse_params_current_city') else weather_station_params
            print( weather_station)
            
            weather = self.w2.parse_params if hasattr(self.w2, 'parse_params') else parse_params
                       
            self.btnForm.setEnabled(False)
            self.btnForm.setText('Формирование отчета...')
            self.statusBar.showMessage('Пожалуйста, подождите...')
            self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
            # Выполнение загрузки в новом потоке.
            self.builder = BuildDoc(main_params, weather, weather_station)
            # Qt вызовет метод `drawFinished()`, когда поток завершится.

            self.builder.finished.connect(self.buildFinished)
            self.builder.start()
        
    def buildFinished(self):
        self.textConsole.append("Отчет сформирован!")
        self.statusBar.showMessage('Отчет сформирован!', 4000)
        self.statusBar.setStyleSheet("background-color:rgb(48, 219, 91)")
        self.merge_pdf()
        self.btnOpenPDF.show()
        QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))
        self.btnForm.setEnabled(True)
        self.btnForm.setText('Сформировать PDF')
        # Удаление потока после его использования.
        del self.builder
        
class WindowDrawTwo(QtWidgets.QMainWindow, designDrawSchemesTwo.Ui_WindowDrawSchemesTwo):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnAdd_invertor.hide()
        self.btnAdd_other.hide()
        self.btnShowInvertor.hide()
        self.btnShowOther.hide()
        self.checkUse_threePhase.clicked.connect(self.show_and_hide_color_line_because_phase)
        self.checkDifferentInvertor.clicked.connect(self.show_and_hide_different_invertor)
        self.checkDifferentOther.clicked.connect(self.show_and_hide_different_other)
        self.btnOpen_otherParams.clicked.connect(self.show_other_params)
        self.checkYellowLineInvertor.clicked.connect(self.show_and_hide_switch)
        self.checkRedLineInvertor.clicked.connect(self.show_and_hide_switch)
        self.checkBlueLineInvertor.clicked.connect(self.show_and_hide_switch)
        self.checkGreenLineInvertor.clicked.connect(self.show_and_hide_switch)
        self.checkYellowLineOther.clicked.connect(self.show_and_hide_switch)
        self.checkRedLineOther.clicked.connect(self.show_and_hide_switch)
        self.checkBlueLineOther.clicked.connect(self.show_and_hide_switch)
        self.checkGreenLineOther.clicked.connect(self.show_and_hide_switch)
        self.btnShowInvertor.clicked.connect(self.show_invertor)
        self.btnAdd_invertor.clicked.connect(self.add_invertor)
        self.btnResultInfo.clicked.connect(self.result_info)
        self.btnShowOther.clicked.connect(self.show_other)
        self.btnAdd_other.clicked.connect(self.add_other)
        self.btnReset.clicked.connect(self.reset)
        self.btnDraw.pressed.connect(self.draw)
        self.set_default_params()
        self.invertor_params = []
        self.other_params = []
        self.optional_params = []
        self.checkbox_params = []
        self.all_params = [self.invertor_params, self.other_params, self.optional_params, self.checkbox_params]   

    def reset(self):
        self.checkUse_threePhase.setCheckState(2)
        self.checkUse_threePhase.click()
        self.checkUse_yzip.setCheckState(0)
        self.checkUse_counter.setCheckState(0)
        self.checkDifferentInvertor.setCheckState(0)
        self.checkDifferentOther.setCheckState(0)
        self.textConsoleModule.clear()
        self.textConsoleDraw.clear()
        self.btnAdd_invertor.hide()
        self.btnAdd_other.hide()
        self.invertor_params.clear()
        self.other_params.clear()
        self.optional_params.clear()
        self.checkbox_params.clear()

    def set_invertor_params(self, module, power, amperage):
        self.inputName_invertor.setText(f'{module}')
        self.inputPower_invertor.setText(f'{power}')
        self.inputAmperage_invertor.setText(f'{amperage}')

    def set_default_params(self):
        # Основные параемтры инвертора
        self.inputName_invertor.setText("Sungrow SG110CX")
        self.inputPower_invertor.setText('110')
        self.inputAmperage_invertor.setText('158.8')

        # Основные параметры доп модулей
        self.inputName_other.setText('Sungrow COM100E')
        self.inputPower_other.setText('0.01')
        self.inputAmperage_other.setText('0.05')
        self.inputType_other.setText('Контроллер')

        # Доп параметры инвертора
        self.inputParam1_invertor.setText('QF')
        self.inputParam2_invertor.setText('C160')
        self.inputParam6_invertor.setText('ВБШвнг(А)-LS 4x95')
        self.inputParam7_invertor.setText('180 м*')

        # Доп параметры доп
        self.inputParam1_other.setText('QF')
        self.inputParam2_other.setText('C10')
        self.inputParam6_other.setText('ВБШвнг(А)-LS 4x95')
        self.inputParam7_other.setText('30 м*')

        # Доп параметры узипа
        self.inputParam1_yzip.setText('ОПН 0.4 кВ, 10 кА')
        self.inputParam2_yzip.setText('QF')
        self.inputParam3_yzip.setText('C125')

        # Параметры выхода
        self.inputParam2_out.setText('2*3 ВВГнг(А)-LS 1x120 (3L)+')
        self.inputParam3_out.setText('2 ВВГнг(А)-LS 1x120 (PE+N)+')
        self.inputParam4_out.setText('20 м*')
        self.inputParam5_out.setText("РУ-0.4кВ, Шкаф РП-3.4, сущ. АВ 3QF14")

        self.checkRedLineInvertor.setEnabled(False)
        self.checkRedSwitchInvertor.setEnabled(False)
        self.checkGreenLineInvertor.setEnabled(False)
        self.checkGreenSwitchInvertor.setEnabled(False)

        self.checkRedLineOther.setEnabled(False)
        self.checkRedSwitchOther.setEnabled(False)
        self.checkGreenLineOther.setEnabled(False)
        self.checkGreenSwitchOther.setEnabled(False)

        self.checkYellowLineInvertor.setCheckState(2)
        self.checkYellowSwitchInvertor.setCheckState(2)
        self.checkBlueLineInvertor.setCheckState(2)
        self.checkBlueSwitchInvertor.setCheckState(2)
        self.checkBlackLineInvertor.setCheckState(2)

        self.checkYellowLineOther.setCheckState(2)
        self.checkYellowSwitchOther.setCheckState(2)
        self.checkBlueLineOther.setCheckState(2)
        self.checkBlueSwitchOther.setCheckState(2)
        self.checkBlackLineOther.setCheckState(2)

    def show_other_params(self):  # открытие доп параметров
        if self.width() == 950 and self.height() == 335:
            # self.textConsoleMPPT.clear()
            self.setFixedSize(950, 620)
            self.btnOpen_otherParams.setText('Скрыть')
        else:
            self.setFixedSize(950, 335)
            self.btnOpen_otherParams.setText('Подробнее')

    def show_and_hide_switch(self):
        if not self.checkYellowLineInvertor.isChecked():
            self.checkYellowSwitchInvertor.setCheckState(0)
        if not self.checkRedLineInvertor.isChecked():
            self.checkRedSwitchInvertor.setCheckState(0)
        if not self.checkBlueLineInvertor.isChecked():
            self.checkBlueSwitchInvertor.setCheckState(0)
        if not self.checkGreenLineInvertor.isChecked():
            self.checkGreenSwitchInvertor.setCheckState(0)

        if not self.checkYellowLineOther.isChecked():
            self.checkYellowSwitchOther.setCheckState(0)
        if not self.checkRedLineOther.isChecked():
            self.checkRedSwitchOther.setCheckState(0)
        if not self.checkBlueLineOther.isChecked():
            self.checkBlueSwitchOther.setCheckState(0)
        if not self.checkGreenLineOther.isChecked():
            self.checkGreenSwitchOther.setCheckState(0)

    def show_and_hide_color_line_because_phase(self):

        if self.checkUse_threePhase.isChecked():
            self.checkRedLineInvertor.setEnabled(True)
            self.checkRedSwitchInvertor.setEnabled(True)
            self.checkGreenLineInvertor.setEnabled(True)
            self.checkGreenSwitchInvertor.setEnabled(True)

            self.checkRedLineOther.setEnabled(True)
            self.checkRedSwitchOther.setEnabled(True)
            self.checkGreenLineOther.setEnabled(True)
            self.checkGreenSwitchOther.setEnabled(True)

            self.checkRedLineOther.setCheckState(0)
            self.checkRedSwitchOther.setCheckState(0)
            self.checkGreenLineOther.setCheckState(0)
            self.checkGreenSwitchOther.setCheckState(0)
        else:
            self.checkRedLineInvertor.setEnabled(False)
            self.checkRedSwitchInvertor.setEnabled(False)
            self.checkGreenLineInvertor.setEnabled(False)
            self.checkGreenSwitchInvertor.setEnabled(False)

            self.checkRedLineOther.setEnabled(False)
            self.checkRedSwitchOther.setEnabled(False)
            self.checkGreenLineOther.setEnabled(False)
            self.checkGreenSwitchOther.setEnabled(False)

            self.checkYellowLineInvertor.setCheckState(2)
            self.checkYellowSwitchInvertor.setCheckState(2)
            self.checkBlueLineInvertor.setCheckState(2)
            self.checkBlueSwitchInvertor.setCheckState(2)
            self.checkBlackLineInvertor.setCheckState(2)

            self.checkYellowLineOther.setCheckState(2)
            self.checkYellowSwitchOther.setCheckState(2)
            self.checkBlueLineOther.setCheckState(2)
            self.checkBlueSwitchOther.setCheckState(2)
            self.checkBlackLineOther.setCheckState(2)

    def show_and_hide_different_invertor(self):
        if self.checkDifferentInvertor.isChecked():
            self.btnAdd_invertor.show()
            self.btnShowInvertor.show()
            self.spinBox_countInvertor.setMinimum(1)
        else:
            self.btnAdd_invertor.hide()
            self.btnShowInvertor.hide()
            self.spinBox_countInvertor.setMinimum(0)
            self.spinBox_countInvertor.setValue(0)

    def show_and_hide_different_other(self):
        if self.checkDifferentOther.isChecked():
            self.btnAdd_other.show()
            self.btnShowOther.show()
            self.spinBox_countOther.setMinimum(1)
        else:
            self.btnAdd_other.hide()
            self.btnShowOther.hide()
            self.spinBox_countOther.setMinimum(0)
            self.spinBox_countOther.setValue(0)

    def show_invertor(self):
        self.textConsoleModule.clear()
        r = 0
        for i in self.invertor_params:
            r += 1
            self.textConsoleModule.append(f"Инвертор {r // 21}: {str(i)}")
            if r % 20 == 0:
                self.textConsoleModule.append(f"-----------")

    def show_other(self):
        self.textConsoleModule.clear()
        r = 0
        for i in self.other_params:
            r += 1
            self.textConsoleModule.append(f"Модуль {r // 22}: {str(i)}")
            if r % 21 == 0:
                self.textConsoleModule.append(f"-----------")

    def result_info(self):
        len_invertor_params = len(self.invertor_params)
        len_other_params = len(self.other_params)

        # self.textConsoleDraw.clear()
        self.textConsoleDraw.append(f"В схему добавлено:")
        self.textConsoleDraw.append(f"-- Кол-во инверторов: {len_invertor_params // 20}")
        self.textConsoleDraw.append(f"-- Кол-во дополнительных модулей: {len_other_params // 21}")
        self.textConsoleDraw.append(f"-- Узип") if self.checkUse_yzip.isChecked() else False
        self.textConsoleDraw.append(f"-- Счетчик") if self.checkUse_counter.isChecked() else False
        self.textConsoleDraw.append(f"-- Трёхфазная система") if self.checkUse_threePhase.isChecked() else False

    def add_invertor(self):
        self.invertor_params.append(str(self.inputName_invertor.text()))
        self.invertor_params.append(str(self.inputPower_invertor.text()))
        self.invertor_params.append(str(self.inputAmperage_invertor.text()))
        self.invertor_params.append(self.spinBox_countInvertor.value())

        self.invertor_params.append(str(self.inputParam1_invertor.text()))
        self.invertor_params.append(str(self.inputParam2_invertor.text()))
        self.invertor_params.append("")
        self.invertor_params.append("")
        self.invertor_params.append("")
        self.invertor_params.append(str(self.inputParam6_invertor.text()))
        self.invertor_params.append(str(self.inputParam7_invertor.text()))

        self.invertor_params.append(True if self.checkYellowLineInvertor.isChecked() else False)
        self.invertor_params.append(True if self.checkRedLineInvertor.isChecked() else False)
        self.invertor_params.append(True if self.checkBlueLineInvertor.isChecked() else False)
        self.invertor_params.append(True if self.checkGreenLineInvertor.isChecked() else False)
        self.invertor_params.append(True if self.checkBlackLineInvertor.isChecked() else False)

        self.invertor_params.append(True if self.checkYellowSwitchInvertor.isChecked() else False)
        self.invertor_params.append(True if self.checkRedSwitchInvertor.isChecked() else False)
        self.invertor_params.append(True if self.checkBlueSwitchInvertor.isChecked() else False)
        self.invertor_params.append(True if self.checkGreenSwitchInvertor.isChecked() else False)

        self.textConsoleModule.clear()
        r = 0
        for i in self.invertor_params:
            r += 1
            self.textConsoleModule.append(f"Инвертор {r // 21}: {str(i)}")
            if r % 20 == 0:
                self.textConsoleModule.append(f"-----------")

        self.textConsoleDraw.append(f"Добавлен Инвертор {str(self.inputName_invertor.text())} \n Мощность: {str(self.inputPower_invertor.text())} \n Сила тока: {str(self.inputAmperage_invertor.text())} \n Кол-во: {self.spinBox_countInvertor.value()}")
        return self.invertor_params

    def add_other(self):
        self.other_params.append(str(self.inputName_other.text()))
        self.other_params.append(str(self.inputPower_other.text()))
        self.other_params.append(str(self.inputAmperage_other.text()))
        self.other_params.append(str(self.inputType_other.text()))
        self.other_params.append(self.spinBox_countOther.value())

        self.other_params.append(str(self.inputParam1_other.text()))
        self.other_params.append(str(self.inputParam2_other.text()))
        self.other_params.append("")
        self.other_params.append("")
        self.other_params.append("")
        self.other_params.append(str(self.inputParam6_other.text()))
        self.other_params.append(str(self.inputParam7_other.text()))

        self.other_params.append(True if self.checkYellowLineOther.isChecked() else False)
        self.other_params.append(True if self.checkRedLineOther.isChecked() else False)
        self.other_params.append(True if self.checkBlueLineOther.isChecked() else False)
        self.other_params.append(True if self.checkGreenLineOther.isChecked() else False)
        self.other_params.append(True if self.checkBlackLineOther.isChecked() else False)

        self.other_params.append(True if self.checkYellowSwitchOther.isChecked() else False)
        self.other_params.append(True if self.checkRedSwitchOther.isChecked() else False)
        self.other_params.append(True if self.checkBlueSwitchOther.isChecked() else False)
        self.other_params.append(True if self.checkGreenSwitchOther.isChecked() else False)

        self.textConsoleModule.clear()
        r = 0
        for i in self.other_params:
            r += 1
            self.textConsoleModule.append(f"Модуль {r // 22}: {str(i)}")
            if r % 21 == 0:
                self.textConsoleModule.append(f"-----------")

        self.textConsoleDraw.append(f"Добавлен {str(self.inputType_other.text())}: {str(self.inputName_other.text())} \n Мощность: {str(self.inputPower_other.text())} \n Сила тока: {str(self.inputAmperage_other.text())} \n Кол-во: {self.spinBox_countOther.value()}")
        return self.other_params

    def optional_parametrs(self):
        self.optional_params.append(str(self.inputParam1_yzip.text()))
        self.optional_params.append(str(self.inputParam2_yzip.text()))
        self.optional_params.append(str(self.inputParam3_yzip.text()))
        self.optional_params.append("")
        self.optional_params.append("")

        self.optional_params.append("")
        self.optional_params.append(str(self.inputParam2_out.text()))
        self.optional_params.append(str(self.inputParam3_out.text()))
        self.optional_params.append(str(self.inputParam4_out.text()))
        self.optional_params.append(str(self.inputParam5_out.text()))
        return self.optional_params

    def check_imput_params(self):
        num_error = 0
        if str(self.inputName_invertor.text()) == '':
            self.statusBar.showMessage('Введите название инвертора', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputName_invertor.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            num_error += 1
            return num_error
        else:
            self.set_style_default()

        if str(self.inputPower_invertor.text()) == '':
            self.statusBar.showMessage('Введите мощность инвертора', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputPower_invertor.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            num_error += 1
            return num_error
        else:
            self.set_style_default()

        if str(self.inputAmperage_invertor.text()) == '':
            self.statusBar.showMessage('Введите силу тока в инверторе', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputAmperage_invertor.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            num_error += 1
            return num_error
        else:
            self.set_style_default()

        if str(self.inputName_other.text()) == '':
            self.statusBar.showMessage('Введите название доп. оборудования', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputName_other.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            num_error += 1
            return num_error
        else:
            self.set_style_default()

        if str(self.inputPower_other.text()) == '':
            self.statusBar.showMessage('Введите мощность доп. оборудования', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputPower_other.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            num_error += 1
            return num_error
        else:
            self.set_style_default()

        if str(self.inputAmperage_other.text()) == '':
            self.statusBar.showMessage('Введите силу тока в доп. оборудовании', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputAmperage_other.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            num_error += 1
            return num_error
        else:
            self.set_style_default()

        if str(self.inputType_other.text()) == '':
            self.statusBar.showMessage('Введите тип доп. оборудования', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputType_other.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            num_error += 1
            return num_error
        else:
            self.set_style_default()

        print(num_error)
        return num_error

    def set_style_default(self):
        self.inputName_invertor.setStyleSheet("QLineEdit{\n	background-color:rgba(229,229,234,1); \n	border-radius: 6;\n	border: none;\n}\nQLineEdit:hover{\n	background-color:rgba(242,242,247,1);\n}\nQLineEdit:pressed{\n	background-color:rgba(188,188,192,1);\n	border-radius: 12;\n}")
        self.inputPower_invertor.setStyleSheet("QLineEdit{\n	background-color:rgba(229,229,234,1); \n	border-radius: 6;\n	border: none;\n}\nQLineEdit:hover{\n	background-color:rgba(242,242,247,1);\n}\nQLineEdit:pressed{\n	background-color:rgba(188,188,192,1);\n	border-radius: 12;\n}")
        self.inputAmperage_invertor.setStyleSheet("QLineEdit{\n	background-color:rgba(229,229,234,1); \n	border-radius: 6;\n	border: none;\n}\nQLineEdit:hover{\n	background-color:rgba(242,242,247,1);\n}\nQLineEdit:pressed{\n	background-color:rgba(188,188,192,1);\n	border-radius: 12;\n}")
        self.inputName_other.setStyleSheet("QLineEdit{\n	background-color:rgba(229,229,234,1); \n	border-radius: 6;\n	border: none;\n}\nQLineEdit:hover{\n	background-color:rgba(242,242,247,1);\n}\nQLineEdit:pressed{\n	background-color:rgba(188,188,192,1);\n	border-radius: 12;\n}")
        self.inputPower_other.setStyleSheet("QLineEdit{\n	background-color:rgba(229,229,234,1); \n	border-radius: 6;\n	border: none;\n}\nQLineEdit:hover{\n	background-color:rgba(242,242,247,1);\n}\nQLineEdit:pressed{\n	background-color:rgba(188,188,192,1);\n	border-radius: 12;\n}")
        self.inputAmperage_other.setStyleSheet("QLineEdit{\n	background-color:rgba(229,229,234,1); \n	border-radius: 6;\n	border: none;\n}\nQLineEdit:hover{\n	background-color:rgba(242,242,247,1);\n}\nQLineEdit:pressed{\n	background-color:rgba(188,188,192,1);\n	border-radius: 12;\n}")
        self.inputType_other.setStyleSheet("QLineEdit{\n	background-color:rgba(229,229,234,1); \n	border-radius: 6;\n	border: none;\n}\nQLineEdit:hover{\n	background-color:rgba(242,242,247,1);\n}\nQLineEdit:pressed{\n	background-color:rgba(188,188,192,1);\n	border-radius: 12;\n}")

        self.statusBar.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.statusBar.showMessage('', 100)
        # self.statusBar.setStyleSheet("background-color:rgb(48, 219, 91)")

    def draw(self):
        num_error = self.check_imput_params()
        if num_error != 0:
            return num_error
        print(f"Инвертор: {self.checkDifferentOther.checkState()}")
        print(f"Доп: {self.checkDifferentInvertor.checkState()}")

        if self.checkDifferentOther.checkState() == 0 and self.checkDifferentInvertor.checkState() == 2:
            print('1')
            self.all_params.clear()
            self.other_params.clear()
            self.optional_params.clear()

            self.all_params.append(self.invertor_params)
            self.all_params.append(self.add_other())
            self.all_params.append(self.optional_parametrs())
            if not self.invertor_params:
                self.statusBar.showMessage("Вы не добавили параметры инвертора, НАЖМИТЕ '+'")
                self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
                num_error += 1
                return num_error
        elif self.checkDifferentOther.checkState() == 2 and self.checkDifferentInvertor.checkState() == 0:
            print('2')
            self.all_params.clear()
            self.invertor_params.clear()
            self.optional_params.clear()

            self.all_params.append(self.add_invertor())
            self.all_params.append(self.other_params)
            self.all_params.append(self.optional_parametrs())
            if not self.other_params:
                self.statusBar.showMessage("Вы не добавили параметры дополнительного оборудования, НАЖМИТЕ '+'")
                self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
                num_error += 1
                return num_error
        elif self.checkDifferentOther.checkState() == 2 and self.checkDifferentInvertor.checkState() == 2:
            print('3')
            self.all_params.clear()
            self.optional_params.clear()
            self.all_params.append(self.invertor_params)
            self.all_params.append(self.other_params)
            self.all_params.append(self.optional_parametrs())
            if not self.invertor_params:
                self.statusBar.showMessage("Вы не добавили параметры инвертора, НАЖМИТЕ '+'")
                self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
                num_error += 1
                return num_error
            elif not self.other_params:
                self.statusBar.showMessage("Вы не добавили параметры дополнительного оборудования, НАЖМИТЕ '+'")
                self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
                num_error += 1
                return num_error
        else:
            print('4')
            self.all_params.clear()
            self.invertor_params.clear()
            self.other_params.clear()
            self.optional_params.clear()
            self.all_params.append(self.add_invertor())
            self.all_params.append(self.add_other())
            self.all_params.append(self.optional_parametrs())

        if num_error != 0:
            return num_error
        else:
            self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)")

        # Использовать узип?
        use_yzip = True if self.checkUse_yzip.isChecked() else False

        # Использоватиь счетчик?
        use_counter = True if self.checkUse_counter.isChecked() else False

        # Трёхфазная система?
        use_threePhase = True if self.checkUse_threePhase.isChecked() else False

        self.checkbox_params = [use_yzip, use_counter, use_threePhase]
        self.all_params.append(self.checkbox_params)
        print(self.all_params)
        
        title_project = window.inputTitleProject.text()
        code_project = window.inputCodeProject.text() 
        gost_frame_params = {'title_project': title_project, 'code_project': code_project}   
            
        self.btnDraw.setEnabled(False)
        self.btnDraw.setText('Построение чертежа...')
        self.statusBar.showMessage('Пожалуйста, подождите...')
        self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
        # Выполнение загрузки в новом потоке.
        self.painter = DrawTwo(self.all_params, gost_frame_params)
        # Qt вызовет метод `drawFinished()`, когда поток завершится.

        self.painter.finished.connect(self.drawFinished)
        self.painter.start()
        
    def drawFinished(self):
        self.all_params.clear()
        self.invertor_params.clear()
        self.other_params.clear()
        self.optional_params.clear()
        self.textConsoleModule.clear()
        self.statusBar.showMessage('Чертеж успешно построен', 4000)
        self.statusBar.setStyleSheet("background-color:rgb(48, 219, 91)")
        QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))
        self.textConsoleDraw.append(f"------------------------------------")

        self.btnDraw.setEnabled(True)
        self.btnDraw.setText('Построить')
        # Удаление потока после его использования.
        del self.painter

class WindowDraw(QtWidgets.QMainWindow, designDrawSchemes.Ui_WindowDrawSchemes):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.validate()
        self.btnAdd_new_mppt.hide()
        self.spinBox_CloneInvertor.hide()
        self.btnDraw.clicked.connect(self.draw)
        self.btnUpdateMppt.clicked.connect(self.update_mppt)
        self.btnAdd_new_mppt.clicked.connect(self.add_mppt)
        self.btnUpdateConsole.clicked.connect(self.update_console)
        self.checkUse_CloneInvertor.clicked.connect(self.show_and_hide_clone_invertor)
        self.checkUse_different_mppt.clicked.connect(self.show_and_hide_different_mppt)
        self.checkUse_three_phase.clicked.connect(self.show_and_hide_color_line_because_phase)
        self.checkUse_5or4_line.clicked.connect(self.show_and_hide_color_line_because_phase)
        self.spinBox_CloneInvertor.setMinimum(1)
        self.inputCount_mppt.textChanged.connect(self.validate_input)
        self.inputCount_input_mppt.textChanged.connect(self.validate_input)
        self.inputAll_chain.textChanged.connect(self.validate_input)
        self.checkUse_y_connector.clicked.connect(self.validate_input)
        self.checkUse_all_mppt.clicked.connect(self.validate_input)
        self.btnReset.clicked.connect(self.reset)
        self.set_default_params()
        self.input_params = []

    def reset(self):
        self.inputCount_mppt.clear()
        self.inputCount_input_mppt.clear()
        self.inputSolar_count_on_the_chain.clear()
        self.inputAll_chain.clear()
        self.checkUse_y_connector.setCheckState(0)
        self.checkUse_all_mppt.setCheckState(0)
        self.checkUse_different_mppt.setCheckState(0)
        self.checkUse_three_phase.setCheckState(0)
        self.checkUse_5or4_line.setCheckState(0)
        self.checkUse_5or4_line.setEnabled(False)
        self.checkUse_CloneInvertor.setCheckState(0)
        self.textConsoleMPPT.clear()
        self.textConsoleDraw.clear()
        self.textConsoleCurrent.clear()
        self.btnAdd_new_mppt.hide()
        self.spinBox_CloneInvertor.hide()
        self.input_params.clear()
                
    def set_invertor_params(self, module, mppt, inputs):
        self.inputName_invertor.setText(f'{module}')
        self.inputCount_mppt.setText(f'{mppt}')
        self.inputCount_input_mppt.setText(f'{inputs}')

    def set_default_params(self):
        self.inputName_invertor.setText('Sungrow SG110')
        self.inputNumber_invertor.setText('Инвертор')
        self.inputTitle_grid_line.setText('ВБШвнг(A)-LS 4x95')
        self.inputTitle_grid_line_length.setText('180 м')
        self.inputTitle_grid_top.setText('ЩР 0.4 кВ (ВИЭ)')
        self.inputTitle_grid_switch.setText('QF1 3P 160A')
        self.checkUse_5or4_line.setEnabled(False)

    def show_and_hide_color_line_because_phase(self):
        if self.checkUse_three_phase.isChecked():
            self.checkUse_5or4_line.setEnabled(True)
        else:
            self.checkUse_5or4_line.setEnabled(False)
            self.checkUse_5or4_line.setCheckState(0)
            
    def parametrs(self):
        self.count_mppt = self.inputCount_mppt.text()
        self.input_mppt = self.inputCount_input_mppt.text()
        self.count_fem = self.inputSolar_count_on_the_chain.text()
        self.all_chain = self.inputAll_chain.text()

    def validate(self): #валидация вводимых данных
        reg_ex = QRegExp('^-?(0|[1-9]\d*)(\.[0-9]{1,4})?$')
        self.inputCount_mppt.setValidator(QRegExpValidator(reg_ex, self.inputCount_mppt))
        self.inputCount_input_mppt.setValidator(QRegExpValidator(reg_ex, self.inputCount_input_mppt))
        self.inputSolar_count_on_the_chain.setValidator(QRegExpValidator(reg_ex, self.inputSolar_count_on_the_chain))
        self.inputAll_chain.setValidator(QRegExpValidator(reg_ex, self.inputAll_chain))

    def validate_input(self): #валидация вводимых данных
        
        # creating a opacity effect
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.6)
        
        use_all_mppt = True if self.checkUse_all_mppt.isChecked() else False
        use_y_connector = True if self.checkUse_y_connector.isChecked() else False
        if self.inputCount_input_mppt.text() != '':    
            count_input_mppt = int(self.inputCount_input_mppt.text())
        if self.inputCount_mppt.text() != '':
            self.count_mppt =  int(self.inputCount_mppt.text())
        if self.inputAll_chain.text() != '':
            self.all_chain =  int(self.inputAll_chain.text())
            
        if self.inputCount_mppt.text() != '' and self.inputCount_input_mppt.text() != '':   
            self.textConsoleCurrent.clear()         
            max_input = count_input_mppt * self.count_mppt
            max_input_y = count_input_mppt * self.count_mppt * 2
            self.textConsoleCurrent.append(f"Макс. кол-во входов без Y коннектора: {max_input}")
            self.textConsoleCurrent.append(f"Макс. кол-во входов c Y коннектором: {max_input_y}")
            
            if self.inputAll_chain.text() != '':
                if self.all_chain < self.count_mppt and use_all_mppt == True:
                    # self.textConsoleCurrent.append("")
                    self.textConsoleCurrent.append("ПРЕДУПРЕЖДЕНИЕ:")
                    self.textConsoleCurrent.append("Невозможно распределить по всем MPPT")
                    self.textConsoleCurrent.append("РЕШЕНИЕ: Увеличьте кол-во цепочек / Уберите полное заполнение")
                    self.btnDraw.setEnabled(False)
                    self.btnDraw.setGraphicsEffect(self.opacity_effect)
                elif self.all_chain > max_input and use_y_connector == False:
                    # self.textConsoleCurrent.append("")
                    self.textConsoleCurrent.append("ПРЕДУПРЕЖДЕНИЕ:")
                    self.textConsoleCurrent.append("Кол-во цепочек не вмещается")
                    self.textConsoleCurrent.append("РЕШЕНИЕ: примените Y коннекторы / уменьшите кол-во цепочек")
                    self.btnDraw.setEnabled(False)
                    self.btnDraw.setGraphicsEffect(self.opacity_effect)
                elif self.all_chain <= max_input and use_y_connector == True and use_all_mppt == True:
                    # self.textConsoleCurrent.append("")
                    self.textConsoleCurrent.append("ПРЕДУПРЕЖДЕНИЕ:")
                    self.textConsoleCurrent.append("Кол-во цепочек слишком мало, чтобы распределить по всем  MPPT с Y коннекторами")
                    self.textConsoleCurrent.append("РЕШЕНИЕ: уберите Y коннекторы / уберите полное заполнение")
                    self.btnDraw.setEnabled(False)
                    self.btnDraw.setGraphicsEffect(self.opacity_effect)
                elif self.all_chain > max_input_y:
                    # self.textConsoleCurrent.append("")
                    self.textConsoleCurrent.append("ПРЕДУПРЕЖДЕНИЕ:")
                    self.textConsoleCurrent.append("Кол-во цепочек слишком большое для данной конфигурации")
                    self.textConsoleCurrent.append("РЕШЕНИЕ: уменьшите кол-во цепочек / измените конфигурацию")
                    self.btnDraw.setEnabled(False)
                    self.btnDraw.setGraphicsEffect(self.opacity_effect)
                else:
                    self.btnDraw.setEnabled(True)
                    self.btnDraw.setGraphicsEffect(self.opacity_effect.setOpacity(1))
            
    def check_imput_params(self):
        self.parametrs()
        num_error = 0
        if self.count_mppt == '':
            self.statusBar.showMessage('Введите количество MPPT', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputCount_mppt.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            num_error += 1
            return num_error
        else:
            self.set_style_default()

        if self.input_mppt == '':
            self.statusBar.showMessage('Введите число входов на МРРТ', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputCount_input_mppt.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            num_error += 1
            return num_error
        else:
            self.set_style_default()

        if self.count_fem == '':
            self.statusBar.showMessage('Введите количество ФЭМ в цепочке', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputSolar_count_on_the_chain.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            num_error += 1
            return num_error
        else:
            self.set_style_default()

        if self.all_chain == '':
            self.statusBar.showMessage('Введите общее количество цепочек', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputAll_chain.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            num_error += 1
            return num_error
        else:
            self.set_style_default()
            print(num_error)
            return num_error

    def set_style_default(self):
        self.inputCount_mppt.setStyleSheet("QLineEdit{\n	background-color:rgba(229,229,234,1); \n	border-radius: 6;\n	border: none;\n}\nQLineEdit:hover{\n	background-color:rgba(242,242,247,1);\n}\nQLineEdit:pressed{\n	background-color:rgba(188,188,192,1);\n	border-radius: 12;\n}")
        self.inputCount_input_mppt.setStyleSheet("QLineEdit{\n	background-color:rgba(229,229,234,1); \n	border-radius: 6;\n	border: none;\n}\nQLineEdit:hover{\n	background-color:rgba(242,242,247,1);\n}\nQLineEdit:pressed{\n	background-color:rgba(188,188,192,1);\n	border-radius: 12;\n}")
        self.inputSolar_count_on_the_chain.setStyleSheet("QLineEdit{\n	background-color:rgba(229,229,234,1); \n	border-radius: 6;\n	border: none;\n}\nQLineEdit:hover{\n	background-color:rgba(242,242,247,1);\n}\nQLineEdit:pressed{\n	background-color:rgba(188,188,192,1);\n	border-radius: 12;\n}")
        self.inputAll_chain.setStyleSheet("QLineEdit{\n	background-color:rgba(229,229,234,1); \n	border-radius: 6;\n	border: none;\n}\nQLineEdit:hover{\n	background-color:rgba(242,242,247,1);\n}\nQLineEdit:pressed{\n	background-color:rgba(188,188,192,1);\n	border-radius: 12;\n}")

        self.statusBar.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.statusBar.showMessage('', 100)
        # self.statusBar.setStyleSheet("background-color:rgb(48, 219, 91)")

    def show_and_hide_different_mppt(self):
        if self.checkUse_different_mppt.isChecked():
            self.btnAdd_new_mppt.show()
            # self.textConsoleMPPT.clear()
        else:
            self.btnAdd_new_mppt.hide()

    def show_and_hide_clone_invertor(self):
        if self.checkUse_CloneInvertor.isChecked():
            self.spinBox_CloneInvertor.show()
        else:
            self.spinBox_CloneInvertor.hide()
            self.spinBox_CloneInvertor.setValue(1)

    def update_mppt(self):
        self.textConsoleMPPT.clear()
        self.textConsoleMPPT.append(f"Актуальное: {self.input_params}")

    def update_console(self):
        self.textConsoleDraw.clear()

    def add_mppt(self):
        num_error = self.check_imput_params()
        if num_error != 0:
            return num_error
        max_input = int(self.input_mppt) * int(self.count_mppt)
        max_input_y = int(self.input_mppt) * int(self.count_mppt) * 2
        self.input_params.append(int(self.inputCount_mppt.text()))
        self.input_params.append(int(self.inputCount_input_mppt.text()))
        self.input_params.append(int(self.inputSolar_count_on_the_chain.text()))
        self.input_params.append(int(self.inputAll_chain.text()))
        # self.textConsoleDraw.append("Параметры MPPT")
        self.textConsoleMPPT.clear()
        self.textConsoleMPPT.append(str(self.input_params))
        self.textConsoleDraw.append("----------------------------")
        self.textConsoleDraw.append("ИСХОДНЫЕ ДАННЫЕ:")
        self.textConsoleDraw.append(f"- Число MPPT: {self.count_mppt}")
        self.textConsoleDraw.append(f"- Число входов MPPT: {self.input_mppt}")
        self.textConsoleDraw.append(f"- Число ФЭМ модулей в цепочке: {self.count_fem}")
        self.textConsoleDraw.append(f"-Число цепочек: {self.all_chain}")
        self.textConsoleDraw.append(f"-Максимальное кол-во входов без Y: {max_input}")
        self.textConsoleDraw.append(f"-Максимальное кол-во входов c Y: {max_input_y}")
        # print(self.input_params)

    def draw(self):
        num_error = self.check_imput_params()
        if num_error != 0:
            return num_error

        if self.checkUse_different_mppt.checkState() == 0:
            self.input_params.clear()
            self.add_mppt()

        count_diffirent_mppt = len(self.input_params) // 4# количество разных mppt
        parametrs = []
        parametrs.append(str(self.inputName_invertor.text()))
        parametrs.append(str(self.inputNumber_invertor.text()))
        parametrs.append(str(self.inputTitle_grid_line.text()))
        parametrs.append(str(self.inputTitle_grid_top.text()))
        parametrs.append(str(self.inputTitle_grid_switch.text()))
        parametrs.append(True if self.checkUse_y_connector.isChecked() else False) # использовать Y коннекторы Да(True) Нет(False)?
        parametrs.append(True if self.checkUse_all_mppt.isChecked() else False) # распределять по всем mppt(True) или оставлять пустые(False)?
        parametrs.append(True if self.checkUse_different_mppt.isChecked() else False) #Режим разных mppt вкл(True)/выкл(False)
        parametrs.append(count_diffirent_mppt)
        parametrs.append(True if self.checkUse_three_phase.isChecked() else False) #3-х фахная система вкл(True)/выкл(False)
        parametrs.append(True if self.checkUse_5or4_line.isChecked() else False) #5/4 провода вкл(True)/выкл(False)
        parametrs.append(str(self.inputTitle_grid_line_length.text()))

        count_invertor = self.spinBox_CloneInvertor.value() #количество инверторов
        self.textConsoleDraw.append(f"Кол-во инверторов: {count_invertor}")

        save_input_params = self.input_params.copy()

        for i in range(count_invertor):
            if not save_input_params:
                self.textConsoleDraw.append("Введите заново параметры разных MPPT")
                self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
                return
            i += 1
            self.textConsoleDraw.append(f"Номер инвертора: {i}")
            if self.checkUse_CloneInvertor.isChecked() != 0:
                self.input_params = save_input_params.copy()
            
            self.btnDraw.setEnabled(False)
            self.btnDraw.setText('Построение чертежа...')
            self.statusBar.showMessage('Пожалуйста, подождите...')
            self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
            
            title_project = window.inputTitleProject.text()
            code_project = window.inputCodeProject.text()            
            gost_frame_params = {'title_project': title_project, 'code_project': code_project} 
            # Выполнение загрузки в новом потоке.
            self.painter_draw_one = DrawOne(self.input_params, parametrs, i, gost_frame_params)
            # Qt вызовет метод `drawFinished()`, когда поток завершится.

            self.painter_draw_one.finished.connect(self.drawFinished)
            self.painter_draw_one.start()

    def drawFinished(self):
        if self.painter_draw_one.num_error[0] == 0:
            self.textConsoleDraw.append("----------------------------")
            self.textConsoleDraw.append("РЕЗУЛЬТАТЫ:")
            self.textConsoleDraw.append(f" Всего цепочек: {self.painter_draw_one.num_error[1]}")
            self.textConsoleDraw.append(f" Всего модулей: {self.painter_draw_one.num_error[2]}")
            self.statusBar.showMessage('Чертеж успешно построен', 4000)
            self.statusBar.setStyleSheet("background-color:rgb(48, 219, 91)")
            QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))
            self.btnDraw.setEnabled(True)
            self.btnDraw.setText('Построить')
        elif self.painter_draw_one.num_error[0] == 1:
            self.textConsoleDraw.append("!!!")
            self.textConsoleDraw.append("Кол-во цепочек меньше числа MPPT, невозможно заполгнить все MPPT")
            self.textConsoleDraw.append("---")
            self.statusBar.showMessage("Внимание!")
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.btnDraw.setEnabled(True)
            self.btnDraw.setText('Построить')
        elif self.painter_draw_one.num_error[0] == 3:
            self.textConsoleDraw.append("!!!")
            self.textConsoleDraw.append("Данное количесво цепочек не вмещается, примените Y коннекторы, либо измените конфигурацию MPPT")
            self.textConsoleDraw.append("---")
            self.statusBar.showMessage("Внимание!")
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.btnDraw.setEnabled(True)
            self.btnDraw.setText('Построить')
        elif self.painter_draw_one.num_error[0] == 4:
            self.textConsoleDraw.append("!!!")
            self.textConsoleDraw.append("Данное количесво цепочек слишком мало чтобы заполнить все MPPT применяя Y коннекторы, уберите Y коннекторы или полное заполнение")
            self.textConsoleDraw.append("---")
            self.statusBar.showMessage("Внимание!")
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.btnDraw.setEnabled(True)
            self.btnDraw.setText('Построить')
        elif self.painter_draw_one.num_error[0] == 5:
            self.textConsoleDraw.append("!!!")
            self.textConsoleDraw.append("Слишком большое количество цепочек")
            self.textConsoleDraw.append("---")
            self.statusBar.showMessage("Внимание!")
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.btnDraw.setEnabled(True)
            self.btnDraw.setText('Построить')
        # Удаление потока после его использования.
        del self.painter_draw_one
        
class WindowParse(QtWidgets.QMainWindow, designParsing.Ui_WindowRP5):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.checkNet()
        current_date = date.today()
        self.dateEdit_end.setDate(current_date)
        self.btnSearch.clicked.connect(self.parsing_search)
        self.btnParse.clicked.connect(self.parsing_download)
        self.btnDwnld_T.clicked.connect(self.parsing_load)
        self.listCity.activated.connect(self.parsing_date)
        # self.parse_params = None
             
    def checkNet(self):
        num_error = 0
        try:
            response = requests.get("http://www.google.com")
            # print("response code: ", response.status_code)
            self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)")
            num_error += 1
            return num_error
        except requests.ConnectionError:
            self.statusBar.showMessage('Нет подключения к интернету', 10000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            print("Could not connect")
            return num_error
   
    def opacity(self, button, enabled):
        count_opacity = 0.6 if enabled == False else 1
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(count_opacity)
        button.setGraphicsEffect(opacity_effect)
        button.setEnabled(enabled)

    def check_inCity(self):
        num_error = 0
        internet = self.checkNet()
        c = self.inputCity.text()
        if c is None or c == '' or len(c) == 0:
            self.statusBar.showMessage('Введите город в строку поиска!', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.opacity(self.btnDwnld_T, True)
            self.opacity(self.btnParse, True)
            self.btnSearch.setEnabled(True)
            self.btnParse.setText('Скачать архив')
            self.btnDwnld_T.setText('Подгрузить температуру')
            self.btnSearch.setText('Найти')
            return num_error
        elif len(c) == 1:
            self.statusBar.showMessage('Слишком короткий запрос!', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.opacity(self.btnDwnld_T, True)
            self.opacity(self.btnParse, True)
            self.btnSearch.setEnabled(True)
            self.btnParse.setText('Скачать архив')
            self.btnDwnld_T.setText('Подгрузить температуру')
            self.btnSearch.setText('Найти')
            return num_error
        elif internet == 0:
            return num_error
        else:
            self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)")
            num_error += 1
            return num_error

    def parsing_search(self):
        self.btnSearch.setEnabled(False)
        self.opacity(self.btnDwnld_T, False)
        self.opacity(self.btnParse, False)
        self.btnSearch.setText('Поиск...')
        if self.check_inCity() == 0:
            return
        city = self.inputCity.text()
        self.textConsole.clear()
        # self.textConsole.append("Идет поиск...")
        self.listCity.clear()
        self.statusBar.showMessage('Пожалуйста, подождите...')
        self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
        QtWidgets.QApplication.processEvents()
        
        self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
        
        # Выполнение загрузки в новом потоке.
        self.parser_search = Parsing(city, 0, "search")
        self.parser_search.finished.connect(self.searchFinished)
        self.parser_search.start()

    def parsing_date(self):
        num_error = 0
        self.opacity(self.btnDwnld_T, False)
        self.opacity(self.btnParse, False)
        self.opacity(self.listCity, False)
        if self.check_inCity() == 0:
            return num_error
        self.textConsole.append("...")
        self.textConsole.append("Подгрузка дополнительной информации о населенном пункте...")
        self.statusBar.showMessage('Пожалуйста, подождите...')
        self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
        QtWidgets.QApplication.processEvents()

        list_city = self.listCity.currentIndex()
        
        # Выполнение загрузки в новом потоке.
        self.parser_data = Parsing(list_city, 0, "data")
        self.parser_data.finished.connect(self.dataFinished)
        self.parser_data.start()
        
    def parsing_date_load(self, method):
        num_error = 0
        if self.check_inCity() == 0:
            return num_error
        self.statusBar.showMessage('Пожалуйста, подождите...')
        self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")

        lc = self.listCity
        list_city = lc.currentIndex()
        if lc is None or lc == '' or len(lc) == 0 or list_city == -1 :
            self.statusBar.showMessage('Не-а, не так быстро :)', 10000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.textConsole.append("Выполните поиск или выберите город из списка")
            self.opacity(self.btnDwnld_T, True )
            self.opacity(self.btnParse, True )
            self.btnParse.setText('Скачать архив')
            self.btnDwnld_T.setText('Подгрузить температуру')
            return num_error

        self.textConsole.append("...")
        self.textConsole.append("Проверка введенных данных...")
        QtWidgets.QApplication.processEvents()

        num_error = 2

        date_start = self.dateEdit_start.text()
        date_end = self.dateEdit_end.text()
        
        if method == 1:
            parsingSelenium.input_date(date_start, date_end)
        elif method == 2:
            parsingSelenium.input_date_statist(date_start, date_end)
            
        QtWidgets.QApplication.processEvents()
        return num_error

    def parsing_download(self):
        self.btnParse.setEnabled(False)
        self.btnParse.setText('Скачивание...')
        self.statusBar.showMessage('Пожалуйста, подождите...')
        self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
        QtWidgets.QApplication.processEvents()

        check = self.parsing_date_load(1)
        if check == 0 or check == 1 :
            self.btnParse.setEnabled(True)
            return

        self.textConsole.append("...")
        self.textConsole.append("Формирование ссылки... *Может занять до 30сек")
        self.statusBar.showMessage('Пожалуйста, подождите...')
        self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
        QtWidgets.QApplication.processEvents()
        
        # Выполнение загрузки в новом потоке.
        self.parser_download = Parsing(0, 0, "download")
        self.parser_download.finished.connect(self.downloadFinished)
        self.parser_download.start()

    def parsing_load(self):
        self.statusBar.showMessage('Пожалуйста, подождите...')
        self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
        self.opacity(self.btnDwnld_T, False)
        self.btnDwnld_T.setText('Подгрузка...')
        QtWidgets.QApplication.processEvents()

        check = self.parsing_date_load(2)
        if check == 0 or check == 1 :
            return

        self.textConsole.append("...")
        self.textConsole.append("Выполняется подгрузка...")
        self.statusBar.showMessage('Пожалуйста, подождите...')
        self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
        QtWidgets.QApplication.processEvents()
        
        # Выполнение загрузки в новом потоке.
        self.parser_load = Parsing(0, 0, "load")
        self.parser_load.finished.connect(self.loadFinished)
        self.parser_load.start()
    
    def downloadFinished(self):
        if self.parser_download.return_download == 1:
            self.textConsole.append("Ссылка сформирована! Скачивание файла...")
            QtWidgets.QApplication.processEvents()
            # window.import_rp5()
            self.textConsole.append("Файл загружен! Данные внесены в поля с пометкой RP5. Архив находится в arhiv.xls.gz")
            self.statusBar.showMessage('Файл загружен!', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(48, 219, 91)")
            QTimer.singleShot(5000, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))
        else:
            self.textConsole.append("Не получилось сформировать ссылку, попробуйте загрузить еще раз *При большой выборке файл загружается с 2-3 раза")
            self.statusBar.showMessage('Ссылка не сформирована', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            QTimer.singleShot(5000, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))
        self.opacity(self.btnParse, True )
        # Удаление потока после его использования.
        self.btnParse.setText('Скачать архив')
        del self.parser_download
        
    def loadFinished(self):
        print(self.parser_load.return_download)
        if self.parser_load.return_download['num_error'] == 1:
            self.textConsole.append("Подгрузка выполнена!")
            QtWidgets.QApplication.processEvents()
            self.textConsole.append(f"Выборка: {str(self.parser_load.return_download['all_range'])}")
            self.textConsole.append(f"Число наблюдений: {str(self.parser_load.return_download['number_of_observations'])}")
            self.textConsole.append(f"Температура:")
            self.textConsole.append(f"- Минимум: {str(self.parser_load.return_download['min_temp'])} {str(self.parser_load.return_download['date_min_temp'])}")
            self.textConsole.append(f"- Максимум: {str(self.parser_load.return_download['max_temp'])} {str(self.parser_load.return_download['date_max_temp'])}")
            self.textConsole.append(f"- Средняя: {str(self.parser_load.return_download['average_temp'])}")
            self.textConsole.append(f"Давление:")
            self.textConsole.append(f"- Среднее: {str(self.parser_load.return_download['average_pressure'])}")
            self.textConsole.append(f"Влажность воздуха:")
            self.textConsole.append(f"- Средняя: {str(self.parser_load.return_download['average_humidity'])}")
            self.textConsole.append(f"Ветер:")
            self.textConsole.append(f"- Преобладающий: {str(self.parser_load.return_download['main_wind'])}")
            self.textConsole.append(f"- Средняя скорость: {str(self.parser_load.return_download['average_speed_wind'])}")
            self.textConsole.append(f"- Максимальная скорость: {str(self.parser_load.return_download['max_speed_wind'])}")
            self.textConsole.append(f"Осадки:")
            self.textConsole.append(f"- Максимальные за 12 часов: {str(self.parser_load.return_download['precipitation_on_12_hour'])}")
            self.textConsole.append(f"Снежный покров:")
            self.textConsole.append(f"- Средняя высота: {str(self.parser_load.return_download['average_height_snow'])}")
            self.textConsole.append(f"- Максимальная высота: {str(self.parser_load.return_download['max_height_snow'])}")
            self.textConsole.append(f"- Ранняя дата наличия: {str(self.parser_load.return_download['first_date_snow'])}")
            self.textConsole.append(f"- Поздняя дата наличия: {str(self.parser_load.return_download['last_date_snow'])}")
            self.statusBar.showMessage('Данные успешно подгружены!', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(48, 219, 91)")
            QTimer.singleShot(5000, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))
            self.parse_params = self.parser_load.return_download.copy()
        else:
            self.textConsole.append("Не рассчиталось, попробуйте подгрузить еще раз")
            self.statusBar.showMessage('Проблема', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            QTimer.singleShot(5000, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))
        # Удаление потока после его использования.
        self.opacity(self.btnDwnld_T, True )
        self.btnDwnld_T.setText('Подгрузить температуру')
        del self.parser_load
        
    def dataFinished(self):
        self.textConsole.append(f"Выбран: {str(self.parser_data.current_city['view_city'])}, №: {str(self.parser_data.current_city['num_weather_station'])},{str(self.parser_data.current_city['strt_monit'])}")
        self.statusBar.showMessage('Населенный пункт подгружен', 5000)
        self.statusBar.setStyleSheet("background-color:rgb(48, 219, 91)")
        QTimer.singleShot(5000, lambda: self.statusBar.setStyleSheet("background-color: rgb(255, 255, 255)"))
        self.parse_params_current_city = self.parser_data.current_city.copy()
        # Удаление потока после его использования.
        self.opacity(self.btnDwnld_T, True)
        self.opacity(self.btnParse, True)
        self.opacity(self.listCity, True)
        del self.parser_data

    def searchFinished(self):
        if self.parser_search.return_search == 0:
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.statusBar.showMessage('Что-то пошло не так!', 5000)
            QTimer.singleShot(5000, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))
            self.opacity(self.btnDwnld_T, True)
            self.opacity(self.btnParse, True)
            self.btnSearch.setEnabled(True)
            self.btnSearch.setText('Найти')
            return self.textConsole.append("По Вашему запросу ничего не найдено")
        elif self.parser_search.return_search == 1:
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.statusBar.showMessage('Что-то пошло не так!', 5000)
            QTimer.singleShot(5000, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))
            self.opacity(self.btnDwnld_T, True)
            self.opacity(self.btnParse, True)
            self.btnSearch.setEnabled(True)
            self.btnSearch.setText('Найти')
            return self.textConsole.append("Нет подключения к сети интернет")
        all_parameters = list(map(', '.join, self.parser_search.return_search[1])) # ['1234', '5678']
        self.textConsole.append(str(self.parser_search.return_search[0]))
        self.listCity.addItems(all_parameters)
        self.textConsole.append("Поиск закончен, выберите город из списка выше")
        self.statusBar.showMessage('Успешно!', 5000)
        self.statusBar.setStyleSheet("background-color:rgb(48, 219, 91)")
        QTimer.singleShot(5000, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))
        self.opacity(self.btnDwnld_T, True)
        self.opacity(self.btnParse, True)
        self.btnSearch.setEnabled(True)
        self.btnSearch.setText('Найти')
        # Удаление потока после его использования.
        del self.parser_search

    def closeFinished(self):
        # Удаление потока после его использования.
        del self.parser_close

def main():
    global window
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainApp()  # Создаём объект класса ExampleApp
    window.setWindowIcon(QtGui.QIcon('Data/icons/graficon.png'))
    window.show()  # Показываем окно
    window.setFixedSize(820,420)
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
    
