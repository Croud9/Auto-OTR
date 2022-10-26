from operator import invert
import draw_schemes2
import designDrawSchemesTwo
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QThread

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
        self.main_window = instance_of_main_window
        self.spinBox_numInvertor.setMinimum(1)
        self.spinBox_numInvertor.setEnabled(False)
        self.spinBox_numOther.setMinimum(1)
        self.spinBox_numOther.setEnabled(False)
        self.checkUse_threePhase.stateChanged.connect(self.show_and_hide_color_line_because_phase)
        self.btnOpen_otherParams.clicked.connect(self.show_other_params)
        self.checkYellowLineInvertor.clicked.connect(self.show_and_hide_switch)
        self.checkRedLineInvertor.clicked.connect(self.show_and_hide_switch)
        self.checkBlueLineInvertor.clicked.connect(self.show_and_hide_switch)
        self.checkGreenLineInvertor.clicked.connect(self.show_and_hide_switch)
        self.checkYellowLineOther.clicked.connect(self.show_and_hide_switch)
        self.checkRedLineOther.clicked.connect(self.show_and_hide_switch)
        self.checkBlueLineOther.clicked.connect(self.show_and_hide_switch)
        self.checkGreenLineOther.clicked.connect(self.show_and_hide_switch)
        self.btnResultInfo.clicked.connect(self.result_info)
        self.btnReset.clicked.connect(self.reset)
        self.btnSaveConfig.clicked.connect(self.save_config)
        self.btnDraw.pressed.connect(self.draw)
        self.spinBox_numInvertor.valueChanged.connect(self.up_down_invertor_selection)
        self.spinBox_numOther.valueChanged.connect(self.up_down_other_device_selection)
        self.set_default_params()
        self.invertor_params = []
        self.other_params = []
        self.optional_params = []
        self.checkbox_params = []
        self.all_params = [self.invertor_params, self.other_params, self.optional_params, self.checkbox_params]   

    def reset(self):
        self.checkUse_threePhase.setCheckState(2)
        self.checkUse_yzip.setCheckState(0)
        self.checkUse_counter.setCheckState(0)
        self.textConsoleDraw.clear()
        self.invertor_params.clear()
        self.other_params.clear()
        self.optional_params.clear()
        self.checkbox_params.clear()

    def set_default_params(self):
        # Основные параемтры инвертора
        # self.inputName_invertor.setText("Sungrow SG110CX")
        # self.inputPower_invertor.setText('110')
        # self.inputAmperage_invertor.setText('158.8')

        # Основные параметры доп модулей
        # self.inputName_other.setText('Sungrow COM100E')
        # self.inputPower_other.setText('0.01')
        # self.inputAmperage_other.setText('0.05')
        # self.inputType_other.setText('Контроллер')

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
        self.invertor_params.append(str(self.inputParam2_invertor.text())) #5
        self.invertor_params.append("")
        self.invertor_params.append("")
        self.invertor_params.append("")
        self.invertor_params.append(str(self.inputParam6_invertor.text()))
        self.invertor_params.append(str(self.inputParam7_invertor.text()))

        self.invertor_params.append(True if self.checkYellowLineInvertor.isChecked() else False)
        self.invertor_params.append(True if self.checkRedLineInvertor.isChecked() else False) #12
        self.invertor_params.append(True if self.checkBlueLineInvertor.isChecked() else False)
        self.invertor_params.append(True if self.checkGreenLineInvertor.isChecked() else False) #14
        self.invertor_params.append(True if self.checkBlackLineInvertor.isChecked() else False)

        self.invertor_params.append(True if self.checkYellowSwitchInvertor.isChecked() else False)
        self.invertor_params.append(True if self.checkRedSwitchInvertor.isChecked() else False)
        self.invertor_params.append(True if self.checkBlueSwitchInvertor.isChecked() else False)
        self.invertor_params.append(True if self.checkGreenSwitchInvertor.isChecked() else False)

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
        if str(self.inputName_invertor.text()) == '':
            self.statusBar.showMessage('Введите название инвертора', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputName_invertor.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            return 1
        else:
            self.set_style_default()

        if str(self.inputPower_invertor.text()) == '':
            self.statusBar.showMessage('Введите мощность инвертора', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputPower_invertor.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            return 1
        else:
            self.set_style_default()

        if str(self.inputAmperage_invertor.text()) == '':
            self.statusBar.showMessage('Введите силу тока в инверторе', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputAmperage_invertor.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            return 1
        else:
            self.set_style_default()

        if str(self.inputName_other.text()) == '':
            self.statusBar.showMessage('Введите название доп. оборудования', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputName_other.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            return 1
        else:
            self.set_style_default()

        if str(self.inputPower_other.text()) == '':
            self.statusBar.showMessage('Введите мощность доп. оборудования', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputPower_other.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            return 1
        else:
            self.set_style_default()

        if str(self.inputAmperage_other.text()) == '':
            self.statusBar.showMessage('Введите силу тока в доп. оборудовании', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputAmperage_other.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            return 1
        else:
            self.set_style_default()

        if str(self.inputType_other.text()) == '':
            self.statusBar.showMessage('Введите тип доп. оборудования', 5000)
            self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
            self.inputType_other.setStyleSheet("border: 1.45px solid red; border-radius: 6; background-color:rgba(242,242,247,1);")
            return 1
        else:
            self.set_style_default()
        return 0

    def set_style_default(self):
        default_style_input = 'QLineEdit{ background-color:rgba(229,229,234,1);\
                            border-radius: 6;\
                            border: none;\
                            padding-left: 8px }\
                        QLineEdit:hover{ background-color:rgba(242,242,247,1); }\
                        QLineEdit:pressed{ background-color:rgba(188,188,192,1);\
                            border-radius: 12; }'
        self.inputName_invertor.setStyleSheet(default_style_input)
        self.inputPower_invertor.setStyleSheet(default_style_input)
        self.inputAmperage_invertor.setStyleSheet(default_style_input)
        self.inputName_other.setStyleSheet(default_style_input)
        self.inputPower_other.setStyleSheet(default_style_input)
        self.inputAmperage_other.setStyleSheet(default_style_input)
        self.inputType_other.setStyleSheet(default_style_input)

        self.statusBar.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.statusBar.showMessage('', 100)

    def save_config(self):
        if self.check_imput_params() != 0:
            return
        invertor = self.invertor_and_config_keys()
        invertor['module'] = str(self.inputName_invertor.text())
        invertor['p_max'] = str(self.inputPower_invertor.text())
        invertor['i_out_max'] = str(self.inputAmperage_invertor.text())
        invertor['count_invertor'] = self.spinBox_countInvertor.value()

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
        self.main_window.w3.up_down_invertor_selection()
        # print('Вторая схема: ', invertor)

    def invertor_and_config_keys(self):
        invertors = self.main_window.invertors
        self.spinBox_numInvertor.setMaximum(len(invertors))
        self.spinBox_numInvertor.setEnabled(True)
        spinbox_val = self.spinBox_numInvertor.value() - 1
        return invertors[f'found_invertor_{spinbox_val}']  

    def up_down_invertor_selection(self):
        invertor = self.invertor_and_config_keys()
        self.inputName_invertor.setText(f'{invertor["module"]}')
        self.inputPower_invertor.setText(f'{invertor["p_max"]}')
        self.inputAmperage_invertor.setText(f'{invertor["i_out_max"]}')
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
        self.inputName_other.setText(f'{other["title_other"]}')
        self.inputType_other.setText(f'{other["type_other"]}')
        self.inputPower_other.setText(f'{other["power_other"]}')
        self.inputAmperage_other.setText(f'{other["i_other"]}')
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
        if self.check_imput_params() != 0:
            return

        self.out_params()

        self.btnDraw.setEnabled(False)
        self.btnDraw.setText('Построение чертежа...')
        self.statusBar.showMessage('Пожалуйста, подождите...')
        self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
        self.painter = DrawTwo(self.draw_params, self.gost_frame_params)
        self.painter.finished.connect(self.drawFinished)
        self.painter.start()
        
    def drawFinished(self):
        self.all_params.clear()
        self.invertor_params.clear()
        self.other_params.clear()
        self.optional_params.clear()
        self.statusBar.showMessage('Чертеж успешно построен', 4000)
        self.statusBar.setStyleSheet("background-color:rgb(48, 219, 91)")
        QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet("background-color:rgb(255, 255, 255)"))
        self.textConsoleDraw.append(f"------------------------------------")

        self.btnDraw.setEnabled(True)
        self.btnDraw.setText('Построить')
        # Удаление потока после его использования.
        del self.painter

 