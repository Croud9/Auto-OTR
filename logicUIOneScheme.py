import draw_schemes
import designDrawSchemes
import styles_responce
import validate
from PyQt5 import QtWidgets
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QThread, QRegExp, QTimer
from PyQt5.QtGui import *
from PyQt5.QtCore import *

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
        self.input_data()
        validate.validate_number(self.fields_text)
        self.main_window = instance_of_main_window
        self.btnDraw.clicked.connect(self.draw)
        self.btnAdd_new_mppt.clicked.connect(self.add_mppt)
        self.btnDelConfig.clicked.connect(self.del_mppt)
        self.btnUpdateConsole.clicked.connect(self.update_console)
        self.btnReset.clicked.connect(self.reset)
        self.btnSaveConfig.clicked.connect(self.save_config)
        self.checkUse_5or4_line.clicked.connect(self.show_and_hide_color_line_because_phase)
        self.inputCount_mppt.textChanged.connect(self.validate_input)
        self.inputAll_chain.textChanged.connect(self.validate_input)
        self.inputCount_input_mppt.textChanged.connect(self.validate_input)
        self.checkUse_three_phase.stateChanged.connect(self.show_and_hide_color_line_because_phase)
        self.checkUse_y_connector.stateChanged.connect(self.validate_input)
        self.checkUse_all_mppt.stateChanged.connect(self.validate_input)
        self.spinBox_numInvertor.valueChanged.connect(self.up_down_invertor_selection)
        self.spinBox_numDifferentMPPT.valueChanged.connect(lambda: self.spin_diff_mppt(False))

    def input_data(self):
        self.spinBox_numInvertor.setMinimum(1)
        self.spinBox_numInvertor.setEnabled(False)
        self.spinBox_numDifferentMPPT.setMinimum(1)
        self.spinBox_numDifferentMPPT.hide()
        self.btnDelConfig.hide()
        self.spinBox_CloneInvertor.setMinimum(1)
        self.btnSaveConfig.setIcon(QIcon('data/cons/dop/save.png'))
        self.btnSaveConfig.setIconSize(QSize(30, 30))
        self.draw_params = {}
        self.fields_text = [self.inputCount_mppt, self.inputCount_input_mppt, self.inputSolar_count_on_the_chain, self.inputAll_chain]

    def reset(self):
        self.inputCount_mppt.clear()
        self.inputCount_input_mppt.clear()
        self.inputSolar_count_on_the_chain.clear()
        self.inputAll_chain.clear()
        self.checkUse_y_connector.setCheckState(0)
        self.checkUse_all_mppt.setCheckState(0)
        self.checkUse_three_phase.setCheckState(0)
        self.checkUse_5or4_line.setCheckState(0)
        self.checkUse_5or4_line.setEnabled(False)
        self.textConsoleDraw.clear()
        self.textConsoleCurrent.clear()

    def invertor_and_config_keys(self):
        invertors = self.main_window.invertors
        self.spinBox_numInvertor.setMaximum(len(invertors))
        self.spinBox_numInvertor.setEnabled(True)

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
            self.show_and_hide_different_mppt(True) # разные mppt
            self.spin_diff_mppt(False)
        else:
            for config in config_keys:
                self.inputSolar_count_on_the_chain.setText(str(invertor[config]['count_pv']))
                self.inputCount_mppt.setText(str(invertor[config]['count_mppt']))
                self.inputAll_chain.setText(str(invertor[config]['count_string']))
                self.inputAll_chain.setText(str(invertor[config]['count_string']))
                self.checkUse_y_connector.setCheckState(2 if invertor[config]['use_y_connector'] == True else 0)
            if not config_keys:
                self.inputCount_mppt.setText(str(invertor['mppt']))
                self.inputSolar_count_on_the_chain.setText(str(0))
                self.inputAll_chain.setText(str(0))
            self.spinBox_numDifferentMPPT.hide()
            self.show_and_hide_different_mppt(False)

    def show_and_hide_color_line_because_phase(self):
        if self.checkUse_three_phase.isChecked():
            self.checkUse_5or4_line.setEnabled(True)
        else:
            self.checkUse_5or4_line.setEnabled(False)
            self.checkUse_5or4_line.setCheckState(0)

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
        self.set_style_default()
        if self.inputCount_mppt.text() == '':
            styles_responce.no_fill_field(self, self.inputCount_mppt)
            return 1
        elif self.inputCount_input_mppt.text() == '':
            styles_responce.no_fill_field(self, self.inputCount_input_mppt)
            return 1
        elif self.inputSolar_count_on_the_chain.text() == '':
            styles_responce.no_fill_field(self, self.inputSolar_count_on_the_chain)
            return 1
        elif self.inputAll_chain.text() == '':
            styles_responce.no_fill_field(self, self.inputAll_chain)
            return 1
        else:
            return 0

    def set_style_default(self):
        self.inputCount_mppt.setStyleSheet(styles_responce.default_style_input)
        self.inputCount_input_mppt.setStyleSheet(styles_responce.default_style_input)
        self.inputSolar_count_on_the_chain.setStyleSheet(styles_responce.default_style_input)
        self.inputAll_chain.setStyleSheet(styles_responce.default_style_input)

        self.statusBar.setStyleSheet(styles_responce.status_white)
        self.statusBar.showMessage('', 100)

    def show_and_hide_different_mppt(self, status):
        if status == True:
            self.spinBox_numDifferentMPPT.show()
            if self.spinBox_numDifferentMPPT.value() > 1:
                self.btnDelConfig.show()
        else:
            self.spinBox_numDifferentMPPT.hide()
            self.btnDelConfig.hide()

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
        self.main_window.w4.up_down_invertor_selection()
        self.statusBar.showMessage('Параметры сохранены', 2000)
        self.statusBar.setStyleSheet(styles_responce.status_green)
        QTimer.singleShot(2000, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))

    def spin_diff_mppt(self, add_new_mppt):
        invertor = self.invertor_and_config_keys()[0]
        config_keys = self.invertor_and_config_keys()[1]
        self.spinBox_numDifferentMPPT.show()
        self.spinBox_numDifferentMPPT.setMaximum(len(config_keys))
        if add_new_mppt == True:
            self.spinBox_numDifferentMPPT.setValue(len(config_keys))
        current_config_index = self.spinBox_numDifferentMPPT.value() - 1

        self.inputSolar_count_on_the_chain.setText(str(invertor[config_keys[current_config_index]]['count_pv']))
        self.inputCount_mppt.setText(str(invertor[config_keys[current_config_index]]['count_mppt']))
        self.inputAll_chain.setText(str(invertor[config_keys[current_config_index]]['count_string']))
        self.checkUse_all_mppt.setCheckState(2 if invertor[config_keys[current_config_index]]['use_all_mppt'] == True else 0)
        self.checkUse_y_connector.setCheckState(2 if invertor[config_keys[current_config_index]]['use_y_connector'] == True else 0)
        if len(config_keys) > 1:
            self.btnDelConfig.show()

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

        invertor[name] = {'count_mppt': mppt, 'count_pv': pv,
                        'count_string': strings, 'use_y_connector': y_connector, 'use_all_mppt': all_mppt}
        invertor['diff_mppt'] = True
        self.spin_diff_mppt(True)

    def del_mppt(self):
        invertor = self.invertor_and_config_keys()[0]
        config_keys = self.invertor_and_config_keys()[1]
        current_config_index = self.spinBox_numDifferentMPPT.value() - 1
        del invertor[config_keys[current_config_index]]
        del config_keys[current_config_index]
        index = 0
        for key in config_keys:
            invertor[f'config_{index}'] = invertor.pop(key)
            index += 1

        self.spin_diff_mppt(True)
        if self.spinBox_numDifferentMPPT.value() == 1:
            self.show_and_hide_different_mppt(False)

    def out_params(self):
        title_project = self.main_window.inputTitleProject.text()
        code_project = self.main_window.inputCodeProject.text()            
        self.gost_frame_params = {'title_project': title_project, 'code_project': code_project}
        
    def draw(self):
        invertor = self.invertor_and_config_keys()[0]
        config_keys = self.invertor_and_config_keys()[1]

        if not config_keys:
            self.statusBar.showMessage('Сохраните параметры', 2000)
            self.statusBar.setStyleSheet(styles_responce.status_yellow)
            QTimer.singleShot(2000, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))
            return 

        for num in range(1, len(config_keys)):
            self.spinBox_numDifferentMPPT.setValue(num)
            self.spin_diff_mppt(False)
            if self.validate_input() != 0:
                self.statusBar.showMessage('Неверная конфигурация MPPT', 4000)
                self.statusBar.setStyleSheet(styles_responce.status_yellow)
                QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))
                return
        
        self.out_params()

        self.btnDraw.setEnabled(False)
        self.btnDraw.setText('Построение...')
        self.statusBar.showMessage('Пожалуйста, подождите...')
        self.statusBar.setStyleSheet(styles_responce.status_yellow)
    
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
            self.statusBar.setStyleSheet(styles_responce.status_green)
            QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))
            self.btnDraw.setEnabled(True)
            self.btnDraw.setText('Построить')
        elif self.painter_draw_one.num_error['error'] == 1:
            self.textConsoleDraw.append("!!!")
            self.textConsoleDraw.append("Кол-во цепочек меньше числа MPPT, невозможно заполгнить все MPPT")
            self.textConsoleDraw.append("---")
            self.statusBar.showMessage("Внимание!")
            self.statusBar.setStyleSheet(styles_responce.status_red)
            self.btnDraw.setEnabled(True)
            self.btnDraw.setText('Построить')
        elif self.painter_draw_one.num_error['error'] == 3:
            self.textConsoleDraw.append("!!!")
            self.textConsoleDraw.append("Данное количесво цепочек не вмещается, примените Y коннекторы, либо измените конфигурацию MPPT")
            self.textConsoleDraw.append("---")
            self.statusBar.showMessage("Внимание!")
            self.statusBar.setStyleSheet(styles_responce.status_red)
            self.btnDraw.setEnabled(True)
            self.btnDraw.setText('Построить')
        elif self.painter_draw_one.num_error['error'] == 4:
            self.textConsoleDraw.append("!!!")
            self.textConsoleDraw.append("Данное количесво цепочек слишком мало чтобы заполнить все MPPT применяя Y коннекторы, уберите Y коннекторы или полное заполнение")
            self.textConsoleDraw.append("---")
            self.statusBar.showMessage("Внимание!")
            self.statusBar.setStyleSheet(styles_responce.status_red)
            self.btnDraw.setEnabled(True)
            self.btnDraw.setText('Построить')
        elif self.painter_draw_one.num_error['error'] == 5:
            self.textConsoleDraw.append("!!!")
            self.textConsoleDraw.append("Слишком большое количество цепочек")
            self.textConsoleDraw.append("---")
            self.statusBar.showMessage("Внимание!")
            self.statusBar.setStyleSheet(styles_responce.status_red)
            self.btnDraw.setEnabled(True)
            self.btnDraw.setText('Построить')
        # Удаление потока после его использования.
        del self.painter_draw_one
 
 