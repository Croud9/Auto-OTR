# перевод дизайна
# cd "C:\PythonPRJCT\autoReportPdf"
# pyuic5 designCalcPV.ui -o designCalcPV.py
# pyuic5 designRepPDF.ui -o designRepPDF.py
# pyuic5 designParsing.ui -o designParsing.py
# pyuic5 designDrawSchemes.ui -o designDrawSchemes.py
# pyuic5 designDrawSchemesTwo.ui -o designDrawSchemesTwo.py
# pyuic5 designDrawStructuralScheme.ui -o designDrawStructuralScheme.py
# pyuic5 designAbout.ui -o designAbout.py

from numpy import true_divide
import pdf_builder
import designRepPDF # загрузка файлов
import logicUICalcPV
import logicUIAbout
import logicUIParse
import logicUIOneScheme
import logicUITwoScheme
import logicUIStructuralScheme
import search_data
import validate
import geocoding
import styles_responce
import glob, fitz, sys, os # загрузка модулей
os.environ['path'] += r';Data/file_sys/dlls' # для работы cairosvg
import cairosvg
from os.path import isfile, join
from PyPDF2 import PdfFileMerger
from datetime import date
from PyQt5 import QtWidgets, QtGui, QtSvg
from PyQt5.QtGui import QIcon, QMovie, QTextCursor
from PyQt5.QtCore import QSize, QTimer, QThread
from PyQt5.QtWidgets import QLabel
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
            cairosvg.svg2pdf(url = self.paths[0], write_to = path_to_pdf_schemes +"/General/generalScheme.pdf")  
        if self.flag == 'structural':
            cairosvg.svg2pdf(url = self.paths[0], write_to = path_to_pdf_schemes +"/Structural/structural.pdf")  
        elif self.flag == 'detailed':
            for i in range(len(self.paths)):
                cairosvg.svg2pdf(url = self.paths[i], write_to = path_to_pdf_schemes + f"/Detailed/detailed{i}.pdf")  
        elif self.flag == 'pvsyst':
            # To get better resolution
            self.found_pdf = search_data.search_in_pdf(self.paths)
            try:
                if validate.internet() == True:
                    self.full_address = geocoding.get_full_address_by_coordinates(self.found_pdf['lati_pdf'], self.found_pdf['longi_pdf'])
            except Exception:
                pass
            zoom_x = 2.0  # horizontal zoom
            zoom_y = 2.0  # vertical zoom
            mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension         
            all_files = glob.glob(self.paths)
            for filename in all_files:
                with fitz.open(filename) as doc:  
                    for page in doc:  # iterate through the pages
                        if page.number != 0:
                            pix = page.get_pixmap(matrix=mat)  # render page to an image #matrix=mat
                            pix.save(f"Data/Images/PVsyst/page-{page.number + 1}.png")  # store image as a PNG  

class MainApp(QtWidgets.QMainWindow, designRepPDF.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('Data/icons/graficon.png'))
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.hide()
        self.input_data()
        validate.validate_number(self.fields_text)
        self.internet_on()
        self.btnWifi.clicked.connect(self.internet_on)
        self.btnKTPTemplate.clicked.connect(self.pattern_ktp)
        self.btnOtherTemplate.clicked.connect(self.pattern_other)
        self.btnOpenPDF.clicked.connect(self.open_result_doc)
        self.btnInfo.clicked.connect(self.open_manual_doc)
        self.btnAbout.clicked.connect(self.show_window_about)
        self.btnOne.clicked.connect(self.load_pvsyst)
        self.btnForm.clicked.connect(self.create_document)
        self.btnRP5.clicked.connect(self.show_window_parse)
        self.btnDrawScheme.clicked.connect(self.show_window_draw)
        self.btnDrawSchemeTwo.clicked.connect(self.show_window_draw_two)
        self.btnDrawStructuralScheme.clicked.connect(self.show_window_draw_structural)
        self.btnCalcPV.clicked.connect(self.show_window_calc)
        self.checkBox_3.clicked.connect(self.show_and_hide_cbox3)
        self.checkBox_5.clicked.connect(self.show_and_hide_cbox5)
        self.checkBox_8.clicked.connect(self.show_and_hide_cbox8)
        self.btnShow3.clicked.connect(self.show_btn_cbox3)
        self.btnShow5.clicked.connect(self.show_btn_cbox5)
        self.btnShow8.clicked.connect(self.show_btn_cbox8)
        self.btnLoadScheme1.clicked.connect(self.load_scheme_one)
        self.btnLoadScheme2.clicked.connect(self.load_scheme_two)
        self.btnLoadStructScheme.clicked.connect(self.load_structural_scheme)
        self.btnLoadPlaneSet.clicked.connect(self.load_plane_set_scheme)
        self.btnAddKTPParams.clicked.connect(self.generate_ktp_file)
        self.listRoof.activated.connect(self.select_roof)
        self.listInvertor_folder.activated.connect(self.select_invertor)
        self.listInvertor_file.activated.connect(self.load_invertor)
        self.listPV_folder.activated.connect(self.select_pv)
        self.listPV_file.activated.connect(self.load_pv)
        self.listKTP_folder.activated.connect(self.select_other)
        self.listKTP_file.activated.connect(self.load_other)
        self.inputAddress.selectionChanged.connect(self.show_button_coordinates)
        self.btnSearchCoordinates.clicked.connect(self.coordinate_by_address)
        self.inputTitleProject.textChanged.connect(self.generate_code_project)
        self.btnDelPvsystData.clicked.connect(self.del_pvsyst)
        self.btnDelSchemeOneData.clicked.connect(self.del_scheme_one)
        self.btnDelSchemeTwoData.clicked.connect(self.del_scheme_two)
        self.btnDelStructScheme.clicked.connect(self.del_structural_scheme)
        self.btnDelPlaneSet.clicked.connect(self.del_plane_set)
        self.btnAddInvertor.clicked.connect(self.add_invertor)
        self.btnDelInvertor.clicked.connect(self.del_invertor)
        self.btnAddPV.clicked.connect(self.add_pv)
        self.btnDelPV.clicked.connect(self.del_pv)
        self.btnAddKTP.clicked.connect(self.add_other)
        self.btnDelOther.clicked.connect(self.del_other)
        self.spinBox_numInvertor.valueChanged.connect(self.up_down_invertor_selection)
        self.spinBox_numPV.valueChanged.connect(self.up_down_pv_selection)
        self.spinBox_numKTP.valueChanged.connect(self.up_down_other_selection)

    def startAnimation(self):
        self.movie.start()
        self.labelLoading.show()
  
    def stopAnimation(self):
        self.movie.stop()
        self.labelLoading.hide()

    def instance_ofter_class(self, instance_of_main_window): 
        self.w2 = logicUIParse.WindowParse(instance_of_main_window)
        self.w3 = logicUIOneScheme.WindowDraw(instance_of_main_window)
        self.w4 = logicUITwoScheme.WindowDrawTwo(instance_of_main_window) 
        self.w5 = logicUICalcPV.CalcPV(instance_of_main_window) 
        self.w6 = logicUIStructuralScheme.WindowDrawStructural(instance_of_main_window) 
        self.w7 = logicUIAbout.WindowAbout(instance_of_main_window) 

    def hide(self):
        self.btnOpenPDF.hide()
        self.spinBox_numInvertor.hide()
        self.spinBox_numPV.hide()
        self.spinBox_numKTP.hide()
        self.btnDelInvertor.hide()
        self.btnDelPV.hide()
        self.btnDelOther.hide()
        self.btnDelPvsystData.hide()
        self.btnDelSchemeOneData.hide()
        self.btnDelSchemeTwoData.hide()
        self.btnDelStructScheme.hide()
        self.btnDelPlaneSet.hide()

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

    def pattern_ktp(self):
        self.inputKTP.clear()
        self.inputKTP.append('Тип оборудования=КТП') # Название КТП
        self.inputKTP.append('Название оборудования=КТПНУ-250/10/0,4-T-KK-УХЛ1') # Название КТП
        self.inputKTP.append('Сила тока, А=Введите значение') 
        self.inputKTP.append('Мощность, кВт=Введите значение') 
        self.inputKTP.append('Габаритные размеры, ДхШхВ, мм=5000x4800x3300') 
        self.inputKTP.append('Кол-во транспортных единиц, шт=2') 
        self.inputKTP.append('Масса, кг=13000') 
        self.inputKTP.append('Номинальное напряжение ВН, кВ=10') 
        self.inputKTP.append('Наибольшее рабочее напряжение, кВ=12') 
        self.inputKTP.append('Номинальная частота переменного тока, Гц=50') 
        self.inputKTP.append('Номинальный ток главный цепей вводных ячеек ВН, А=630') 
        self.inputKTP.append('Номинальный ток главный цепей, А=630') 
        self.inputKTP.append('Номинальный ток сборных шин, А=630') 
        self.inputKTP.append('Ток термической стойкости в  течение 1 сек. со стороны ВН, не менее, кА=13') 
        self.inputKTP.append('Ток электродинамической стойкости в  течение 1 сек. со стороны ВН, не менее, кА=17') 
        self.inputKTP.append('Номинальное напряжение НН, кВ=0,4') 
        self.inputKTP.append('Номинальный ток РУНН, А=400') 
        self.inputKTP.append('Тип системы заземления со стороны НН=TN-C-S') 
        self.inputKTP.append('Тип силового трансформатора Т1=ТЛС') 
        self.inputKTP.append('Мощность силового трансформатора Т1, кВ*А=250') 
        self.inputKTP.append('Способ и диапазон регулирования=ПБВ±2х2,5%') 
        self.inputKTP.append('Схема и группа соединения обмоток=Д/Ун-11') 
        self.inputKTP.moveCursor(QTextCursor.Start)

    def pattern_other(self):
        self.inputKTP.clear()
        self.inputKTP.append('Тип оборудования=Введите значение') # Название КТП
        self.inputKTP.append('Название оборудования=Введите значение') # Название КТП
        self.inputKTP.append('Мощность, кВт=Введите значение') # Название КТП
        self.inputKTP.append('Сила тока, А=Введите значение') # Название КТП
        self.inputKTP.append('! ДЛЯ АВТОЗАПОЛНЕНИЯ ПАРАМЕТРОВ СХЕМ, ПАРАМЕТРЫ ВЫШЕ ОБЯЗАТЕЛЬНЫ, ПРИ СОХРАНЕНИИ ФАЙЛА УДАЛИТЕ СТРОКИ НИЖЕ, ВКЛЮЧАЯ ЭТУ !') 
        self.inputKTP.append('Название параметра, Единица измерения=Значение') 
        self.inputKTP.append('Название параметра, Единица измерения=Значение') 
        self.inputKTP.append('Пример: (Номинальное напряжение ВН, кВ=10)') 

    def input_data(self):
        # self.btnDevice.setIcon(QIcon('data/cons/paper-clip.png'))
        # self.btnDevice.setIconSize(QSize(40, 40))
        self.btnLoadPlaneSet.setIcon(QIcon('data/cons/dop/terrain.png'))
        self.btnLoadPlaneSet.setIconSize(QSize(50, 50))
        self.btnDrawStructuralScheme.setIcon(QIcon('data/cons/dop/electrical-panel.png'))
        self.btnDrawStructuralScheme.setIconSize(QSize(45, 45))
        self.btnRP5.setIcon(QIcon('data/cons/cloud3.png'))
        self.btnRP5.setIconSize(QSize(50, 50))
        self.btnForm.setIcon(QIcon('data/cons/dop/analytic.png'))
        self.btnForm.setIconSize(QSize(50, 50))
        self.btnOne.setIcon(QIcon('data/cons/pvsyst.png'))
        self.btnOne.setIconSize(QSize(45, 45))
        self.btnDrawScheme.setIcon(QIcon('data/cons/dop/electric-panel1.png'))
        self.btnDrawScheme.setIconSize(QSize(45, 45))
        self.btnDrawSchemeTwo.setIcon(QIcon('data/cons/dop/solar-panels.png'))
        self.btnDrawSchemeTwo.setIconSize(QSize(50, 50))
        self.btnCalcPV.setIcon(QIcon('data/cons/dop/solar-panel1.png'))
        self.btnCalcPV.setIconSize(QSize(50, 50))
        self.btnInfo.setIcon(QIcon('data/cons/dop/question2.png'))
        self.btnInfo.setIconSize(QSize(20, 20))
        self.btnAbout.setIcon(QIcon('data/cons/dop/information2.png'))
        self.btnAbout.setIconSize(QSize(20, 20))
        self.btnAbout.move(5, 2)
        self.btnInfo.move(40, 2)

        self.btnWifi.resize(30, 30)
        self.btnWifi.move(190, 7)
        self.btnWifi.setIcon(QIcon('data/cons/dop/no-wifi.png'))
        self.btnWifi.setIconSize(QSize(25, 25))
        self.btnWifi.hide()
         
        self.pattern_other()
        # self.spinBox_numInvertor.lineEdit().setDisabled(True) 
        self.path_pvsyst = ''
        self.path_plane_set_schemes = ''
        self.pathes_detail_schemes = []
        self.path_structural_schemes = []
        self.path_general_schemes = []
        self.invertors = {}
        self.pvs = {}
        self.others = {}
        self.spinBox_numInvertor.setMinimum(1)
        self.spinBox_numPV.setMinimum(1)
        self.spinBox_numKTP.setMinimum(1)
        self.invertors['found_invertor_0'] = search_data.null_search_params('invertor')
        self.pvs['found_pv_0'] = search_data.null_search_params('pv')
        self.others['found_other_0'] = {}

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
        self.company_invertor = sorted(os.listdir(path_to_invertors))
        self.listInvertor_folder.addItems(self.company_invertor)

        self.listPV_folder.addItem("Выберите")
        self.company_pv = sorted(os.listdir(path_to_pv))
        self.listPV_folder.addItems(self.company_pv)
        
        self.listKTP_folder.addItem("Выберите")
        company_ktp = sorted(os.listdir(path_to_ktp))
        self.listKTP_folder.addItems(company_ktp)
        self.movie = QMovie('data/cons/loading_gif250trans.gif')
        self.labelLoading.setMovie(self.movie)
        self.fields_text = [self.inputUDotIn, self.inputAddressLat, self.inputAddressLong]

    def open_result_doc(self):
        os.startfile("Data\Report\Auto-OTR.pdf")

    def open_manual_doc(self):
        os.startfile("Data\Manual.pdf")

    def hide_del_button_schemes(self):
        fp_general = path_to_pdf_schemes + "/General"
        fp_detailed = path_to_pdf_schemes + "/Detailed"
        fp_structural = path_to_pdf_schemes + "/Structural"
        files_in_detailed = [f for f in os.listdir(fp_detailed) if isfile(join(fp_detailed, f))]
        files_in_general = [f for f in os.listdir(fp_general) if isfile(join(fp_general, f))]
        files_in_structural = [f for f in os.listdir(fp_structural) if isfile(join(fp_structural, f))]

        if len(files_in_detailed) == 0:
            self.btnDelSchemeOneData.hide()
        else: 
            self.btnDelSchemeOneData.show()

        if len(files_in_general) == 0:
            self.btnDelSchemeTwoData.hide()
        else: 
            self.btnDelSchemeTwoData.show()

        if len(files_in_structural) == 0:
            self.btnDelStructScheme.hide()
        else: 
            self.btnDelStructScheme.show()

        if self.path_plane_set_schemes == '':
            self.btnDelPlaneSet.hide()
        else: 
            self.btnDelPlaneSet.show()

    def hide_del_button_device(self):
        patch_imgs_pvsyst = "Data/Images/PVsyst"
        img_files_pvsyst = [f for f in os.listdir(patch_imgs_pvsyst) if os.path.isfile(os.path.join(patch_imgs_pvsyst, f))]

        if len(img_files_pvsyst) == 0:
            self.btnDelPvsystData.hide()
        else: 
            self.btnDelPvsystData.show()

    def validation(self):
        if self.listRoof.currentText() == "Выберите":
            self.statusBar.showMessage('Выберите тип крыши', 5000)
            self.statusBar.setStyleSheet(styles_responce.status_red)
            self.listRoof.setStyleSheet(styles_responce.warning_style_comboBox)
            return 0
        else:
            self.set_style_default()

    def internet_on(self):
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.6)
        if validate.internet() == True:
            self.statusBar.setStyleSheet(styles_responce.status_white)
            self.btnWifi.hide()
            self.btnRP5.setEnabled(True)
            self.btnRP5.setGraphicsEffect(self.opacity_effect.setOpacity(1))
            self.btnSearchCoordinates.setEnabled(True)
            self.btnSearchCoordinates.setGraphicsEffect(self.opacity_effect.setOpacity(1))
            return True
        else:
            self.btnRP5.setGraphicsEffect(self.opacity_effect)
            self.btnRP5.setEnabled(False)
            self.btnSearchCoordinates.setGraphicsEffect(self.opacity_effect)
            self.btnSearchCoordinates.setEnabled(False)
            self.btnWifi.show()
            return False

    def set_style_default(self):
        self.listRoof.setStyleSheet(styles_responce.default_style_comboBox)
        self.statusBar.setStyleSheet(styles_responce.status_white)
        self.statusBar.showMessage('', 100)
 
    def closeEvent(self, event):
        self.statusBar.showMessage('Браузер закрывается, пожалуйста, подождите...')
        self.statusBar.setStyleSheet(styles_responce.status_yellow)
        QtWidgets.QApplication.processEvents()
        del self.w2
        del self.w3
        del self.w4
        del self.w5 
        del self.w6 
        del self.w7 
        self.parser_close = logicUIParse.Parsing(0, 0, "close")
        self.parser_close.finished.connect(self.closeFinished)
        self.parser_close.start()     

    def coordinate_by_address(self):
        try:
            coord = geocoding.get_coordinates_by_full_address(self.inputAddress.text())
            if not 'error' in coord:
                self.inputAddressLat.setText(coord['latitude'])
                self.inputAddressLong.setText(coord['longitude'])
                self.inputAddress.setText(coord['full_address'])
                self.w2.inputCity.setText(coord['city'])
            else:
                self.statusBar.showMessage(coord['error'], 4000)
                self.statusBar.setStyleSheet(styles_responce.status_orange)
                QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))
        except Exception:
                self.statusBar.showMessage('Не подгруженны геоданные, повторите попытку', 4000)
                self.statusBar.setStyleSheet(styles_responce.status_orange)
                QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))

    def show_button_coordinates(self):
        if self.btnSearchCoordinates.isHidden():
            self.btnSearchCoordinates.show()

    def generate_code_project(self):
        full_title = self.inputTitleProject.text()
        not_vowels_and_num = ''.join([letter for letter in full_title if letter not in 'ьЬъЪ-ауоыиэяюёеАУОЫИЭЯЮЁЕ0123456789,. ']).upper()
        current_year = str(date.today().year)
        self.inputCodeProject.setText(not_vowels_and_num[:3] + current_year)

    def generate_ktp_file(self):
        params = self.inputKTP.toPlainText()
        file_name = self.inputNameFileKTP.text()

        if file_name == '':
            file_name = 'noname'

        with open(f"Data/Modules/KTP's/New/{file_name}.txt", 'w') as file:
            file.write(params) # Название КТП
        self.statusBar.showMessage('Файл создан!', 4000)
        self.statusBar.setStyleSheet(styles_responce.status_green)
        QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))
        self.select_other()
           
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

    def check_open_parse_window(self):
        if (self.browser_status == None or self.browser_status > 0) and self.w2.isHidden():
            print("Проверка связи")
            self.statusBar.showMessage('Браузер не может запуститься, возможно проблема в слабом интернет соединении')
            self.statusBar.setStyleSheet(styles_responce.status_red)
            QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))
            self.stopAnimation()
            # del self.parser_open
            self.btnRP5.setEnabled(True)

    def show_window_parse(self):  # открытие окна погоды
        QtWidgets.QApplication.processEvents()
        if self.browser_status == None or self.browser_status > 0:
            if self.internet_on() == False:
                return
            # self.btnRP5
            self.btnRP5.setEnabled(False)
            # self.btnRP5.setText('Запуск..')
            self.startAnimation()
            self.statusBar.showMessage('Идет первоначальный запуск браузера, пожалуйста, подождите...')
            self.statusBar.setStyleSheet(styles_responce.status_yellow)
            self.parser_open = logicUIParse.Parsing(0, 0, "open")
            QTimer.singleShot(30000, lambda: self.check_open_parse_window())
            self.parser_open.finished.connect(self.showParserFinished)
            self.parser_open.start()
        elif self.w2.isHidden():
            self.w2.setWindowIcon(QtGui.QIcon('Data/icons/graficon.png'))
            self.w2.setFixedSize(970, 430)
            self.w2.show()

    def show_window_about(self):  # открытие   окна рисования первой схемы
        self.w7.setWindowIcon(QtGui.QIcon('Data/icons/graficon.png'))
        self.w7.show()
        self.w7.setFixedSize(595, 325)

    def show_window_draw(self):  # открытие   окна рисования первой схемы
        self.w3.setWindowIcon(QtGui.QIcon('Data/icons/graficon.png'))
        self.w3.show()
        self.w3.setFixedSize(770, 475)

    def show_window_draw_two(self):  # открытие   окна рисования первой схемы
        self.w4.setWindowIcon(QtGui.QIcon('Data/icons/graficon.png'))
        self.w4.show()
        self.w4.setFixedSize(950, 335)

    def show_window_draw_structural(self):  # открытие   окна рисования первой схемы
        self.w6.setWindowIcon(QtGui.QIcon('Data/icons/graficon.png'))
        self.w6.show()
        self.w6.setFixedSize(380, 475)

    def show_window_calc(self):  # открытие   окна рисования первой схемы
        self.w5.setWindowIcon(QtGui.QIcon('Data/icons/graficon.png'))
        self.w5.show()
        self.w5.setFixedSize(1220,620)

    def select_roof(self):
        self.current_roof = self.listRoof.currentIndex()

    def select_invertor(self):
        self.listInvertor_file.clear()
        if self.listInvertor_folder.currentText() != "Выберите":
            self.select_title_invertor = self.listInvertor_folder.currentText() 
            modules_file = f'{path_to_invertors}/{self.select_title_invertor}'
            self.type_modules = sorted(os.listdir(modules_file))
            names_modules = []
            for name in self.type_modules:
                names_modules.append(name[:-4])
            self.listInvertor_file.addItems(names_modules)
        return names_modules
            
    def select_pv(self):
        self.listPV_file.clear()
        if self.listPV_folder.currentText() != "Выберите":
            self.select_title_pv = self.listPV_folder.currentText() 
            modules_file = f'{path_to_pv}/{self.select_title_pv}'
            self.type_pv_modules = sorted(os.listdir(modules_file))
            names_modules = []
            for name in self.type_pv_modules:
                names_modules.append(name[:-4])
            self.listPV_file.addItems(names_modules)
        return names_modules
            
    def select_other(self):
        self.listKTP_file.clear()
        if self.listKTP_folder.currentText() != "Выберите":
            self.select_title_ktp = self.listKTP_folder.currentText() 
            modules_file = f'{path_to_ktp}/{self.select_title_ktp}'
            self.type_other_modules = sorted(os.listdir(modules_file))
            names_modules = []
            for name in self.type_other_modules:
                names_modules.append(name[:-4])
            self.listKTP_file.addItems(names_modules)

    def load_invertor(self):
        current_invertor = self.listInvertor_file.currentText()
        for select_invertor in self.type_modules:
            if current_invertor in select_invertor: 
                extension = select_invertor[-4:]
                self.invertors[f'found_invertor_{self.spinBox_numInvertor.value() - 1}'] = search_data.search_in_invertor(f"{path_to_invertors}/{self.select_title_invertor}/{current_invertor + extension}") 
                current = self.invertors[f'found_invertor_{self.spinBox_numInvertor.value() - 1}']
                if current['broken_file'] == True:
                    self.statusBar.showMessage('Битый файл, данные не загружены', 4000)
                    self.statusBar.setStyleSheet(styles_responce.status_yellow)
                    QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))
                else:
                    self.statusBar.showMessage('', 100)
                    self.statusBar.showMessage(styles_responce.status_ok, 2000)
                    self.statusBar.setStyleSheet(styles_responce.status_white)

                current['file'] = self.listInvertor_file.currentIndex()
                current['folder'] = self.listInvertor_folder.currentIndex()
                current['type_inv'] = 'Инвертор'
                current['title_grid_line'] = 'ВБШвнг(A)-LS 4x95'
                current['title_grid_line_length'] = '180 м'
                current['title_grid_top'] = 'ЩР 0.4 кВ (ВИЭ)'
                current['title_grid_switch'] = 'QF1 3P 160A'
                current['use_5or4_line'] = False
                current['count_invertor'] = 1 #количество инверторов
                current['diff_mppt'] = False #количество инверторов
                for num in range(int(current['count_invertor'])):
                    current[f'local_{num}'] = {'controller': False, 'commutator': False, 'left_yzip': False, 
                                                'right_yzip': False, 'title_other_device': 'УЗИП'}

                current['type_inv'] = 'Инвертор'
                current['i_nom_inv'] = 'C160'
                current['brand_cable_inv'] = 'ВБШвнг(А)-LS 4x95'
                current['length_cable_inv'] = '180 м*'
                if current['phase'] == 3:
                    current['yellow_line_inv'] = True
                    current['red_line_inv'] = True 
                    current['blue_line_inv'] = True
                    current['green_line_inv'] = True
                    current['black_line_inv'] = True
                    current['yellow_switch_inv'] = True
                    current['red_switch_inv'] = True
                    current['blue_switch_inv'] = True
                    current['green_switch_inv'] = True
                else:
                    current['red_line_inv'] = False
                    current['green_line_inv'] = False
                    current['red_switch_inv'] = False
                    current['green_switch_inv'] = False
                    current['yellow_line_inv'] = True
                    current['blue_line_inv'] = True
                    current['black_line_inv'] = True
                    current['yellow_switch_inv'] = True
                    current['blue_switch_inv'] = True

                self.w3.up_down_invertor_selection()
                self.w4.up_down_invertor_selection()
                self.w6.up_down_invertor_selection()
                return current

    def load_pv(self):
        current_pv = self.listPV_file.currentText()
        for select_pv in self.type_pv_modules:
            if current_pv in select_pv:
                extension = select_pv[-4:] 
                self.pvs[f'found_pv_{self.spinBox_numPV.value() - 1}'] = search_data.search_in_pv(f"{path_to_pv}/{self.select_title_pv}/{current_pv + extension}") 
                current = self.pvs[f'found_pv_{self.spinBox_numPV.value() - 1}']
                current['file'] = self.listPV_file.currentIndex()
                current['folder'] = self.listPV_folder.currentIndex()
                self.statusBar.showMessage(styles_responce.status_ok, 2000)

    def load_other(self):
        current_other = self.listKTP_file.currentText()
        for select_other in self.type_other_modules:
            if current_other in select_other:
                extension = select_other[-4:]  
                current = self.others[f'found_other_{self.spinBox_numKTP.value() - 1}']
                current['table_data'] = search_data.search_in_others_device(f"{path_to_ktp}/{self.select_title_ktp}/{current_other + extension}") 
                current['file'] = self.listKTP_file.currentIndex()
                current['folder'] = self.listKTP_folder.currentIndex()
                key_title = 'nil'
                key_type = 'nil'
                key_power = 'nil'
                key_i = 'nil'
                for key in current['table_data'].keys():
                    if 'тип оборудования' in key.lower(): key_type = key
                    elif 'название оборудования' in key.lower(): key_title = key
                    elif 'мощность' in key.lower(): key_power = key
                    elif 'сила тока' in key.lower(): key_i = key

                current['title_other'] = current['table_data'].get(key_title, 'Н/Д')
                current['type_other'] = current['table_data'].get(key_type, 'Н/Д')
                current['power_other'] = current['table_data'].get(key_power, 'Н/Д')
                current['i_other'] = current['table_data'].get(key_i, 'Н/Д')
                current['count_other'] = 1

                current['type_param_other'] = 'QF'
                current['i_nom_other'] = 'C160'
                current['brand_cable_other'] = 'ВБШвнг(А)-LS 4x95'
                current['length_cable_other'] = '180 м*'
                current['red_line_other'] = False
                current['green_line_other'] = False
                current['red_switch_other'] = False
                current['green_switch_other'] = False
                current['yellow_line_other'] = True
                current['blue_line_other'] = True
                current['black_line_other'] = True
                current['yellow_switch_other'] = True
                current['blue_switch_other'] = True
                self.w4.up_down_other_device_selection()
                self.statusBar.showMessage(styles_responce.status_ok, 2000)
                print(current)

    def load_pvsyst(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', path_to_pdf_pvsyst, "*.pdf")[0] #открытие диалога для выбора файла
        print(path)
        self.hide_del_button_device()
        if len(path) != 0:
            self.path_pvsyst = path
            print(self.path_pvsyst)
            if self.del_pdf('pvsyst') == 1: return
            self.textConsole.append("- Загружен отчет PVsyst")
            self.btnOne.setEnabled(False)
            self.startAnimation()
            self.converter_pvsyst = СonvertFiles(self.path_pvsyst, 'pvsyst')
            self.converter_pvsyst.finished.connect(self.convertPvsystFinished)
            self.converter_pvsyst.start()

    def load_scheme_one(self):
        self.pathes_detail_schemes = QtWidgets.QFileDialog.getOpenFileNames(self, 'Выберите файлы схем инверторa', 
                                                                            path_to_schemes + '/Invertor', "*.svg")[0]
        print(self.pathes_detail_schemes)
        self.hide_del_button_schemes()
        if len(self.pathes_detail_schemes) != 0:
            if self.del_pdf('detailed') == 1: return
            self.textConsole.append("- Загружена принципиальная эл.схема")
            self.btnLoadScheme1.setEnabled(False)
            self.converter1 = СonvertFiles(self.pathes_detail_schemes, 'detailed')
            self.converter1.finished.connect(self.convertOneFinished)
            self.converter1.start()
        
    def load_scheme_two(self):
        self.path_general_schemes = [QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл схемы станции', 
                                                                            path_to_schemes + '/General', "*.svg")[0]]
        print( self.path_general_schemes)
        self.hide_del_button_schemes()
        if len(self.path_general_schemes[0]) != 0:
            if self.del_pdf('general') == 1: return
            self.textConsole.append("- Загружена принципиальная эл.схема ")
            self.btnLoadScheme2.setEnabled(False)
            self.converter2 = СonvertFiles(self.path_general_schemes, 'general')
            self.converter2.finished.connect(self.convertTwoFinished)
            self.converter2.start()

    def load_structural_scheme(self):
        self.path_structural_schemes = [QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл структурной схемы', 
                                                                            path_to_schemes + '/Structural', "*.svg")[0]]
        print(self.path_structural_schemes)
        self.hide_del_button_schemes()

        if len(self.path_structural_schemes[0]) != 0:
            if self.del_pdf('structural') == 1: return
            self.textConsole.append("- Загружена структурная эл.схема ")
            self.btnLoadStructScheme.setEnabled(False)
            self.converter3 = СonvertFiles(self.path_structural_schemes, 'structural')
            self.converter3.finished.connect(self.convertStructFinished)
            self.converter3.start()

    def load_plane_set_scheme(self):
        self.path_plane_set_schemes = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл плана размещения', 
                                                                            'Data/PDF in/', "*.pdf")[0]
        print(self.path_plane_set_schemes)
        self.hide_del_button_schemes()
        if self.path_plane_set_schemes != '':
            self.textConsole.append("- Загружен план размещения ")

    def add_invertor(self):
        current_load = f'found_invertor_{self.spinBox_numInvertor.value() - 1}'
        if self.listInvertor_file.currentText() != "" and self.invertors[current_load]['module'] != 'Н/Д':
            self.spinBox_numInvertor.show()
            self.btnDelInvertor.show() 
            self.listInvertor_file.clear()
            self.listInvertor_folder.setCurrentIndex(0)
            self.invertors[f'found_invertor_{len(self.invertors)}'] = search_data.null_search_params('invertor')
            self.spinBox_numInvertor.setMinimum(1)
            self.spinBox_numInvertor.setMaximum(len(self.invertors))
            self.spinBox_numInvertor.setValue(len(self.invertors))

    def add_pv(self):
        current_load = f'found_pv_{self.spinBox_numPV.value() - 1}'
        if self.listPV_folder.currentText() != "Выберите" and self.pvs[current_load]['module_pv'] != 'Н/Д':
            self.spinBox_numPV.show()
            self.btnDelPV.show() 
            self.listPV_file.clear()
            self.listPV_folder.setCurrentIndex(0)
            self.pvs[f'found_pv_{len(self.pvs)}'] = search_data.null_search_params('pv')
            self.spinBox_numPV.setMinimum(1)
            self.spinBox_numPV.setMaximum(len(self.pvs))
            self.spinBox_numPV.setValue(len(self.pvs))

    def add_other(self):
        current_load = f'found_other_{self.spinBox_numKTP.value() - 1}'
        if self.listKTP_folder.currentText() != "Выберите" and len(self.others[current_load]) != 0 :
            self.spinBox_numKTP.show()
            self.btnDelOther.show() 
            self.listKTP_file.clear()
            self.listKTP_folder.setCurrentIndex(0)
            self.others[f'found_other_{len(self.others)}'] = {}
            self.spinBox_numKTP.setMinimum(1)
            self.spinBox_numKTP.setMaximum(len(self.others))
            self.spinBox_numKTP.setValue(len(self.others)) 

    def del_invertor(self):
        if len(self.invertors) > 1:
            del self.invertors[f'found_invertor_{self.spinBox_numInvertor.value() - 1}']
            self.spinBox_numInvertor.setMaximum(len(self.invertors))
            self.spinBox_numInvertor.setValue(len(self.invertors))
            index = 0
            for key in list(self.invertors.keys()):
                self.invertors[f'found_invertor_{index}'] = self.invertors.pop(key)
                index += 1
            self.up_down_invertor_selection()
            self.w3.up_down_invertor_selection()
            self.w4.up_down_invertor_selection()
            self.w6.up_down_invertor_selection()
        if len(self.invertors) == 1:
            self.btnDelInvertor.hide()
            self.spinBox_numInvertor.hide()

    def del_pv(self):
        if len(self.pvs) > 1:
            del self.pvs[f'found_pv_{self.spinBox_numPV.value() - 1}']
            self.spinBox_numPV.setMaximum(len(self.pvs))
            self.spinBox_numPV.setValue(len(self.pvs))
            index = 0
            for key in list(self.pvs.keys()):
                self.pvs[f'found_pv_{index}'] = self.pvs.pop(key)
                index += 1
            self.up_down_pv_selection()
        if len(self.pvs) == 1:
            self.btnDelPV.hide()
            self.spinBox_numPV.hide()

    def del_other(self):
        if len(self.others) > 1:
            del self.others[f'found_other_{self.spinBox_numKTP.value() - 1}']
            self.spinBox_numKTP.setMaximum(len(self.others))
            self.spinBox_numKTP.setValue(len(self.others))
            index = 0
            for key in list(self.others.keys()):
                self.others[f'found_other_{index}'] = self.others.pop(key)
                index += 1
            self.up_down_other_selection()
            self.w4.up_down_other_device_selection()
        if len(self.others) == 1:
            self.btnDelOther.hide()
            self.spinBox_numKTP.hide()

    def del_pdf(self, method):
        fp_structural = path_to_pdf_schemes + "/Structural"
        fp_general = path_to_pdf_schemes + "/General"
        fp_detailed = path_to_pdf_schemes + "/Detailed"
        patch_imgs_pvsyst = "Data/Images/PVsyst"
        img_files_pvsyst = [f for f in os.listdir(patch_imgs_pvsyst) if os.path.isfile(os.path.join(patch_imgs_pvsyst, f))]
        files_in_structural = [f for f in os.listdir(fp_structural) if isfile(join(fp_structural, f))]
        files_in_general = [f for f in os.listdir(fp_general) if isfile(join(fp_general, f))]
        files_in_detailed = [f for f in os.listdir(fp_detailed) if isfile(join(fp_detailed, f))]
        
        try:
            if len(files_in_general) != 0 and method == 'general':
                os.remove(fp_general + f"/{files_in_general[0]}")
            if len(files_in_structural) != 0 and method == 'structural':
                os.remove(fp_structural + f"/{files_in_structural[0]}")
            if len(files_in_detailed ) != 0 and method == 'detailed':
                for file in files_in_detailed:
                    os.remove(fp_detailed + f"/{file}")   
            if len(img_files_pvsyst) != 0 and method == 'pvsyst':
                for file in img_files_pvsyst:
                    os.remove(patch_imgs_pvsyst + f"/{file}")  
        except PermissionError:
            self.statusBar.showMessage('Открыт pdf файл, закройте его и повторите попытку', 4000)
            self.statusBar.setStyleSheet(styles_responce.status_red)
            QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))
            return 1

    def del_pvsyst(self):
        if self.del_pdf('pvsyst') == 1:
            return
        self.found_pdf = search_data.null_search_params('pvsyst')
        self.path_pvsyst = ''
        self.hide_del_button_device()
        self.statusBar.showMessage('Файл PVsyst исключен из отчета', 2500)
        self.statusBar.setStyleSheet(styles_responce.status_info)
        QTimer.singleShot(2500, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))

    def del_scheme_one(self):
        if self.del_pdf('detailed') == 1: return
        self.hide_del_button_schemes()
        self.statusBar.showMessage('Файл первого чертежа исключен из отчета', 2500)
        self.statusBar.setStyleSheet(styles_responce.status_info)
        QTimer.singleShot(2500, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))

    def del_scheme_two(self):
        if self.del_pdf('general') == 1: return
        self.hide_del_button_schemes()
        self.statusBar.showMessage('Файл второго чертежа исключен из отчета', 2500)
        self.statusBar.setStyleSheet(styles_responce.status_info)
        QTimer.singleShot(2500, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))

    def del_structural_scheme(self):
        if self.del_pdf('structural') == 1: return
        self.hide_del_button_schemes()
        self.statusBar.showMessage('Файл структурной схемы исключен из отчета', 2500)
        self.statusBar.setStyleSheet(styles_responce.status_info)
        QTimer.singleShot(2500, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))

    def del_plane_set(self):
        self.path_plane_set_schemes = ''
        self.hide_del_button_schemes()
        self.statusBar.showMessage('Файл плана размещения исключен из отчета', 2500)
        self.statusBar.setStyleSheet(styles_responce.status_info)
        QTimer.singleShot(2500, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))
  
    def up_down_invertor_selection(self):
        current = self.invertors[f'found_invertor_{self.spinBox_numInvertor.value() - 1}']
        if 'folder' in current:
            self.listInvertor_folder.setCurrentIndex(current['folder'])
            self.select_invertor()
            if 'file' in current:
                self.listInvertor_file.setCurrentIndex(current['file'])
            else:
                self.listInvertor_file.clear()
        else:
            self.listInvertor_folder.setCurrentIndex(0)
            self.listInvertor_file.clear()

    def up_down_pv_selection(self):
        current = self.pvs[f'found_pv_{self.spinBox_numPV.value() - 1}']
        if 'folder' in current:
            self.listPV_folder.setCurrentIndex(current['folder'])
            self.select_pv()
            if 'file' in current:
                self.listPV_file.setCurrentIndex(current['file'])
            else:
                self.listPV_file.clear()
        else:
            self.listPV_folder.setCurrentIndex(0)
            self.listPV_file.clear()

    def up_down_other_selection(self):
        current = self.others[f'found_other_{self.spinBox_numKTP.value() - 1}']
        if 'folder' in current:
            self.listKTP_folder.setCurrentIndex(current['folder'])
            self.select_other()
            if 'file' in current:
                self.listKTP_file.setCurrentIndex(current['file'])
            else:
                self.listKTP_file.clear()
        else:
            self.listKTP_folder.setCurrentIndex(0)
            self.listKTP_file.clear()
      
    def merge_pdf(self):
        pdf_merger = PdfFileMerger()
        fp_structural = path_to_pdf_schemes + "/Structural"
        fp_general = path_to_pdf_schemes + "/General"
        fp_detailed = path_to_pdf_schemes + "/Detailed"
        files_in_structural = [f for f in os.listdir(fp_structural) if isfile(join(fp_structural, f))]
        files_in_general = [f for f in os.listdir(fp_general) if isfile(join(fp_general, f))]
        files_in_detailed = [f for f in os.listdir(fp_detailed) if isfile(join(fp_detailed, f))]

        with open("Data/Report/Report.pdf", 'rb') as report: 
            pdf_merger.append(report)
        if len(files_in_structural) != 0 and self.path_structural_schemes != " ":
            with open(fp_structural + f"/{files_in_structural[0]}", 'rb') as image_fd: 
                pdf_merger.append(image_fd)
        if len(files_in_general) != 0 and self.path_general_schemes != " ":
            with open(fp_general + f"/{files_in_general[0]}", 'rb') as image_fd: 
                pdf_merger.append(image_fd)
        if len(files_in_detailed ) != 0 and self.pathes_detail_schemes != " ":
            for i in range(len(files_in_detailed)):
                with open(fp_detailed + f"/{files_in_detailed[i]}", 'rb') as image_fd: 
                    pdf_merger.append(image_fd)
        if self.path_plane_set_schemes != '':
            with open(self.path_plane_set_schemes, 'rb') as image_fd: 
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
        if hasattr(self.w2, 'parse_params'):
            self.weather = self.w2.parse_params
            self.weather['climate_info'] = self.w2.textConsoleClimat.toPlainText()
        else:
            self.weather = self.parse_params

        self.calcPV = self.w5.stc_noct if hasattr(self.w5, 'temperature') else {} 

        self.weather_station = self.w2.parse_params_current_city if hasattr(self.w2, 'parse_params_current_city') else self.weather_station_params
        
    def create_document(self):
        try:
            with open("Data/Report/Report.pdf", 'w') as fp:
                pass
            with open("Data/Report/Auto-OTR.pdf", 'w') as fp:
                pass
        except PermissionError:
            self.statusBar.showMessage('Открыт pdf файл отчета, закройте его и повторите попытку', 4000)
            self.statusBar.setStyleSheet(styles_responce.status_red)
            QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))
            return

        if self.validation() == 0:
            return
        else:
            self.btnOpenPDF.hide()
            self.label_10.show()
            self.label_10.setText('Создание...')
            self.startAnimation()
            QtWidgets.QApplication.processEvents()
            self.out_params()
            
            main_params = {'path_to_pvsyst': self.path_pvsyst, 'roof': self.current_roof, 'invertors': self.invertors,
                            **self.blocks, **self.object_passport, 'pvs': self.pvs, 'others': self.others,
                            **self.weather, **self.weather_station, **self.found_pdf, 'calcPV': self.calcPV}
            print(main_params)
            
            self.btnForm.setEnabled(False)
            self.statusBar.showMessage('Пожалуйста, подождите...')
            self.statusBar.setStyleSheet(styles_responce.status_yellow)
            self.builder = BuildDoc(main_params)
            self.builder.finished.connect(self.buildFinished)
            self.builder.start()

    def showParserFinished(self):
        self.browser_status = self.parser_open.browser_status
        if self.browser_status == 0:
            self.w2.setWindowIcon(QtGui.QIcon('Data/icons/graficon.png'))
            self.w2.show()
            self.w2.setFixedSize(915, 430)
            self.statusBar.showMessage('Успешно!', 4000)
            self.statusBar.setStyleSheet(styles_responce.status_green)
        elif self.browser_status == 1:
            self.statusBar.showMessage('Удаленный хост принудительно разорвал существующее подключение', 4000)
            self.statusBar.setStyleSheet(styles_responce.status_red)
        elif self.browser_status == 2:
            self.statusBar.showMessage('Слабое или нестабильное интеренет подключение', 4000)
            self.statusBar.setStyleSheet(styles_responce.status_red)
        else:
            self.statusBar.showMessage('Что-то пошло не так, попробуйте запустить снова', 4000)
            self.statusBar.setStyleSheet(styles_responce.status_red)
        QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))
        self.btnRP5.setEnabled(True)
        self.stopAnimation()
        del self.parser_open

    def closeFinished(self):
        del self.parser_close 

    def convertOneFinished(self):
        self.btnLoadScheme1.setEnabled(True)
        self.hide_del_button_schemes()
        del self.converter1
        
    def convertTwoFinished(self):
        self.btnLoadScheme2.setEnabled(True)
        self.hide_del_button_schemes()
        del self.converter2

    def convertStructFinished(self):
        self.btnLoadStructScheme.setEnabled(True)
        self.hide_del_button_schemes()
        del self.converter3

    def convertPvsystFinished(self):
        self.found_pdf = self.converter_pvsyst.found_pdf 
        self.inputAddressLat.setText(self.found_pdf['lati_pdf'])
        self.inputAddressLong.setText(self.found_pdf['longi_pdf'])

        if self.internet_on() == True and hasattr(self.converter_pvsyst, 'full_address'):
            full_address = self.converter_pvsyst.full_address
            self.inputAddress.setText(full_address['full_address'])
            self.w2.inputCity.setText(full_address['city_point'])
        
        array_pv = self.found_pdf['found_pv_invertor']['pv_array_config_0']
        if isinstance(array_pv, str):
            self.statusBar.showMessage(array_pv, 4000)
            self.statusBar.setStyleSheet(styles_responce.status_yellow)
            QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))
        else:
            self.set_draw_params()
            self.statusBar.showMessage('Параметры схем сконфигурированы, проверьте данные и постройте', 4000)
            self.statusBar.setStyleSheet(styles_responce.status_green)
            QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))
        self.btnOne.setEnabled(True)
        self.hide_del_button_device()
        self.stopAnimation()
        del self.converter_pvsyst

    def set_draw_params(self):
        print('конфигурация фэм массивов: ', self.found_pdf['found_pv_invertor'])
        
        while len(self.invertors) > 1:
            self.del_invertor()

        while len(self.pvs) > 1:    
            self.del_pv()

        count_diff_inv = len(self.found_pdf['found_pv_invertor']) - 2

        for num in range(count_diff_inv):
            found_inv_company = False
            found_pv_company = False
            found_inv = False
            found_pv = False
            
            pvsyst_pvs_invrtrs = self.found_pdf['found_pv_invertor'][f'pv_array_config_{num}']

            for company in self.company_invertor:
                if pvsyst_pvs_invrtrs['title_invertor'].lower() in company.lower() or company.lower() in pvsyst_pvs_invrtrs['title_invertor'].lower():
                    self.listInvertor_folder.setCurrentText(company)
                    names_invrtrs = self.select_invertor()
                    found_inv_company = True

                    for model in names_invrtrs:
                        if pvsyst_pvs_invrtrs['model_invertor'].lower() in model.lower() or model.lower() in pvsyst_pvs_invrtrs['model_invertor'].lower():
                            self.listInvertor_file.setCurrentText(model)
                            found_inv = True

                    config_keys = []    
                    for key in pvsyst_pvs_invrtrs.keys():
                        if 'config' in key:
                            config_keys.append(key)

                    if found_inv == True:
                        current_invertor = self.load_invertor()
                        count_invertors = 0
                        diff_mppt = False
                        for config in config_keys:
                            current_invertor[config] = pvsyst_pvs_invrtrs[config]

                            count_invertor = current_invertor[config]['count_invertor']
                            if '.' in count_invertor:
                                diff_mppt = True
                                count_invertors += float(count_invertor)
                                del current_invertor[config]['count_invertor']
                            else:
                                diff_mppt = False
                                count_invertors = int(count_invertor)
                                current_invertor[config]['count_mppt'] = int(current_invertor[config]['count_mppt']) // count_invertors
                                current_invertor[config]['count_string'] = int(current_invertor[config]['count_string']) // count_invertors
                                del current_invertor[config]['count_invertor']

                            max_chain = int(current_invertor[config]['count_mppt']) * int(current_invertor['inputs'])
                            max_chain_y = max_chain * 2
                            count_strings = int(current_invertor[config]['count_string'])
                            if count_strings > max_chain and count_strings <= max_chain_y:
                                current_invertor[config]['use_y_connector'] = True
                            else:
                                current_invertor[config]['use_y_connector'] = False
                            current_invertor[config]['use_all_mppt'] = False

                        current_invertor['count_invertor'] = int(count_invertors)
                        for num in range(current_invertor['count_invertor']):
                            current_invertor[f'local_{num}'] = {'controller': False, 'commutator': False, 'left_yzip': False,
                                                                'right_yzip': False, 'title_other_device': 'УЗИП'}
                        current_invertor['diff_mppt'] = diff_mppt
                        print('После добавки', current_invertor)
                        self.w3.up_down_invertor_selection()
                        self.w4.up_down_invertor_selection()
                        self.w6.up_down_invertor_selection()
                    else:
                        self.del_invertor()
                        self.textConsole.append(f"Инвертор {pvsyst_pvs_invrtrs['model_invertor']} не найден")
                        self.textConsole.append(f'Его параметры:')
                        for config in config_keys:
                            self.textConsole.append(f'{pvsyst_pvs_invrtrs[config]}')

            if found_inv_company == False:
                self.textConsole.append(f"Инверторная компания {pvsyst_pvs_invrtrs['title_invertor']} не найдена")

            for company in self.company_pv:
                if pvsyst_pvs_invrtrs['title_pv'].lower() in company.lower() or company.lower() in pvsyst_pvs_invrtrs['title_pv'].lower():
                    self.listPV_folder.setCurrentText(company)
                    names_pv = self.select_pv()
                    found_pv_company = True
            
                    for model in names_pv:
                        if pvsyst_pvs_invrtrs['model_pv'].lower() in model.lower() or model.lower() in pvsyst_pvs_invrtrs['model_pv'].lower():
                            self.listPV_file.setCurrentText(model)
                            found_pv = True

                    if found_pv == True:
                        self.load_pv()
                    else:
                        self.textConsole.append(f"ФЭМ {pvsyst_pvs_invrtrs['model_pv']} не найден")

            if found_pv_company == False:
                self.textConsole.append(f"Компания ФЭМ {pvsyst_pvs_invrtrs['title_pv']} не найдена")

            if count_diff_inv > 1 and num < count_diff_inv - 1 :
                self.add_invertor()
                self.add_pv()
        print(self.invertors)
        print(self.pvs)

    def buildFinished(self):
        self.textConsole.append("Отчет сформирован!")
        self.statusBar.showMessage('Отчет сформирован!', 4000)
        self.statusBar.setStyleSheet(styles_responce.status_green)
        QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))
        self.merge_pdf()
        self.stopAnimation()
        self.btnOpenPDF.show()
        self.label_10.setText('Создать')
        self.btnForm.setEnabled(True)
        del self.builder

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainApp()  # Создаём объект класса ExampleApp
    window.setWindowIcon(QtGui.QIcon('Data/icons/graficon.png'))
    window.show()  # Показываем окно
    window.setFixedSize(1075, 525)
    window.instance_ofter_class(window)
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':
    main()

