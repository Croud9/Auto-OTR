from itertools import count
import draw_schemes
import designDrawSchemes
import search_data
from PyQt5 import QtWidgets
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QThread, QRegExp, QTimer

class DrawOne(QThread):
    def __init__(self, draw_params, gost_frame_params):
        super().__init__()
        self.draw_params = draw_params
        self.count_invertor = self.draw_params['count_invertor']
        self.gost_frame_params = gost_frame_params
        self.modules = 0
        self.chains = 0

    def run(self):
        for num in range(self.count_invertor):
            num += 1
            self.num_error = draw_schemes.draw(self.draw_params, num, self.gost_frame_params)
            if self.num_error['error'] != 0: return 
            self.modules += self.num_error['modules']
            self.chains += self.num_error['chains']
  
class WindowDraw(QtWidgets.QMainWindow, designDrawSchemes.Ui_WindowDrawSchemes):
    def __init__(self, instance_of_main_window):
        super().__init__()
        self.setupUi(self)
        self.validate()
        self.spinBox_numInvertor.setMinimum(1)
        self.spinBox_numDifferentMPPT.setMinimum(1)
        self.spinBox_numDifferentMPPT.hide()
        self.spinBox_CloneInvertor.setMinimum(1)
        self.btnAdd_new_mppt.hide()
        self.main_window = instance_of_main_window
        self.btnDraw.clicked.connect(self.draw)
        self.btnAdd_new_mppt.clicked.connect(self.add_mppt)
        self.btnUpdateConsole.clicked.connect(self.update_console)
        self.checkUse_different_mppt.stateChanged.connect(self.show_and_hide_different_mppt)
        self.checkUse_three_phase.stateChanged.connect(self.show_and_hide_color_line_because_phase)
        self.checkUse_5or4_line.clicked.connect(self.show_and_hide_color_line_because_phase)
        self.inputCount_mppt.textChanged.connect(self.validate_input)
        self.inputCount_input_mppt.textChanged.connect(self.validate_input)
        self.inputAll_chain.textChanged.connect(self.validate_input)
        self.checkUse_y_connector.stateChanged.connect(self.validate_input)
        self.checkUse_all_mppt.stateChanged.connect(self.validate_input)
        self.btnReset.clicked.connect(self.reset)
        self.spinBox_numInvertor.valueChanged.connect(self.up_down_invertor_selection)
        self.spinBox_numDifferentMPPT.valueChanged.connect(self.spin_diff_mppt)
        self.btnSaveConfig.clicked.connect(self.save_config)
        self.styles()
        self.draw_params = {}

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
        self.textConsoleDraw.clear()
        self.textConsoleCurrent.clear()
        self.btnAdd_new_mppt.hide()

    def invertor_and_config_keys(self):
        invertors = self.main_window.invertors
        self.spinBox_numInvertor.setMaximum(len(invertors))

        spinbox_val = self.spinBox_numInvertor.value() - 1
        invertor = invertors[f'found_invertor_{spinbox_val}']

        config_keys = []    
        for key in invertor.keys():
            if 'config' in key:
                config_keys.append(key)
        return invertor, config_keys    

    def up_down_invertor_selection(self):
        invertor = self.invertor_and_config_keys()[0]
        config_keys = self.invertor_and_config_keys()[1]

        self.inputName_invertor.setText(f'{invertor["module"]}')
        self.inputCount_mppt.setText(f'{invertor["mppt"]}')
        self.inputCount_input_mppt.setText(f'{invertor["inputs"]}')
        self.spinBox_CloneInvertor.setValue(int(invertor['count_invertor']))
        if invertor['phase'] == 3:
            self.checkUse_three_phase.setCheckState(2)
        elif invertor['phase'] == 1:
            self.checkUse_three_phase.setCheckState(0)
        self.inputNumber_invertor.setText(f"{invertor['type_inv']}")
        self.inputTitle_grid_line.setText(f"{invertor['title_grid_line']}")
        self.inputTitle_grid_line_length.setText(f"{invertor['title_grid_line_length']}")
        self.inputTitle_grid_top.setText(f"{invertor['title_grid_top']}")
        self.inputTitle_grid_switch.setText(f"{invertor['title_grid_switch']}")
        self.checkUse_5or4_line.setCheckState(2 if invertor['use_5or4_line'] == True else 0)        

        if invertor['diff_mppt'] == True:
            self.checkUse_different_mppt.setCheckState(2) # разные mppt
            self.spin_diff_mppt()
        else:
            for config in config_keys:
                self.inputSolar_count_on_the_chain.setText(str(invertor[config]['count_pv']))
                self.inputCount_mppt.setText(str(invertor[config]['count_mppt']))
                self.inputAll_chain.setText(str(invertor[config]['count_string']))
            if not config_keys:
                self.inputSolar_count_on_the_chain.setText(str(0))
                self.inputCount_mppt.setText(str(invertor['mppt']))
                self.inputAll_chain.setText(str(0))
            self.spinBox_numDifferentMPPT.hide()
            self.checkUse_different_mppt.setCheckState(0)

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
            max_input_y = max_input * 2
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
                    return 0
        else:
            self.textConsoleCurrent.clear() 
            
    def check_imput_params(self):
        self.parametrs()
        if self.count_mppt == '':
            self.statusBar.showMessage('Введите количество MPPT', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputCount_mppt.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            return 1
        elif self.input_mppt == '':
            self.statusBar.showMessage('Введите число входов на МРРТ', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputCount_input_mppt.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            return 1
        elif self.count_fem == '':
            self.statusBar.showMessage('Введите количество ФЭМ в цепочке', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputSolar_count_on_the_chain.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            return 1
        elif self.all_chain == '':
            self.statusBar.showMessage('Введите общее количество цепочек', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputAll_chain.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            return 1
        else:
            self.set_style_default()
            return 0

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

    def set_style_default(self):
        self.inputCount_mppt.setStyleSheet(self.default_style_input)
        self.inputCount_input_mppt.setStyleSheet(self.default_style_input)
        self.inputSolar_count_on_the_chain.setStyleSheet(self.default_style_input)
        self.inputAll_chain.setStyleSheet(self.default_style_input)

        self.statusBar.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.statusBar.showMessage('', 100)

    def show_and_hide_different_mppt(self):
        if self.checkUse_different_mppt.isChecked():
            self.btnAdd_new_mppt.show()
        else:
            self.btnAdd_new_mppt.hide()

    def update_console(self):
        self.textConsoleDraw.clear()

    def save_config(self):
        if self.check_imput_params() != 0:
            return 1

        invertor = self.invertor_and_config_keys()[0]
        config_keys = self.invertor_and_config_keys()[1]

        current_config_index = self.spinBox_numDifferentMPPT.value() - 1

        invertor['module'] = str(self.inputName_invertor.text())
        invertor['type_inv'] = str(self.inputNumber_invertor.text())
        invertor['title_grid_line'] = str(self.inputTitle_grid_line.text())
        invertor['title_grid_line_length'] = str(self.inputTitle_grid_line_length.text())
        invertor['title_grid_top'] = str(self.inputTitle_grid_top.text())
        invertor['title_grid_switch'] = str(self.inputTitle_grid_switch.text())
        invertor['phase'] = 3 if self.checkUse_three_phase.isChecked() else 1
        invertor['use_5or4_line'] = True if self.checkUse_5or4_line.isChecked() else False
        invertor['inputs'] = int(self.inputCount_input_mppt.text())
        invertor['count_invertor'] = self.spinBox_CloneInvertor.value() #количество инверторов
        if not config_keys:
            self.add_mppt()
            invertor['diff_mppt'] = False
        else:
            invertor[config_keys[current_config_index]]['count_pv'] = int(self.inputSolar_count_on_the_chain.text())
            invertor[config_keys[current_config_index]]['count_mppt'] = int(self.inputCount_mppt.text())
            invertor[config_keys[current_config_index]]['count_string'] = int(self.inputAll_chain.text())
            invertor[config_keys[current_config_index]]['use_all_mppt'] = True if self.checkUse_all_mppt.isChecked() else False
            invertor[config_keys[current_config_index]]['use_y_connector'] = True if self.checkUse_y_connector.isChecked() else False
        self.statusBar.showMessage('Данные обновлены',2000)

    def spin_diff_mppt(self):
        invertor = self.invertor_and_config_keys()[0]
        config_keys = self.invertor_and_config_keys()[1]

        self.spinBox_numDifferentMPPT.show()
        self.spinBox_numDifferentMPPT.setMaximum(len(config_keys))

        current_config_index = self.spinBox_numDifferentMPPT.value() - 1

        self.inputSolar_count_on_the_chain.setText(str(invertor[config_keys[current_config_index]]['count_pv']))
        self.inputCount_mppt.setText(str(invertor[config_keys[current_config_index]]['count_mppt']))
        self.inputAll_chain.setText(str(invertor[config_keys[current_config_index]]['count_string']))
        self.checkUse_all_mppt.setCheckState(2 if invertor[config_keys[current_config_index]]['use_all_mppt'] == True else 0)
        self.checkUse_y_connector.setCheckState(2 if invertor[config_keys[current_config_index]]['use_y_connector'] == True else 0)

    def spin_diff_mpp_for_add(self):
        invertor = self.invertor_and_config_keys()[0]
        config_keys = self.invertor_and_config_keys()[1]

        self.spinBox_numDifferentMPPT.show()
        self.spinBox_numDifferentMPPT.setMaximum(len(config_keys))
        self.spinBox_numDifferentMPPT.setValue(len(config_keys))

        current_config_index = self.spinBox_numDifferentMPPT.value() - 1

        self.inputSolar_count_on_the_chain.setText(str(invertor[config_keys[current_config_index]]['count_pv']))
        self.inputCount_mppt.setText(str(invertor[config_keys[current_config_index]]['count_mppt']))
        self.inputAll_chain.setText(str(invertor[config_keys[current_config_index]]['count_string']))
        self.checkUse_all_mppt.setCheckState(2 if invertor[config_keys[current_config_index]]['use_all_mppt'] == True else 0)
        self.checkUse_y_connector.setCheckState(2 if invertor[config_keys[current_config_index]]['use_y_connector'] == True else 0)

    def add_mppt(self):
        if self.check_imput_params() != 0:
            return 1
        
        mppt = int(self.inputCount_mppt.text())
        inputs = int(self.inputCount_input_mppt.text())
        pv = int(self.inputSolar_count_on_the_chain.text())
        strings = int(self.inputAll_chain.text())
        y_connector = True if self.checkUse_y_connector.isChecked() else False
        all_mppt = True if self.checkUse_all_mppt.isChecked() else False

        invertor = self.invertor_and_config_keys()[0]
        config_keys = self.invertor_and_config_keys()[1]

        if not config_keys:
            name = 'config_0'
        else:
            name = f'config_{len(config_keys)}'

        # self.draw_params[name] = {'count_mppt': mppt,'count_inputs': inputs,'count_pv': pv,
        #                 'count_string': strings, 'use_y_connector': y_connector, 'use_all_mppt': all_mppt}

        invertor[name] = {'count_mppt': mppt, 'count_pv': pv,
                        'count_string': strings, 'use_y_connector': y_connector, 'use_all_mppt': all_mppt}
        invertor['diff_mppt'] = True
        self.spin_diff_mpp_for_add()

        # max_input = int(self.input_mppt) * int(self.count_mppt)
        # max_input_y = int(self.input_mppt) * int(self.count_mppt) * 2
        # self.textConsoleDraw.append("----------------------------")
        # self.textConsoleDraw.append("ИСХОДНЫЕ ДАННЫЕ:")
        # self.textConsoleDraw.append(f"- Число MPPT: {self.count_mppt}")
        # self.textConsoleDraw.append(f"- Число входов MPPT: {self.input_mppt}")
        # self.textConsoleDraw.append(f"- Число ФЭМ модулей в цепочке: {self.count_fem}")
        # self.textConsoleDraw.append(f"-Число цепочек: {self.all_chain}")
        # self.textConsoleDraw.append(f"-Максимальное кол-во входов без Y: {max_input}")
        # self.textConsoleDraw.append(f"-Максимальное кол-во входов c Y: {max_input_y}")

    def out_params(self):
        title_project = self.main_window.inputTitleProject.text()
        code_project = self.main_window.inputCodeProject.text()            
        # self.text_and_bool = {}
        # self.text_and_bool['title_inv'] = str(self.inputName_invertor.text())
        # self.text_and_bool['num_inv'] = str(self.inputNumber_invertor.text())
        # self.text_and_bool['title_grid_line'] = str(self.inputTitle_grid_line.text())
        # self.text_and_bool['title_grid_line_length'] = str(self.inputTitle_grid_line_length.text())
        # self.text_and_bool['title_grid_top'] = str(self.inputTitle_grid_top.text())
        # self.text_and_bool['title_grid_switch'] = str(self.inputTitle_grid_switch.text())
        # self.text_and_bool['use_three_phase'] = True if self.checkUse_three_phase.isChecked() else False
        # self.text_and_bool['use_5or4_line'] = True if self.checkUse_5or4_line.isChecked() else False
        # self.text_and_bool['count_invertor'] = self.spinBox_CloneInvertor.value() #количество инверторов

        # self.draw_params = {**self.draw_params, **self.text_and_bool}
        self.gost_frame_params = {'title_project': title_project, 'code_project': code_project}
        
    def draw(self):
        invertor = self.invertor_and_config_keys()[0]
        config_keys = self.invertor_and_config_keys()[1]
        print('Kontrolnie parametri::: ',invertor)

        if not config_keys:
            return print("Сохраните параметры")

        for num in range(1, len(config_keys)):
            self.spinBox_numDifferentMPPT.setValue(num)
            self.spin_diff_mppt()
            if self.validate_input() != 0:
                self.statusBar.showMessage('Неверная конфигурация MPPT', 4000)
                self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
                QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))
                return print('Ошибонька')
        
        self.out_params()

        self.btnDraw.setEnabled(False)
        self.btnDraw.setText('Построение...')
        self.statusBar.showMessage('Пожалуйста, подождите...')
        self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
    
        self.painter_draw_one = DrawOne(invertor, self.gost_frame_params)
        self.painter_draw_one.finished.connect(self.drawFinished)
        self.painter_draw_one.start()

    def drawFinished(self):
        if self.painter_draw_one.num_error['error'] == 0:
            self.textConsoleDraw.append("----------------------------")
            self.textConsoleDraw.append("РЕЗУЛЬТАТЫ:")
            self.textConsoleDraw.append(f" Всего цепочек: {self.painter_draw_one.chains}")
            self.textConsoleDraw.append(f" Всего модулей: {self.painter_draw_one.modules}")
            self.statusBar.showMessage('Чертеж успешно построен', 4000)
            self.statusBar.setStyleSheet("background-color:rgb(48, 219, 91)")
            QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))
            self.btnDraw.setEnabled(True)
            self.btnDraw.setText('Построить')
        elif self.painter_draw_one.num_error['error'] == 1:
            self.textConsoleDraw.append("!!!")
            self.textConsoleDraw.append("Кол-во цепочек меньше числа MPPT, невозможно заполгнить все MPPT")
            self.textConsoleDraw.append("---")
            self.statusBar.showMessage("Внимание!")
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.btnDraw.setEnabled(True)
            self.btnDraw.setText('Построить')
        elif self.painter_draw_one.num_error['error'] == 3:
            self.textConsoleDraw.append("!!!")
            self.textConsoleDraw.append("Данное количесво цепочек не вмещается, примените Y коннекторы, либо измените конфигурацию MPPT")
            self.textConsoleDraw.append("---")
            self.statusBar.showMessage("Внимание!")
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.btnDraw.setEnabled(True)
            self.btnDraw.setText('Построить')
        elif self.painter_draw_one.num_error['error'] == 4:
            self.textConsoleDraw.append("!!!")
            self.textConsoleDraw.append("Данное количесво цепочек слишком мало чтобы заполнить все MPPT применяя Y коннекторы, уберите Y коннекторы или полное заполнение")
            self.textConsoleDraw.append("---")
            self.statusBar.showMessage("Внимание!")
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.btnDraw.setEnabled(True)
            self.btnDraw.setText('Построить')
        elif self.painter_draw_one.num_error['error'] == 5:
            self.textConsoleDraw.append("!!!")
            self.textConsoleDraw.append("Слишком большое количество цепочек")
            self.textConsoleDraw.append("---")
            self.statusBar.showMessage("Внимание!")
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.btnDraw.setEnabled(True)
            self.btnDraw.setText('Построить')
        # Удаление потока после его использования.
        del self.painter_draw_one
 
 