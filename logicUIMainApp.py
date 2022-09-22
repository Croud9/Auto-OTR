# перевод дизайна
# cd "C:\PythonPRJCT\autoReportPdf"
# pyuic5 designRepPDF.ui -o designRepPDF.py
# pyuic5 designParsing.ui -o designParsing.py
# pyuic5 designDrawSchemes.ui -o designDrawSchemes.py
# pyuic5 designDrawSchemesTwo.ui -o designDrawSchemesTwo.py

import pdf_builder
import designRepPDF # загрузка файлов
import logicUIParse
import logicUIOneScheme
import logicUITwoScheme
import search_data
import encode_file
import geocoding
import glob, fitz, requests, sys, os # загрузка модулей
from os.path import isfile, join
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from PyPDF2 import PdfFileMerger
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.Qt import *
from PyQt5.QtCore import QTimer, QThread, Qt
from datetime import date
import wikipedia
wikipedia.set_lang("ru")

path_to_pdf_pvsyst = "Data/PDF in/PVsyst"
path_to_pdf_schemes = "Data/PDF in/Shemes"
path_to_schemes = "Data/Schemes"
path_to_invertors = "Data/Modules/Invertors"
path_to_pv = "Data/Modules/PV's"
path_to_ktp = "Data/Modules/KTP's" 

class BuildDoc(QThread):
    def __init__(self, params):
        super().__init__()
        self.params = params

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
            # rew = pdf_builder.docPDF()
            # rew.convert_to_pdf(self.paths[0], path_to_pdf_schemes +"/General/generalScheme.pdf")
            renderPDF.drawToFile(svg2rlg(self.paths[0]), path_to_pdf_schemes +"/General/generalScheme.pdf")
        elif self.flag == 'detailed':
            for i in range(len(self.paths)):
                renderPDF.drawToFile(svg2rlg(self.paths[i]), path_to_pdf_schemes + f"/Detailed/detailed{i}.pdf")
        elif self.flag == 'pvsyst':
            # To get better resolution
            self.found_pdf = search_data.search_in_pdf(self.paths)
            zoom_x = 2.0  # horizontal zoom
            zoom_y = 2.0  # vertical zoom
            mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension         
            all_files = glob.glob(self.paths)
            for filename in all_files:
                with fitz.open(filename) as doc:  
                    for page in doc:  # iterate through the pages
                        pix = page.get_pixmap(matrix=mat)  # render page to an image #matrix=mat
                        pix.save(f"Data/Images/PVsyst/page-{page.number + 1}.png")  # store image as a PNG  

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
        self.listPV_file.activated.connect(self.pv_load)
        self.inputAddress.selectionChanged.connect(self.show_button_coordinates)
        self.btnSearchCoordinates.clicked.connect(self.coordinate_by_address)
        self.inputTitleProject.textChanged.connect(self.generate_code_project)
        self.btnDelPvsystData.clicked.connect(self.del_pvsyst)
        self.btnDelSchemeOneData.clicked.connect(self.del_scheme_one)
        self.btnDelSchemeTwoData.clicked.connect(self.del_scheme_two)
        self.btnAddInvertor.clicked.connect(self.add_invertor)
        self.btnDelInvertor.clicked.connect(self.del_invertor)
        self.spinBox_numInvertor.valueChanged.connect(self.up_down_ivertor_selection)

    def instance_ofter_class(self, instance_of_main_window): 
        self.w2 = logicUIParse.WindowParse()
        self.w3 = logicUIOneScheme.WindowDraw(instance_of_main_window)
        self.w4 = logicUITwoScheme.WindowDrawTwo(instance_of_main_window)

    def input_data(self):
        climat = wikipedia.page("Оренбург Климат").content
        if 'Климат' in climat:
            print(climat)
        # self.spinBox_numInvertor.lineEdit().setDisabled(True) 
        self.path_pvsyst = ''
        self.pathes_detail_schemes = []
        self.path_general_schemes = ['']
        self.invertors = {}
        self.spinBox_numInvertor.setMinimum(1)
        self.invertors['found_invertor_0'] = search_data.null_search_params('invertor')
        # self.found_invertor = search_data.null_search_params('invertor')
        self.found_pv = search_data.null_search_params('pv')
        self.found_pdf = search_data.null_search_params('pvsyst')
        self.parse_params = search_data.null_search_params('weather')
        self.weather_station_params = search_data.null_search_params('weather_station')
        self.browser_status = None
        
        self.inputTitleProject.setText("ШЛЮМБЕРЖЕ. ЛИПЕЦК. СЭС 363,4 КВТ")
        self.inputCodeProject.setText("ШЛМ2022")
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
        company_pv = sorted(os.listdir(path_to_pv))
        company_ktp = sorted(os.listdir(path_to_ktp))
        self.listInvertor_folder.addItems(company_invertor)
        self.listPV_folder.addItems(company_pv)
        self.listKTP_folder.addItems(company_ktp)

    def open_result_doc(self):
        os.startfile("Data\Report\Auto-OTR.pdf")

    def hide_del_button(self):
        fp_general = path_to_pdf_schemes + "/General"
        fp_detailed = path_to_pdf_schemes + "/Detailed"
        patch_imgs_pvsyst = "Data/Images/PVsyst"
        img_files_pvsyst = [f for f in os.listdir(patch_imgs_pvsyst) if os.path.isfile(os.path.join(patch_imgs_pvsyst, f))]
        files_in_detailed = [f for f in os.listdir(fp_detailed) if isfile(join(fp_detailed, f))]
        files_in_general = [f for f in os.listdir(fp_general) if isfile(join(fp_general, f))]
        if len(img_files_pvsyst) == 0:
            self.btnDelPvsystData.hide()
        else: 
            self.btnDelPvsystData.show()
            
        if len(files_in_detailed) == 0:
            self.btnDelSchemeOneData.hide()
        else: 
            self.btnDelSchemeOneData.show()

        if len(files_in_general) == 0:
            self.btnDelSchemeTwoData.hide()
        else: 
            self.btnDelSchemeTwoData.show()

    def validation(self):
        if self.listRoof.currentText() == "Выберите":
            self.statusBar.showMessage('Выберите тип крыши', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.listRoof.setStyleSheet("QComboBox{background-color:rgba(229,229,234,1); border: 1.45px solid red; border-radius: 6; padding-left: 6.55px;} QComboBox:drop-down {width: 0px; height: 0px; border: 0px;}")
            return 0
        else:
            self.set_style_default()

    def checkNet(self):
        try:
            response = requests.get("http://www.google.com")
            self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)")
            return 1
        except requests.ConnectionError:
            self.statusBar.showMessage('Нет подключения к интернету', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            QTimer.singleShot(5000, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))
            return 0

    def set_style_default(self):
        self.listRoof.setStyleSheet("QComboBox{\n	background-color:rgba(229,229,234,1); \n	border: none;\n	border-radius: 6;\n	padding-left: 8px;\n}\n\nQComboBox:drop-down \n{\n    width: 0px;\n    height: 0px;\n    border: 0px;\n}\nQComboBox:hover{\n	background-color:rgba(242,242,247,1);\n}\n")
        self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.statusBar.showMessage('', 100)
 
    def closeEvent(self, event):
        self.statusBar.showMessage('Браузер закрывается, пожалуйста, подождите...')
        self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
        QtWidgets.QApplication.processEvents()
        
        # Выполнение загрузки в новом потоке.
        self.parser_close = logicUIParse.Parsing(0, 0, "close")
        self.parser_close.finished.connect(self.closeFinished)
        self.parser_close.start()     

    def coordinate_by_address(self):
        coord = geocoding.get_coordinates_by_full_address(self.inputAddress.text())
        if not 'error' in coord:
            self.inputAddressLat.setText(coord['latitude'])
            self.inputAddressLong.setText(coord['longitude'])
            self.inputAddress.setText(coord['full_address'])
            self.w2.inputCity.setText(coord['city'])

        else:
            self.statusBar.showMessage(coord['error'], 4000)
            self.statusBar.setStyleSheet("background-color:rgba(255, 169, 31, 0.89)")
            QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))

    def show_button_coordinates(self):
        if self.btnSearchCoordinates.isHidden():
            self.btnSearchCoordinates.show()

    def generate_code_project(self):
        full_title = self.inputTitleProject.text()
        not_vowels_and_num = ''.join([letter for letter in full_title if letter not in 'ьЬъЪ-ауоыиэяюёеАУОЫИЭЯЮЁЕ0123456789,. ']).upper()
        current_year = str(date.today().year)
        self.inputCodeProject.setText(not_vowels_and_num[:3] + current_year)

    def hide(self):
        self.btnDelInvertor.hide() 
        self.btnOpenPDF.hide() 
        self.btnSearchCoordinates.hide()
        self.btnDelPvsystData.hide()
        self.btnDelSchemeOneData.hide()
        self.btnDelSchemeTwoData.hide()
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
            self.btnSearchCoordinates.hide()
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
            self.btnDelInvertor.hide() 
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
            self.btnSearchCoordinates.hide()
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
            if len(self.invertors) > 1:
                self.spinBox_numInvertor.show()
                self.btnDelInvertor.show() 
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
            self.btnDelInvertor.hide() 
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
            self.btnSearchCoordinates.hide()
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
        if self.browser_status == None:
            if self.checkNet() == 0:
                return
            # self.btnRP5
            self.btnRP5.setEnabled(False)
            self.btnRP5.setText('Запуск..')
            self.statusBar.showMessage('Идет первоначальный запуск браузера, пожалуйста, подождите...')
            self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
            self.parser_open = logicUIParse.Parsing(0, 0, "open")
            self.parser_open.finished.connect(self.showParserFinished)
            self.parser_open.start()
        elif self.w2.isHidden():
            self.w2.setWindowIcon(QtGui.QIcon('Data/icons/graficon.png'))
            self.w2.show()
            self.w2.setFixedSize(470, 430)

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
            self.hide_del_button()
        else:   
            self.btnDrawScheme.hide()
            self.btnDrawSchemeTwo.hide()
            self.btnLoadScheme1.hide()
            self.btnLoadScheme2.hide()
            self.btnDelSchemeOneData.hide()
            self.btnDelSchemeTwoData.hide()

    def roof_select(self):
        self.current_roof = self.listRoof.currentIndex()

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
            modules_file = f'{path_to_pv}/{self.select_title_pv}'
            self.type_pv_modules = sorted(os.listdir(modules_file))
            names_modules = []
            for name in self.type_pv_modules:
                names_modules.append(name.split(".")[0])
            self.listPV_file.addItems(names_modules)
            
    def ktp_select(self):
        self.listKTP_file.clear()
        if self.listInvertor_folder.currentText() != "Выберите":
            self.select_title_ktp = self.listKTP_folder.currentText() 
            modules_file = f'{path_to_ktp}/{self.select_title_ktp}'
            self.type_ktp_modules = sorted(os.listdir(modules_file))
            names_modules = []
            for name in self.type_ktp_modules:
                names_modules.append(name.split(".")[0])
            self.listKTP_file.addItems(names_modules)

    def invertor_load(self):
        current_invertor = self.listInvertor_file.currentText()
        for select_invertor in self.type_modules:
            if current_invertor in select_invertor: 
                self.invertors[f'found_invertor_{self.spinBox_numInvertor.value() - 1}'] = search_data.search_in_invertor(f"{path_to_invertors}/{self.select_title_invertor}/{select_invertor}") 
                current = self.invertors[f'found_invertor_{self.spinBox_numInvertor.value() - 1}']
                current['file'] = self.listInvertor_file.currentIndex()
                current['folder'] = self.listInvertor_folder.currentIndex()
                self.w3.set_invertor_params(current['module'], current['mppt'], current['inputs']) # вставка параметров в окно первой схемы
                self.w4.set_invertor_params(current['module'], current['p_max'], current['i_out_max']) # вставка параметров в окно второй схемы
                print(self.invertors)
                
    def pv_load(self):
        current_pv = self.listPV_file.currentText()
        for select_pv in self.type_pv_modules:
            if current_pv in select_pv: 
                self.found_pv = search_data.search_in_pv(f"{path_to_pv}/{self.select_title_pv}/{select_pv}") 
    
    def add_invertor(self):
        self.spinBox_numInvertor.show()
        self.btnDelInvertor.show() 
        self.listInvertor_file.clear()
        self.listInvertor_folder.setCurrentIndex(0)
        self.invertors[f'found_invertor_{len(self.invertors)}'] = search_data.null_search_params('invertor')
        self.spinBox_numInvertor.setMinimum(1)
        self.spinBox_numInvertor.setMaximum(len(self.invertors))
        self.spinBox_numInvertor.setValue(len(self.invertors))

    def del_invertor(self):
        if len(self.invertors) > 1:
            del self.invertors[f'found_invertor_{self.spinBox_numInvertor.value() - 1}']
            self.spinBox_numInvertor.setMaximum(len(self.invertors))
            self.spinBox_numInvertor.setValue(len(self.invertors))
            index = 0
            for key in list(self.invertors.keys()):
                self.invertors[f'found_invertor_{index}'] = self.invertors.pop(key)
                index += 1
            self.up_down_ivertor_selection()
        if len(self.invertors) == 1:
            self.btnDelInvertor.hide()
            self.spinBox_numInvertor.hide()

    def up_down_ivertor_selection(self):
        # self.spinBox_numInvertor.lineEdit().deselect()
        current = self.invertors[f'found_invertor_{self.spinBox_numInvertor.value() - 1}']
        if 'folder' in current:
            self.listInvertor_folder.setCurrentIndex(current['folder'])
            self.invertor_select()
            if 'file' in current:
                self.listInvertor_file.setCurrentIndex(current['file'])
            else:
                self.listInvertor_file.clear()
        else:
            self.listInvertor_folder.setCurrentIndex(0)
            self.listInvertor_file.clear()

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

    def del_pvsyst(self):
        self.delete_pdf('pvsyst')
        self.found_pdf = search_data.null_search_params('pvsyst')
        self.path_pvsyst = ''
        self.hide_del_button()
        self.statusBar.showMessage('Файл PVsyst исключен из отчета', 2500)
        self.statusBar.setStyleSheet("background-color: rgba(229,229,234,1); color:  #3b83ff; font-weight: bold;")
        QTimer.singleShot(2500, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))

    def del_scheme_one(self):
        self.delete_pdf('detailed')
        self.hide_del_button()
        self.statusBar.showMessage('Файл первого чертежа исключен из отчета', 2500)
        self.statusBar.setStyleSheet("background-color: rgba(229,229,234,1); color:  #3b83ff; font-weight: bold;")
        QTimer.singleShot(2500, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))

    def del_scheme_two(self):
        self.delete_pdf('general')
        self.hide_del_button()
        self.statusBar.showMessage('Файл второго чертежа исключен из отчета', 2500)
        self.statusBar.setStyleSheet("background-color: rgba(229,229,234,1); color:  #3b83ff; font-weight: bold;")
        QTimer.singleShot(2500, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))
        
    def pvsyst(self):
        self.path_pvsyst = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', path_to_pdf_pvsyst, "*.pdf")[0] #открытие диалога для выбора файла
        print(self.path_pvsyst)
        self.hide_del_button()
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
        self.hide_del_button()
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
        self.hide_del_button()
        if len(self.path_general_schemes[0]) != 0:
            self.delete_pdf('general')
            self.textConsole.append("- Загружена структурная эл.схема ")
            self.btnLoadScheme2.setEnabled(False)
            self.converter2 = СonvertFiles(self.path_general_schemes, 'general')
            self.converter2.finished.connect(self.convertTwoFinished)
            self.converter2.start()

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
        block_1 = True if self.checkBox_1.isChecked() else False
        block_2 = True if self.checkBox_2.isChecked() else False
        block_3 = True if self.checkBox_3.isChecked() else False
        block_3_1 = True if self.checkBox_3_1.isChecked() else False
        block_3_2 = True if self.checkBox_3_2.isChecked() else False
        block_3_3 = True if self.checkBox_3_3.isChecked() else False
        block_3_4 = True if self.checkBox_3_4.isChecked() else False
        block_4 = True if self.checkBox_4.isChecked() else False
        block_5 = True if self.checkBox_5.isChecked() else False
        block_5_1 = True if self.checkBox_5_1.isChecked() else False
        block_5_1_1 = True if self.checkBox_5_1_1.isChecked() else False
        block_5_1_2 = True if self.checkBox_5_1_2.isChecked() else False
        block_5_1_3 = True if self.checkBox_5_1_3.isChecked() else False
        block_5_1_4 = True if self.checkBox_5_1_4.isChecked() else False
        block_5_2 = True if self.checkBox_5_2.isChecked() else False
        block_5_3 = True if self.checkBox_5_3.isChecked() else False
        block_5_4 = True if self.checkBox_5_4.isChecked() else False
        block_5_5 = True if self.checkBox_5_5.isChecked() else False
        block_5_6 = True if self.checkBox_5_6.isChecked() else False
        block_6 = True if self.checkBox_6.isChecked() else False
        block_7 = True if self.checkBox_7.isChecked() else False
        block_8 = True if self.checkBox_8.isChecked() else False
        block_8_1 = True if self.checkBox_8_1.isChecked() else False
        block_8_2 = True if self.checkBox_8_2.isChecked() else False
        block_8_3 = True if self.checkBox_8_3.isChecked() else False
        block_8_4 = True if self.checkBox_8_4.isChecked() else False
        block_8_5 = True if self.checkBox_8_5.isChecked() else False
        block_8_6 = True if self.checkBox_8_6.isChecked() else False
        title_project = self.inputTitleProject.text()
        code_project = self.inputCodeProject.text()
        client = self.inputClient.text()
        u_dot_in = self.inputUDotIn.text()
        address = self.inputAddress.text()
        type_object = self.inputObjectType.text()
        latitude = self.inputAddressLat.text()
        longitude = self.inputAddressLong.text()
        self.object_passport = {'title_project': title_project, 'code_project': code_project, 'client': client, 'u_dot_in': u_dot_in,
                                'address': address, 'type_object': type_object, 'lati_ui': latitude, 'longi_ui': longitude}
        self.blocks = {'block_1': block_1, 'block_2': block_2, 'block_3': block_3, 
                    'block_3_1': block_3_1, 'block_3_2': block_3_2, 'block_3_3': block_3_3, 'block_3_4': block_3_4, 
                    'block_4': block_4, 'block_5': block_5, 'block_5_1': block_5_1, 'block_5_1_1': block_5_1_1, 
                    'block_5_1_2': block_5_1_2, 'block_5_1_3': block_5_1_3, 'block_5_1_4': block_5_1_4, 
                    'block_5_2': block_5_2, 'block_5_3': block_5_3, 'block_5_4': block_5_4, 'block_5_5': block_5_5, 
                    'block_5_6': block_5_6, 'block_6': block_6, 'block_7': block_7, 'block_8': block_8,
                    'block_8_1': block_8_1, 'block_8_2': block_8_2, 'block_8_3': block_8_3, 
                    'block_8_4': block_8_4, 'block_8_5': block_8_5, 'block_8_6': block_8_6,}
        self.weather = self.w2.parse_params if hasattr(self.w2, 'parse_params') else self.parse_params
        self.weather_station = self.w2.parse_params_current_city if hasattr(self.w2, 'parse_params_current_city') else self.weather_station_params
        
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
            
            main_params = {'path_to_pvsyst': self.path_pvsyst, 'roof': self.current_roof, 'invertors': self.invertors,
                            **self.blocks, **self.object_passport, 
                            **self.weather, **self.weather_station, **self.found_pdf, **self.found_pv}
            print(main_params)
            
            self.btnForm.setEnabled(False)
            self.btnForm.setText('Формирование отчета...')
            self.statusBar.showMessage('Пожалуйста, подождите...')
            self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
            # Выполнение загрузки в новом потоке.
            self.builder = BuildDoc(main_params)
            self.builder.finished.connect(self.buildFinished)
            self.builder.start()

    def showParserFinished(self):
        self.browser_status = self.parser_open.browser_status
        if self.browser_status == 0:
            self.w2.setWindowIcon(QtGui.QIcon('Data/icons/graficon.png'))
            self.w2.show()
            self.w2.setFixedSize(470, 430)

            self.statusBar.showMessage('Успешно!', 4000)
            self.statusBar.setStyleSheet("background-color:rgb(48, 219, 91)")
            QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))
            self.btnRP5.setEnabled(True)
            self.btnRP5.setText('RP5')
        else:
            self.statusBar.showMessage('Что-то пошло не так с браузером, попробуйте запустить снова')
            self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
            self.btnRP5.setEnabled(True)
            self.btnRP5.setText('RP5')
        del self.parser_open

    def closeFinished(self):
        del self.parser_close  

    def convertOneFinished(self):
        self.btnLoadScheme1.setEnabled(True)
        self.hide_del_button()
        del self.converter1
        
    def convertTwoFinished(self):
        self.btnLoadScheme2.setEnabled(True)
        self.hide_del_button()
        del self.converter2
                       
    def convertPvsystFinished(self):
        self.found_pdf = self.converter_pvsyst.found_pdf 
        self.inputAddressLat.setText(self.found_pdf['lati_pdf'])
        self.inputAddressLong.setText(self.found_pdf['longi_pdf'])
        full_address = geocoding.get_full_address_by_coordinates(self.found_pdf['lati_pdf'], self.found_pdf['longi_pdf'])
        self.inputAddress.setText(full_address['full_address'])
        self.w2.inputCity.setText(full_address['city_point'])
        self.btnOne.setEnabled(True)
        self.hide_del_button()
        del self.converter_pvsyst

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

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainApp()  # Создаём объект класса ExampleApp
    window.setWindowIcon(QtGui.QIcon('Data/icons/graficon.png'))
    window.show()  # Показываем окно
    window.setFixedSize(820,420)
    window.instance_ofter_class(window)
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':
    main()

