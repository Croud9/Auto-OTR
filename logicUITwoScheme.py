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
        self.btnAdd_invertor.hide()
        self.btnAdd_other.hide()
        self.btnShowInvertor.hide()
        self.btnShowOther.hide()
        self.checkUse_threePhase.stateChanged.connect(self.show_and_hide_color_line_because_phase)
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
        self.spinBox_numInvertor.valueChanged.connect(self.up_down_invertor_selection)
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

    def set_default_params(self):
        # Основные параемтры инвертора
        # self.inputName_invertor.setText("Sungrow SG110CX")
        # self.inputPower_invertor.setText('110')
        # self.inputAmperage_invertor.setText('158.8')

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
        self.inputName_invertor.setStyleSheet("QLineEdit{\n	background-color:rgba(229,229,234,1); \n	border-radius: 6;\n	border: none;\n}\nQLineEdit:hover{\n	background-color:rgba(242,242,247,1);\n}\nQLineEdit:pressed{\n	background-color:rgba(188,188,192,1);\n	border-radius: 12;\n}")
        self.inputPower_invertor.setStyleSheet("QLineEdit{\n	background-color:rgba(229,229,234,1); \n	border-radius: 6;\n	border: none;\n}\nQLineEdit:hover{\n	background-color:rgba(242,242,247,1);\n}\nQLineEdit:pressed{\n	background-color:rgba(188,188,192,1);\n	border-radius: 12;\n}")
        self.inputAmperage_invertor.setStyleSheet("QLineEdit{\n	background-color:rgba(229,229,234,1); \n	border-radius: 6;\n	border: none;\n}\nQLineEdit:hover{\n	background-color:rgba(242,242,247,1);\n}\nQLineEdit:pressed{\n	background-color:rgba(188,188,192,1);\n	border-radius: 12;\n}")
        self.inputName_other.setStyleSheet("QLineEdit{\n	background-color:rgba(229,229,234,1); \n	border-radius: 6;\n	border: none;\n}\nQLineEdit:hover{\n	background-color:rgba(242,242,247,1);\n}\nQLineEdit:pressed{\n	background-color:rgba(188,188,192,1);\n	border-radius: 12;\n}")
        self.inputPower_other.setStyleSheet("QLineEdit{\n	background-color:rgba(229,229,234,1); \n	border-radius: 6;\n	border: none;\n}\nQLineEdit:hover{\n	background-color:rgba(242,242,247,1);\n}\nQLineEdit:pressed{\n	background-color:rgba(188,188,192,1);\n	border-radius: 12;\n}")
        self.inputAmperage_other.setStyleSheet("QLineEdit{\n	background-color:rgba(229,229,234,1); \n	border-radius: 6;\n	border: none;\n}\nQLineEdit:hover{\n	background-color:rgba(242,242,247,1);\n}\nQLineEdit:pressed{\n	background-color:rgba(188,188,192,1);\n	border-radius: 12;\n}")
        self.inputType_other.setStyleSheet("QLineEdit{\n	background-color:rgba(229,229,234,1); \n	border-radius: 6;\n	border: none;\n}\nQLineEdit:hover{\n	background-color:rgba(242,242,247,1);\n}\nQLineEdit:pressed{\n	background-color:rgba(188,188,192,1);\n	border-radius: 12;\n}")

        self.statusBar.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.statusBar.showMessage('', 100)

    def up_down_invertor_selection(self):
        invertors = self.main_window.invertors
        self.spinBox_numInvertor.setMinimum(1)
        self.spinBox_numInvertor.setMaximum(len(invertors))

        spinbox_val = self.spinBox_numInvertor.value() - 1

        invertor = invertors[f'found_invertor_{spinbox_val}']

        self.inputName_invertor.setText(f'{invertor["module"]}')
        self.inputPower_invertor.setText(f'{invertor["p_max"]}')
        self.inputAmperage_invertor.setText(f'{invertor["i_out_max"]}')
        if invertor['phase'] == 3:
            self.checkUse_threePhase.setCheckState(2)
        elif invertor['phase'] == 1:
            self.checkUse_threePhase.setCheckState(0)

        config_keys = []    
        for key in invertor.keys():
            if 'config' in key:
                config_keys.append(key)

        count_invertors = 0
        for config in config_keys:
            count_invertor = invertor[config]['count_invertor']
            if '.' in count_invertor:
                count_invertors += float(count_invertor)
            else:
                count_invertors += int(count_invertor)
        self.spinBox_countInvertor.setValue(int(count_invertors))
        
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
        
        title_project = self.main_window.inputTitleProject.text()
        code_project = self.main_window.inputCodeProject.text() 
        gost_frame_params = {'title_project': title_project, 'code_project': code_project}   
            
        self.btnDraw.setEnabled(False)
        self.btnDraw.setText('Построение чертежа...')
        self.statusBar.showMessage('Пожалуйста, подождите...')
        self.statusBar.setStyleSheet("background-color:rgb(255, 212, 38)")
        self.painter = DrawTwo(self.all_params, gost_frame_params)
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

 