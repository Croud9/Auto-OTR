import os
from views import designDrawSchemes, styles_and_animation
from helpers import validate
from creators import draw_schemes
from os.path import isfile, join
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtCore import QSize, QTimer, QThread

class DrawOne(QThread):
    def __init__(self, draw_params, gost_frame_params, many_schemes):
        super().__init__()
        self.draw_params = draw_params
        self.many_schemes = many_schemes
        self.count_invertor = self.draw_params['count_invertor']
        self.gost_frame_params = gost_frame_params
        self.modules = 0
        self.chains = 0

    def run(self):
        fp_invertor = 'Data/Schemes/Invertor/'
        files_in_invertor = [f for f in os.listdir(fp_invertor) if isfile(join(fp_invertor, f))]
        if len(files_in_invertor) != 0:
            for file in files_in_invertor:
                os.remove(fp_invertor + f"/{file}") 

        config_keys = []    
        for key in self.draw_params.keys():
            if 'config' in key:
                config_keys.append(key)

        if self.draw_params['diff_mppt'] == True:
            for num in range(self.count_invertor):
                num += 1
                self.num_error = draw_schemes.draw(self.draw_params, num, self.gost_frame_params, False)
                if self.num_error['error'] != 0: return 
                self.modules += self.num_error['modules']
                self.chains += self.num_error['chains']
        else:
            numbr = 0
            if self.many_schemes == True:
                for config in config_keys:
                    counts = int(self.draw_params[config]['count_invertor'])
                    for num in range(counts):
                        numbr += 1
                        self.num_error = draw_schemes.draw(self.draw_params, numbr, self.gost_frame_params, config)
                        if self.num_error['error'] != 0: return 
                        self.modules += self.num_error['modules']
                        self.chains += self.num_error['chains']
            else:
                for config in config_keys:
                    counts = int(self.draw_params[config]['count_invertor'])
                    start_num = numbr
                    numbr += counts
                    if counts > 1:
                        if start_num == 0:
                            nums = f"{1}-{numbr}"
                        else:
                            nums = f"{start_num}-{numbr}"
                    else:
                        nums = numbr
                        
                    self.num_error = draw_schemes.draw(self.draw_params, nums, self.gost_frame_params, config)
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
        self.btnOpenScheme.clicked.connect(self.open_scheme)
        self.btnAdd_new_mppt.clicked.connect(self.add_mppt)
        self.btnDelConfig.clicked.connect(self.del_mppt)
        self.btnUpdateConsole.clicked.connect(self.update_console)
        # self.btnReset.clicked.connect(self.reset)
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
        self.btnOpenScheme.hide()
        self.btnDelConfig.hide()
        self.spinBox_CloneInvertor.setMinimum(1)
        self.show_and_hide_color_line_because_phase()
        self.btnSaveConfig.setIcon(QIcon('Data/System/Icons/save.png'))
        self.btnSaveConfig.setIconSize(QSize(30, 30))
        self.movie = QMovie('Data/System/Icons/loading_gif250trans.gif')
        self.labelLoading.setMovie(self.movie)
        self.draw_params = {}
        self.fields_text = [self.inputCount_mppt, self.inputCount_input_mppt, self.inputSolar_count_on_the_chain, self.inputAll_chain]

    def open_scheme(self):
        self.path_structural_schemes = [QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл структурной схемы', 
                                                                            'Data/Schemes/Invertor', "*.svg")[0]]
        if len(self.path_structural_schemes[0]) != 0:
            os.startfile(self.path_structural_schemes[0])

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
        self.spinBox_numInvertor.setValue(1)
        self.spinBox_numInvertor.setEnabled(False)
        self.spinBox_numDifferentMPPT.setMinimum(1)
        self.spinBox_numDifferentMPPT.setMaximum(1)
        self.spinBox_CloneInvertor.setValue(1)
        self.btnOpenScheme.hide()
        self.inputName_invertor.clear()
        self.inputNumber_invertor.clear()
        self.inputTitle_grid_line.clear()
        self.inputTitle_grid_line_length.clear()
        self.inputTitle_grid_top.clear()
        self.inputTitle_grid_switch.clear()
        self.inputCountAllInvertors.clear()

    def invertor_and_config_keys(self):
        invertors = self.main_window.invertors
        self.spinBox_numInvertor.setMaximum(len(invertors))
        self.spinBox_numInvertor.setEnabled(True)

        spinbox_val = self.spinBox_numInvertor.value() - 1
        invertor = invertors[f'found_invertor_{spinbox_val}']

        config_keys = []
        local_keys = []
        counts_config_inv = []
        for key in invertor.keys():
            if 'local' in key:
                local_keys.append(key)    
            elif 'config' in key:
                config_keys.append(key)
        if invertor['diff_mppt'] == False:
            for key in config_keys:
                if invertor[key].get('count_invertor', 'N/D') != 'N/D':
                    counts_config_inv.append(int(invertor[key]['count_invertor']))

        return invertor, config_keys, local_keys, counts_config_inv  

    def up_down_invertor_selection(self):
        invertor = self.invertor_and_config_keys()[0]
        config_keys = self.invertor_and_config_keys()[1]
        if invertor['broken_file'] != True:
            self.inputName_invertor.setText(f'{invertor["module"]}')
            self.inputName_invertor.setCursorPosition(0)
            self.inputCount_mppt.setText(f'{invertor["mppt"]}')
            self.inputCount_input_mppt.setText(f'{invertor["inputs"]}')
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
            self.inputCountAllInvertors.setText(f"{invertor['count_invertor']}")
            self.checkDifferentMPPT.setCheckState(2 if invertor['diff_mppt'] == True else 0)

            if invertor['diff_mppt'] == True:
                self.spinBox_CloneInvertor.setValue(int(invertor['count_invertor']))
                self.spin_diff_mppt(False)
                self.show_and_hide_different_mppt(True) # разные mppt
            else:
                if not config_keys:
                    self.inputCount_mppt.setText(str(invertor['mppt']))
                    self.inputSolar_count_on_the_chain.setText(str(0))
                    self.inputAll_chain.setText(str(0))
                    self.show_and_hide_different_mppt(False)
                else:
                    self.inputSolar_count_on_the_chain.setText(str(invertor['config_0']['count_pv']))
                    self.inputCount_mppt.setText(str(invertor['config_0']['count_mppt']))
                    self.inputAll_chain.setText(str(invertor['config_0']['count_string']))
                    self.checkUse_y_connector.setCheckState(2 if invertor['config_0']['use_y_connector'] == True else 0)
                    self.spin_diff_mppt(False)
                    self.show_and_hide_different_mppt(True)

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
            styles_and_animation.no_fill_field(self, self.inputCount_mppt)
            return 1
        elif self.inputCount_input_mppt.text() == '':
            styles_and_animation.no_fill_field(self, self.inputCount_input_mppt)
            return 1
        elif self.inputSolar_count_on_the_chain.text() == '':
            styles_and_animation.no_fill_field(self, self.inputSolar_count_on_the_chain)
            return 1
        elif self.inputAll_chain.text() == '':
            styles_and_animation.no_fill_field(self, self.inputAll_chain)
            return 1
        else:
            return 0

    def set_style_default(self):
        self.inputCount_mppt.setStyleSheet(styles_and_animation.default_style_input)
        self.inputCount_input_mppt.setStyleSheet(styles_and_animation.default_style_input)
        self.inputSolar_count_on_the_chain.setStyleSheet(styles_and_animation.default_style_input)
        self.inputAll_chain.setStyleSheet(styles_and_animation.default_style_input)

        self.statusBar.setStyleSheet(styles_and_animation.status_white)
        self.statusBar.showMessage('', 100)

    def show_and_hide_different_mppt(self, status):
        if status == True:
            self.spinBox_numDifferentMPPT.show()
            if self.spinBox_numDifferentMPPT.value() > 1:
                self.btnDelConfig.show()
            else:
                self.btnDelConfig.hide()
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
        local_keys = self.invertor_and_config_keys()[2]
        counts_inv = self.invertor_and_config_keys()[3]

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
        
        if not config_keys:
            self.add_mppt()
            invertor['diff_mppt'] = False
        else:
            invertor[config_keys[current_config_index]]['count_pv'] = int(self.inputSolar_count_on_the_chain.text())
            invertor[config_keys[current_config_index]]['count_mppt'] = int(self.inputCount_mppt.text())
            invertor[config_keys[current_config_index]]['count_string'] = int(self.inputAll_chain.text())
            invertor[config_keys[current_config_index]]['use_all_mppt'] = True if self.checkUse_all_mppt.isChecked() else False
            invertor[config_keys[current_config_index]]['use_y_connector'] = True if self.checkUse_y_connector.isChecked() else False

            diff_mppt = 2 if self.checkDifferentMPPT.isChecked() else 0
            start_rng = 0
            if diff_mppt == 2:
                invertor['diff_mppt'] = True
                invertor['count_invertor'] = self.spinBox_CloneInvertor.value() #количество инверторов
                count_inv = int(invertor['count_invertor'])
            else:
                invertor['diff_mppt'] = False
                invertor[config_keys[current_config_index]]['count_invertor'] = self.spinBox_CloneInvertor.value() #количество инверторов
                count_inv = int(invertor[config_keys[current_config_index]]['count_invertor'])
                start_rng = sum(counts_inv[:current_config_index])
                old_count_inv = sum(counts_inv)
                counts_inv = self.invertor_and_config_keys()[3]
                new_count_inv = sum(counts_inv)
                invertor['count_invertor'] = new_count_inv

                if new_count_inv < old_count_inv:
                    for num in range(start_rng, start_rng + (old_count_inv - new_count_inv)):
                        current_local = f'local_{num}'
                        del invertor[current_local]
                    local_keys = self.invertor_and_config_keys()[2]
                    index = 0
                    for key in local_keys:
                        invertor[f'local_{index}'] = invertor.pop(key)
                        index += 1
                elif new_count_inv == old_count_inv:
                    for num in range(start_rng, start_rng + count_inv):
                        current_local = f'local_{num}'
                        invertor[current_local]['strings'] = int(self.inputAll_chain.text())
                else:
                    index = start_rng + new_count_inv - old_count_inv
                    invertor_for_local = {}
                    for key in local_keys[start_rng:]:
                        invertor_for_local[f'local_{index}'] = invertor.pop(key)
                        index += 1 
                    for num in range(new_count_inv - old_count_inv):
                        current_local = f'local_{start_rng + num}'
                        invertor[current_local] = {'controller': False, 'commutator': False, 'left_yzip': False, 'right_yzip': False,  
                                                    'title_other_device': 'УЗИП', 'strings': int(self.inputAll_chain.text())}
                        num += 1
                    for key, value in invertor_for_local.items():
                        invertor[key] = value
        if invertor.get('i_nom_inv', 'nill') != 'nill':
            self.main_window.w4.up_down_invertor_selection()
        self.main_window.w6.up_down_invertor_selection()
        self.up_down_invertor_selection()
        self.statusBar.showMessage('Параметры сохранены', 2000)
        self.statusBar.setStyleSheet(styles_and_animation.status_green)
        QTimer.singleShot(2000, lambda: self.statusBar.setStyleSheet(styles_and_animation.status_white))

    def spin_diff_mppt(self, add_new_mppt):
        invertor = self.invertor_and_config_keys()[0]
        config_keys = self.invertor_and_config_keys()[1]
        if len(config_keys) != 0:
            self.spinBox_numDifferentMPPT.show()
            self.spinBox_numDifferentMPPT.setMaximum(len(config_keys))
            if add_new_mppt == True:
                self.spinBox_numDifferentMPPT.setValue(len(config_keys))
            current_config_index = self.spinBox_numDifferentMPPT.value() - 1
            if invertor[config_keys[current_config_index]].get('count_invertor', 'N/D') != 'N/D' and invertor['diff_mppt'] == False:
                self.spinBox_CloneInvertor.setValue(int(invertor[config_keys[current_config_index]]['count_invertor']))

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
        count_inv = int(self.spinBox_CloneInvertor.value())
        pv = int(self.inputSolar_count_on_the_chain.text())
        strings = int(self.inputAll_chain.text())
        y_connector = True if self.checkUse_y_connector.isChecked() else False
        all_mppt = True if self.checkUse_all_mppt.isChecked() else False
        diff_mppt = 2 if self.checkDifferentMPPT.isChecked() else 0

        invertor = self.invertor_and_config_keys()[0]
        config_keys = self.invertor_and_config_keys()[1]
        local_keys = self.invertor_and_config_keys()[2]

        if not config_keys:
            name = 'config_0'
        else:
            name = f'config_{len(config_keys)}'

        if diff_mppt == 2:
            invertor['diff_mppt'] = True
            invertor[name] = {'count_mppt': mppt, 'count_pv': pv,
                            'count_string': strings, 'use_y_connector': y_connector, 'use_all_mppt': all_mppt}
        else:
            invertor['diff_mppt'] = False
            invertor[name] = {'count_invertor': count_inv, 'count_mppt': mppt, 'count_pv': pv,
                            'count_string': strings, 'use_y_connector': y_connector, 'use_all_mppt': all_mppt}
        for num in range(count_inv):
            invertor[f'local_{len(local_keys) + num}'] = {'controller': False, 'commutator': False, 'left_yzip': False, 'right_yzip': False,  
                                        'title_other_device': 'УЗИП', 'strings': strings}
        self.spin_diff_mppt(True)
        self.save_config()

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
        self.save_config()
        if self.spinBox_numDifferentMPPT.value() == 1:
            self.show_and_hide_different_mppt(False)

    def out_params(self):
        title_project = self.main_window.inputTitleProject.text()
        code_project = self.main_window.inputCodeProject.text()            
        code_project = self.main_window.inputCodeProject.text()            
        self.many_schemes = True if self.checkManySchemes.isChecked() else False
             
        self.gost_frame_params = {'title_project': title_project, 'code_project': code_project}
        
    def draw(self):
        invertor = self.invertor_and_config_keys()[0]
        config_keys = self.invertor_and_config_keys()[1]

        if not config_keys:
            self.statusBar.showMessage('Сохраните параметры', 2000)
            self.statusBar.setStyleSheet(styles_and_animation.status_yellow)
            QTimer.singleShot(2000, lambda: self.statusBar.setStyleSheet(styles_and_animation.status_white))
            return 

        for num in range(1, len(config_keys)):
            self.spinBox_numDifferentMPPT.setValue(num)
            self.spin_diff_mppt(False)
            if self.validate_input() != 0:
                self.statusBar.showMessage('Неверная конфигурация MPPT', 4000)
                self.statusBar.setStyleSheet(styles_and_animation.status_yellow)
                QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet(styles_and_animation.status_white))
                return
        
        self.out_params()

        self.btnDraw.setEnabled(False)
        self.btnDraw.setText('Построение...')
        styles_and_animation.animation_start(self.movie, self.labelLoading)
        self.btnOpenScheme.hide()
    
        self.painter_draw_one = DrawOne(invertor, self.gost_frame_params, self.many_schemes)
        self.painter_draw_one.finished.connect(self.drawFinished)
        self.painter_draw_one.start()

    def drawFinished(self):
        if self.painter_draw_one.num_error['error'] == 0:
            self.textConsoleDraw.append("----------------------------")
            self.textConsoleDraw.append("РЕЗУЛЬТАТЫ:")
            self.textConsoleDraw.append(f" Всего цепочек: {self.painter_draw_one.chains}")
            self.textConsoleDraw.append(f" Всего модулей: {self.painter_draw_one.modules}")
            self.statusBar.showMessage('Чертеж успешно построен', 4000)
            self.statusBar.setStyleSheet(styles_and_animation.status_green)
            QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet(styles_and_animation.status_white))
            self.btnOpenScheme.show()
        elif self.painter_draw_one.num_error['error'] == 1:
            self.textConsoleDraw.append("!!!")
            self.textConsoleDraw.append("Кол-во цепочек меньше числа MPPT, невозможно заполгнить все MPPT")
            self.textConsoleDraw.append("---")
            self.statusBar.showMessage("Внимание!")
            self.statusBar.setStyleSheet(styles_and_animation.status_red)
        elif self.painter_draw_one.num_error['error'] == 3:
            self.textConsoleDraw.append("!!!")
            self.textConsoleDraw.append("Данное количесво цепочек не вмещается, примените Y коннекторы, либо измените конфигурацию MPPT")
            self.textConsoleDraw.append("---")
            self.statusBar.showMessage("Внимание!")
            self.statusBar.setStyleSheet(styles_and_animation.status_red)
        elif self.painter_draw_one.num_error['error'] == 4:
            self.textConsoleDraw.append("!!!")
            self.textConsoleDraw.append("Данное количесво цепочек слишком мало чтобы заполнить все MPPT применяя Y коннекторы, уберите Y коннекторы или полное заполнение")
            self.textConsoleDraw.append("---")
            self.statusBar.showMessage("Внимание!")
            self.statusBar.setStyleSheet(styles_and_animation.status_red)
        elif self.painter_draw_one.num_error['error'] == 5:
            self.textConsoleDraw.append("!!!")
            self.textConsoleDraw.append("Слишком большое количество цепочек")
            self.textConsoleDraw.append("---")
            self.statusBar.showMessage("Внимание!")
            self.statusBar.setStyleSheet(styles_and_animation.status_red)
        styles_and_animation.animation_stop(self.movie, self.labelLoading)
        self.btnDraw.setEnabled(True)
        self.btnDraw.setText('Построить')
        del self.painter_draw_one
 
 