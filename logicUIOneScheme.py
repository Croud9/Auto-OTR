import draw_schemes
import designDrawSchemes
from PyQt5 import QtWidgets
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QThread, QRegExp, QTimer

class DrawOne(QThread):
    def __init__(self, params, parametrs, count_invertor, gost_frame_params):
        super().__init__()
        self.params = params
        self.parametrs = parametrs
        self.count_invertor = count_invertor
        self.gost_frame_params = gost_frame_params
        self.modules = 0
        self.chains = 0

    def run(self):
        for num in range(self.count_invertor):
            num += 1
            main_params = self.params.copy()
            self.num_error = draw_schemes.draw(main_params, self.parametrs, num, self.gost_frame_params)
            self.modules += self.num_error[2]
            self.chains += self.num_error[1]
  
class WindowDraw(QtWidgets.QMainWindow, designDrawSchemes.Ui_WindowDrawSchemes):
    def __init__(self, instance_of_main_window):
        super().__init__()
        self.setupUi(self)
        self.validate()
        self.main_window = instance_of_main_window
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
        false_value = ['Н/Д', '']
        # creating a opacity effect
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.6)
        use_all_mppt = True if self.checkUse_all_mppt.isChecked() else False
        use_y_connector = True if self.checkUse_y_connector.isChecked() else False   
            
        if not self.inputCount_mppt.text() in false_value and not self.inputCount_input_mppt.text() in false_value:
            count_input_mppt = int(self.inputCount_input_mppt.text())
            self.count_mppt = int(self.inputCount_mppt.text())   
            self.textConsoleCurrent.clear()         
            max_input = count_input_mppt * self.count_mppt
            max_input_y = count_input_mppt * self.count_mppt * 2
            self.textConsoleCurrent.append(f"Макс. кол-во входов без Y коннектора: {max_input}")
            self.textConsoleCurrent.append(f"Макс. кол-во входов c Y коннектором: {max_input_y}")
            
            if not self.inputAll_chain.text() in false_value:
                self.all_chain = int(self.inputAll_chain.text())
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
        else:
            self.textConsoleCurrent.clear() 
            
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

        if not save_input_params:
            self.textConsoleDraw.append("Введите заново параметры разных MPPT")
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            return

        self.textConsoleDraw.append(f"Номер инвертора: {count_invertor}")
        if self.checkUse_CloneInvertor.isChecked() != 0:
            self.input_params = save_input_params.copy()
        
        self.btnDraw.setEnabled(False)
        self.btnDraw.setText('Построение чертежа...')
        self.statusBar.showMessage('Пожалуйста, подождите...')
        self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
        
        title_project = self.main_window.inputTitleProject.text()
        code_project = self.main_window.inputCodeProject.text()            
        gost_frame_params = {'title_project': title_project, 'code_project': code_project} 
        self.painter_draw_one = DrawOne(self.input_params, parametrs, count_invertor, gost_frame_params)

        self.painter_draw_one.finished.connect(self.drawFinished)
        self.painter_draw_one.start()

    def drawFinished(self):
        if self.painter_draw_one.num_error[0] == 0:
            self.textConsoleDraw.append("----------------------------")
            self.textConsoleDraw.append("РЕЗУЛЬТАТЫ:")
            self.textConsoleDraw.append(f" Всего цепочек: {self.painter_draw_one.chains}")
            self.textConsoleDraw.append(f" Всего модулей: {self.painter_draw_one.modules}")
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
 
 