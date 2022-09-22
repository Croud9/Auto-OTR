import designParsing
import parsingSelenium
import requests, os 
from datetime import date
from os.path import isfile, join
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QThread
# import wikipedia
# wikipedia.set_lang("ru") 
# print(wikipedia.page("Оренбург").content)
path_to_pdf_schemes = "Data/PDF in/Shemes"

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
             
    def checkNet(self):
        try:
            response = requests.get("http://www.google.com")
            # print("response code: ", response.status_code)
            self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)")
            return 1
        except requests.ConnectionError:
            self.statusBar.showMessage('Нет подключения к интернету', 10000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            print("Could not connect")
            return 0
   
    def opacity(self, button, enabled):
        count_opacity = 0.6 if enabled == False else 1
        opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        opacity_effect.setOpacity(count_opacity)
        button.setGraphicsEffect(opacity_effect)
        button.setEnabled(enabled)

    def check_inCity(self):
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
            return 0
        elif len(c) == 1:
            self.statusBar.showMessage('Слишком короткий запрос!', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.opacity(self.btnDwnld_T, True)
            self.opacity(self.btnParse, True)
            self.btnSearch.setEnabled(True)
            self.btnParse.setText('Скачать архив')
            self.btnDwnld_T.setText('Подгрузить температуру')
            self.btnSearch.setText('Найти')
            return 0
        elif internet == 0:
            return 0
        else:
            # self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)")
            return 1

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
        # QtWidgets.QApplication.processEvents()

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
        self.opacity(self.btnDwnld_T, False)
        self.btnDwnld_T.setText('Подгрузка...')
        QtWidgets.QApplication.processEvents()

        check = self.parsing_date_load(2)
        if check == 0 or check == 1 :
            return

        self.textConsole.append("...")
        self.textConsole.append("Выполняется подгрузка...")
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
        del self.parser_close

