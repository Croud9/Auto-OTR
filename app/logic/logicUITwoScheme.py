import os
from views import styles_and_animation, designDrawSchemesTwo
from helpers import validate
from creators import draw_schemes2
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtCore import QSize, QTimer, QThread

class DrawTwo(QThread):
    def __init__(self, params, gost_frame_params):
        super().__init__()
        self.params = params
        self.gost_frame_params = gost_frame_params

    def run(self):
        draw_schemes2.draw(self.params, self.gost_frame_params) 
        
class WindowDrawTwo(QtWidgets.QMainWindow, designDrawSchemesTwo.Ui_WindowDrawSchemesTwo):
    def __init__(self, instance_of_main_window):
        super().__init__()
        self.setupUi(self)
        self.input_data() 
        validate.validate_number(self.fields_text)
        self.main_window = instance_of_main_window
        self.btnOpenScheme.clicked.connect(self.open_scheme)
        self.btnOpen_otherParams.clicked.connect(self.show_other_params)
        self.checkYellowLineInvertor.clicked.connect(self.show_and_hide_switch)
        self.checkRedLineInvertor.clicked.connect(self.show_and_hide_switch)
        self.checkBlueLineInvertor.clicked.connect(self.show_and_hide_switch)
        self.checkGreenLineInvertor.clicked.connect(self.show_and_hide_switch)
        self.checkYellowLineOther.clicked.connect(self.show_and_hide_switch)
        self.checkRedLineOther.clicked.connect(self.show_and_hide_switch)
        self.checkBlueLineOther.clicked.connect(self.show_and_hide_switch)
        self.checkGreenLineOther.clicked.connect(self.show_and_hide_switch)
        self.btnSaveConfig.clicked.connect(self.save_config)
        # self.btnReset.clicked.connect(self.reset)
        self.btnDraw.pressed.connect(self.draw)
        self.checkUse_threePhase.stateChanged.connect(self.show_and_hide_color_line_because_phase)
        self.spinBox_numInvertor.valueChanged.connect(self.up_down_invertor_selection)
        self.spinBox_numOther.valueChanged.connect(self.up_down_other_device_selection)

    def reset(self):
        self.checkUse_threePhase.setCheckState(2)
        self.checkUse_yzip.setCheckState(0)
        self.checkUse_counter.setCheckState(0)
        self.textConsoleDraw.clear()
        self.btnOpenScheme.hide()
        self.inputName_invertor.clear()
        self.inputPower_invertor.clear()
        self.inputAmperage_invertor.clear()
        self.spinBox_countInvertor.setMinimum(0)
        self.spinBox_countInvertor.setValue(0)

    def input_data(self):
        self.btnOpenScheme.hide()
        self.spinBox_numInvertor.setMinimum(1)
        self.spinBox_numInvertor.setEnabled(False)
        self.spinBox_numOther.setMinimum(1)
        self.spinBox_numOther.setEnabled(False)
        self.btnSaveConfig.setIcon(QIcon('Data/System/Icons/save.png'))
        self.btnSaveConfig.setIconSize(QSize(30, 30))
        self.movie = QMovie('Data/System/Icons/loading_gif250trans.gif')
        self.labelLoading.setMovie(self.movie)
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
        self.inputParam2_out.setCursorPosition(0)
        self.inputParam3_out.setCursorPosition(0)
        self.inputParam5_out.setCursorPosition(0)

        self.checkRedLineInvertor.setEnabled(False)
        self.checkRedSwitchInvertor.setEnabled(False)
        self.checkGreenLineInvertor.setEnabled(False)
        self.checkGreenSwitchInvertor.setEnabled(False)

        self.checkYellowLineInvertor.setCheckState(2)
        self.checkYellowSwitchInvertor.setCheckState(2)
        self.checkBlueLineInvertor.setCheckState(2)
        self.checkBlueSwitchInvertor.setCheckState(2)
        self.checkBlackLineInvertor.setCheckState(2)

        self.checkRedLineOther.setEnabled(False)
        self.checkRedSwitchOther.setEnabled(False)
        self.checkGreenLineOther.setEnabled(False)
        self.checkGreenSwitchOther.setEnabled(False)
        self.checkYellowLineOther.setCheckState(2)
        self.checkYellowSwitchOther.setCheckState(2)
        self.checkBlueLineOther.setCheckState(2)
        self.checkBlueSwitchOther.setCheckState(2)
        self.checkBlackLineOther.setCheckState(2)
        self.fields_text = [self.inputPower_invertor, self.inputAmperage_invertor, self.inputPower_other, self.inputAmperage_other]

    def open_scheme(self):
        os.startfile("Data\Schemes\General\connect_system.svg")

    def show_other_params(self):
        if self.width() == 950 and self.height() == 335:
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

            self.checkRedLineOther.setCheckState(2)
            self.checkRedSwitchOther.setCheckState(2)
            self.checkGreenLineOther.setCheckState(2)
            self.checkGreenSwitchOther.setCheckState(2)

            self.checkRedLineInvertor.setCheckState(2)
            self.checkRedSwitchInvertor.setCheckState(2)
            self.checkGreenLineInvertor.setCheckState(2)
            self.checkGreenSwitchInvertor.setCheckState(2)
        else:
            self.checkRedLineInvertor.setEnabled(False)
            self.checkRedSwitchInvertor.setEnabled(False)
            self.checkGreenLineInvertor.setEnabled(False)
            self.checkGreenSwitchInvertor.setEnabled(False)

            self.checkRedLineOther.setEnabled(False)
            self.checkRedSwitchOther.setEnabled(False)
            self.checkGreenLineOther.setEnabled(False)
            self.checkGreenSwitchOther.setEnabled(False)
            
            self.checkRedLineInvertor.setCheckState(0)
            self.checkRedSwitchInvertor.setCheckState(0)
            self.checkGreenLineInvertor.setCheckState(0)
            self.checkGreenSwitchInvertor.setCheckState(0)

            self.checkRedLineOther.setCheckState(0)
            self.checkRedSwitchOther.setCheckState(0)
            self.checkGreenLineOther.setCheckState(0)
            self.checkGreenSwitchOther.setCheckState(0)

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

    def check_imput_params(self):
        self.set_style_default()
        if str(self.inputName_invertor.text()) == '':
            styles_and_animation.no_fill_field(self, self.inputName_invertor)
            return 1
        elif str(self.inputPower_invertor.text()) == '':
            styles_and_animation.no_fill_field(self, self.inputPower_invertor)
            return 1
        elif str(self.inputAmperage_invertor.text()) == '':
            styles_and_animation.no_fill_field(self, self.inputAmperage_invertor)
            return 1
        elif str(self.inputName_other.text()) == '':
            styles_and_animation.no_fill_field(self, self.inputName_other)
            return 1
        elif str(self.inputPower_other.text()) == '':
            styles_and_animation.no_fill_field(self, self.inputPower_other)
            return 1
        elif str(self.inputAmperage_other.text()) == '':
            styles_and_animation.no_fill_field(self, self.inputAmperage_other)
            return 1
        elif str(self.inputType_other.text()) == '':
            styles_and_animation.no_fill_field(self, self.inputType_other)
            return 1
        else:
            return 0

    def set_style_default(self):
        self.inputName_invertor.setStyleSheet(styles_and_animation.default_style_input)
        self.inputPower_invertor.setStyleSheet(styles_and_animation.default_style_input)
        self.inputAmperage_invertor.setStyleSheet(styles_and_animation.default_style_input)
        self.inputName_other.setStyleSheet(styles_and_animation.default_style_input)
        self.inputPower_other.setStyleSheet(styles_and_animation.default_style_input)
        self.inputAmperage_other.setStyleSheet(styles_and_animation.default_style_input)
        self.inputType_other.setStyleSheet(styles_and_animation.default_style_input)

        self.statusBar.setStyleSheet(styles_and_animation.status_white)
        self.statusBar.showMessage('', 100)

    def save_config(self):
        if self.check_imput_params() != 0:
            return
        invertor = self.invertor_and_config_keys()
        local_keys = []    
        for key in invertor.keys():
            if 'local' in key:
                local_keys.append(key)

        invertor['module'] = str(self.inputName_invertor.text())
        invertor['p_max'] = str(self.inputPower_invertor.text())
        invertor['i_out_max'] = str(self.inputAmperage_invertor.text())
        invertor['count_invertor'] = self.spinBox_countInvertor.value()
        for num in range(int(invertor['count_invertor'])):
            current_local = f'local_{num}'
            if not current_local in local_keys:
                invertor[current_local] = {'controller': False, 'commutator': False, 'left_yzip': False, 'right_yzip': False}

        invertor['type_inv'] = str(self.inputParam1_invertor.text())
        invertor['i_nom_inv'] = str(self.inputParam2_invertor.text())
        invertor['brand_cable_inv'] = str(self.inputParam6_invertor.text())
        invertor['length_cable_inv'] = str(self.inputParam7_invertor.text())

        invertor['yellow_line_inv'] = True if self.checkYellowLineInvertor.isChecked() else False
        invertor['red_line_inv'] = True if self.checkRedLineInvertor.isChecked() else False
        invertor['blue_line_inv'] = True if self.checkBlueLineInvertor.isChecked() else False
        invertor['green_line_inv'] = True if self.checkGreenLineInvertor.isChecked() else False
        invertor['black_line_inv'] = True if self.checkBlackLineInvertor.isChecked() else False

        invertor['yellow_switch_inv'] = True if self.checkYellowSwitchInvertor.isChecked() else False
        invertor['red_switch_inv'] = True if self.checkRedSwitchInvertor.isChecked() else False
        invertor['blue_switch_inv'] = True if self.checkBlueSwitchInvertor.isChecked() else False
        invertor['green_switch_inv'] = True if self.checkGreenSwitchInvertor.isChecked() else False

        other = self.other_device_and_config_keys()
        other['title_other'] = str(self.inputName_other.text())
        other['type_other'] = str(self.inputType_other.text())
        other['power_other'] = str(self.inputPower_other.text())
        other['i_other'] = str(self.inputAmperage_other.text())
        other['count_other'] = self.spinBox_countOther.value()

        other['type_param_other'] = str(self.inputParam1_other.text())
        other['i_nom_other'] = str(self.inputParam2_other.text())
        other['brand_cable_other'] = str(self.inputParam6_other.text())
        other['length_cable_other'] = str(self.inputParam7_other.text())

        other['yellow_line_other'] = True if self.checkYellowLineOther.isChecked() else False
        other['red_line_other'] = True if self.checkRedLineOther.isChecked() else False
        other['blue_line_other'] = True if self.checkBlueLineOther.isChecked() else False
        other['green_line_other'] = True if self.checkGreenLineOther.isChecked() else False
        other['black_line_other'] = True if self.checkBlackLineOther.isChecked() else False

        other['yellow_switch_other'] = True if self.checkYellowSwitchOther.isChecked() else False
        other['red_switch_other'] = True if self.checkRedSwitchOther.isChecked() else False
        other['blue_switch_other'] = True if self.checkBlueSwitchOther.isChecked() else False
        other['green_switch_other'] = True if self.checkGreenSwitchOther.isChecked() else False
        if invertor.get('title_grid_line', False) != False:
            self.main_window.w3.up_down_invertor_selection()
            self.main_window.w6.up_down_invertor_selection()
        self.statusBar.showMessage('Параметры сохранены', 2000)
        self.statusBar.setStyleSheet(styles_and_animation.status_green)
        QTimer.singleShot(2000, lambda: self.statusBar.setStyleSheet(styles_and_animation.status_white))

    def invertor_and_config_keys(self):
        invertors = self.main_window.invertors
        self.spinBox_numInvertor.setMaximum(len(invertors))
        self.spinBox_numInvertor.setEnabled(True)
        spinbox_val = self.spinBox_numInvertor.value() - 1
        return invertors[f'found_invertor_{spinbox_val}']  

    def up_down_invertor_selection(self):
        invertor = self.invertor_and_config_keys()
        if invertor['broken_file'] != True:
            self.inputName_invertor.setText(f'{invertor["module"]}')
            self.inputName_invertor.setCursorPosition(0)
            self.inputPower_invertor.setText(f'{invertor["p_max"]}')
            self.inputAmperage_invertor.setText(f'{invertor["i_out_max"]}')
            self.spinBox_countInvertor.setMinimum(1)
            self.spinBox_countInvertor.setValue(int(invertor['count_invertor']))
            if invertor['phase'] == 3:
                self.checkUse_threePhase.setCheckState(2)
            elif invertor['phase'] == 1:
                self.checkUse_threePhase.setCheckState(0)

            self.inputParam1_invertor.setText(f"{invertor['type_inv']}")
            self.inputParam2_invertor.setText(f"{invertor['i_nom_inv']}")
            self.inputParam6_invertor.setText(f"{invertor['brand_cable_inv']}")
            self.inputParam7_invertor.setText(f"{invertor['length_cable_inv']}")

            self.checkYellowLineInvertor.setCheckState(2 if invertor['yellow_line_inv'] == True else 0)
            self.checkRedLineInvertor.setCheckState(2 if invertor['red_line_inv'] == True else 0)
            self.checkBlueLineInvertor.setCheckState(2 if invertor['blue_line_inv'] == True else 0)
            self.checkGreenLineInvertor.setCheckState(2 if invertor['green_line_inv'] == True else 0)
            self.checkBlackLineInvertor.setCheckState(2 if invertor['black_line_inv'] == True else 0)

            self.checkYellowSwitchInvertor.setCheckState(2 if invertor['yellow_switch_inv'] == True else 0)
            self.checkRedSwitchInvertor.setCheckState(2 if invertor['red_switch_inv'] == True else 0)
            self.checkBlueSwitchInvertor.setCheckState(2 if invertor['blue_switch_inv'] == True else 0)
            self.checkGreenSwitchInvertor.setCheckState(2 if invertor['green_switch_inv'] == True else 0)

    def other_device_and_config_keys(self):
        others = self.main_window.others
        self.spinBox_numOther.setMaximum(len(others))
        self.spinBox_numOther.setEnabled(True)
        spinbox_val = self.spinBox_numOther.value() - 1
        return others[f'found_other_{spinbox_val}']   

    def up_down_other_device_selection(self):
        other = self.other_device_and_config_keys()
        if other['table_data']['broken_file'] != True:
            self.inputName_other.setText(f'{other["title_other"]}')
            self.inputName_other.setCursorPosition(0)
            self.inputType_other.setText(f'{other["type_other"]}')
            self.inputPower_other.setText(f'{other["power_other"]}')
            self.inputAmperage_other.setText(f'{other["i_other"]}')
            self.spinBox_countOther.setMinimum(1)
            self.spinBox_countOther.setValue(int(other['count_other']))

            self.inputParam1_other.setText(f"{other['type_param_other']}")
            self.inputParam2_other.setText(f"{other['i_nom_other']}")
            self.inputParam6_other.setText(f"{other['brand_cable_other']}")
            self.inputParam7_other.setText(f"{other['length_cable_other']}")

            self.checkYellowLineOther.setCheckState(2 if other['yellow_line_other'] == True else 0)
            self.checkRedLineOther.setCheckState(2 if other['red_line_other'] == True else 0)
            self.checkBlueLineOther.setCheckState(2 if other['blue_line_other'] == True else 0)
            self.checkGreenLineOther.setCheckState(2 if other['green_line_other'] == True else 0)
            self.checkBlackLineOther.setCheckState(2 if other['black_line_other'] == True else 0)

            self.checkYellowSwitchOther.setCheckState(2 if other['yellow_switch_other'] == True else 0)
            self.checkRedSwitchOther.setCheckState(2 if other['red_switch_other'] == True else 0)
            self.checkBlueSwitchOther.setCheckState(2 if other['blue_switch_other'] == True else 0)
            self.checkGreenSwitchOther.setCheckState(2 if other['green_switch_other'] == True else 0)

    def out_params(self):
        invertors = self.main_window.invertors
        others = self.main_window.others
        use_yzip = True if self.checkUse_yzip.isChecked() else False
        use_counter = True if self.checkUse_counter.isChecked() else False
        use_threePhase = True if self.checkUse_threePhase.isChecked() else False
        code_project = self.main_window.inputCodeProject.text() 
        title_project = self.main_window.inputTitleProject.text()

        self.draw_params = {**invertors, **others, 'use_yzip': use_yzip, 'use_counter': use_counter, 'use_threePhase': use_threePhase}
        self.gost_frame_params = {'title_project': title_project, 'code_project': code_project}   
        self.draw_params['brand_cable_yzip'] = str(self.inputParam1_yzip.text())
        self.draw_params['type_param_yzip'] = str(self.inputParam2_yzip.text())
        self.draw_params['i_nom_yzip'] = str(self.inputParam3_yzip.text())
        self.draw_params['brand_cable_out'] = str(self.inputParam2_out.text())
        self.draw_params['cable_out'] = str(self.inputParam3_out.text())
        self.draw_params['length_cable_out'] = str(self.inputParam4_out.text())
        self.draw_params['type_param_out'] = str(self.inputParam5_out.text())

    def draw(self):
        invertors = self.main_window.invertors
        if self.check_imput_params() != 0:
            return
        if invertors['found_invertor_0']['module'] == 'Н/Д':
            self.statusBar.showMessage('Сохраните параметры', 2000)
            self.statusBar.setStyleSheet(styles_and_animation.status_yellow)
            QTimer.singleShot(2000, lambda: self.statusBar.setStyleSheet(styles_and_animation.status_white))
            return

        self.out_params()

        self.btnDraw.setEnabled(False)
        self.btnDraw.setText('Построение чертежа...')
        self.btnOpenScheme.hide()
        styles_and_animation.animation_start(self.movie, self.labelLoading)
        self.painter = DrawTwo(self.draw_params, self.gost_frame_params)
        self.painter.finished.connect(self.drawFinished)
        self.painter.start()
        
    def drawFinished(self):
        self.statusBar.showMessage('Чертеж успешно построен', 4000)
        self.statusBar.setStyleSheet(styles_and_animation.status_green)
        styles_and_animation.animation_stop(self.movie, self.labelLoading)
        QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet(styles_and_animation.status_white))
        self.textConsoleDraw.append(f"------------------------------------")
        self.btnDraw.setEnabled(True)
        self.btnDraw.setText('Построить')
        self.btnOpenScheme.show()
        del self.painter

 