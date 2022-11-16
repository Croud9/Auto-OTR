import draw_structural_scheme
# import svg_scheme_viewer
import designDrawStructuralScheme
import styles_responce
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QTimer, QThread
from PyQt5 import QtSvg
import sys, os
from PyQt5 import QtSvg
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class DrawStructural(QThread):
    def __init__(self, invertors, gost_frame_params, general_scheme_data):
        super().__init__()
        self.invertors = invertors
        self.gost_frame_params = gost_frame_params
        self.general_scheme_data = general_scheme_data

    def run(self):
        draw_structural_scheme.draw(self.invertors, self.gost_frame_params, self.general_scheme_data)

class WindowDrawStructural(QtWidgets.QMainWindow, designDrawStructuralScheme.Ui_WindowDrawSchemes):
    def __init__(self, instance_of_main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = instance_of_main_window
        self.input_data()
        self.checkWifi.stateChanged.connect(self.show_and_hide_internet)
        self.checkController.stateChanged.connect(self.show_and_hide_commutator)
        self.btnDraw.clicked.connect(self.draw)
        self.btnOpenScheme.clicked.connect(self.open_scheme)
        self.btnSaveConfig.clicked.connect(self.save_config)
        self.spinBox_numInvertor.valueChanged.connect(self.up_down_invertor_selection)
        self.spinBox_CountInvertors.valueChanged.connect(self.spin_local)

    def input_data(self):
        self.btnOpenScheme.hide()
        self.spinBox_numInvertor.setMinimum(1)
        self.spinBox_numInvertor.setEnabled(False)
        self.spinBox_CountInvertors.setEnabled(False)
        self.checkCommutator.setEnabled(False)
        self.checkWebServer.setEnabled(False)
        self.checkCommutator.setCheckState(0)
        self.btnSaveConfig.setIcon(QIcon('data/cons/dop/save.png'))
        self.btnSaveConfig.setIconSize(QSize(30, 30))
        self.general_scheme_data = {}

    def open_scheme(self):
        os.startfile("Data\Schemes\Structural\structural.svg")

    def viewFinished(self):
        del self.painter_view

    def invertor_and_config_keys(self):
        invertors = self.main_window.invertors
        self.spinBox_numInvertor.setMaximum(len(invertors))
        self.spinBox_numInvertor.setEnabled(True)
        spinbox_val = self.spinBox_numInvertor.value() - 1
        invertor = invertors[f'found_invertor_{spinbox_val}']
  
        count_strings = 0    
        local_keys = []    
        for key in invertor.keys():
            if 'local' in key:
                local_keys.append(key)
            elif 'config' in key:
                count_strings += int(invertor[key]['count_string'])

        invertor['total_count_strings'] = count_strings

        return {'invertor': invertor,'local_keys': local_keys}  

    def up_down_invertor_selection(self):
        current_data = self.invertor_and_config_keys()
        invertor = current_data['invertor']
        local_keys = current_data['local_keys']

        self.inputName_invertor.setText(f'{invertor["module"]}')
        self.inputCountPV.setText(f"{invertor['total_count_strings']}")

        excess = len(local_keys) - int(invertor['count_invertor'])
        if excess > 0:
            del local_keys[ : -excess]
            for current_local in local_keys:
                if current_local in invertor.keys():
                    del invertor[current_local]
        self.spin_local()

    def spin_local(self):
        current_data = self.invertor_and_config_keys()
        invertor = current_data['invertor']
        self.spinBox_CountInvertors.setEnabled(True)
        self.spinBox_CountInvertors.setMinimum(1)       
        self.spinBox_CountInvertors.setMaximum(int(invertor['count_invertor']))
        current_local_index = self.spinBox_CountInvertors.value() - 1
        self.inputTitleOtherDevice.setText(f"{invertor[f'local_{current_local_index}']['title_other_device']}")
        self.checkController.setCheckState(2 if invertor[f'local_{current_local_index}']['controller'] == True else 0)
        self.checkCommutator.setCheckState(2 if invertor[f'local_{current_local_index}']['commutator'] == True else 0)
        self.checkYzipLeft.setCheckState(2 if invertor[f'local_{current_local_index}']['left_yzip'] == True else 0)
        self.checkYzipRight.setCheckState(2 if invertor[f'local_{current_local_index}']['right_yzip'] == True else 0)

    def show_and_hide_internet(self):
        if self.checkWifi.isChecked():
            self.checkUnitedInternet.setEnabled(False)
            self.checkUnitedInternet.setCheckState(0)
            self.checkWebServer.setEnabled(True)
        else:
            self.checkUnitedInternet.setEnabled(True)
            self.checkWebServer.setCheckState(0)
            self.checkWebServer.setEnabled(False)
            
    def show_and_hide_commutator(self):
        if self.checkController.isChecked():
            self.checkCommutator.setEnabled(True)
        else:
            self.checkCommutator.setEnabled(False)
            self.checkCommutator.setCheckState(0)

    def save_config(self):
        if self.spinBox_CountInvertors.value() != 0:
            current_data = self.invertor_and_config_keys()
            invertor = current_data['invertor']
            current_local_index = self.spinBox_CountInvertors.value() - 1
            controller = True if self.checkController.isChecked() else False
            commutator = True if self.checkCommutator.isChecked() else False
            yzip_l = True if self.checkYzipLeft.isChecked() else False
            yzip_r = True if self.checkYzipRight.isChecked() else False
            title_other_device = self.inputTitleOtherDevice.text()

            invertor[f'local_{current_local_index}'] = {'controller': controller, 'commutator': commutator, 'left_yzip': yzip_l,
                                                        'right_yzip': yzip_r, 'title_other_device': title_other_device}
            print(invertor)
            self.statusBar.showMessage('Параметры сохранены', 2000)
            self.statusBar.setStyleSheet(styles_responce.status_green)
            QTimer.singleShot(2000, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))

    def total_calculate(self):
        invertors = self.main_window.invertors
        invertor_keys = [] 
        local_keys = []    
        for key in invertors.keys():
            if 'found_invertor' in key:
                invertor_keys.append(key)
                
        for invertor in invertor_keys:
            for key in invertors[invertor].keys():
                if 'local' in key:
                    local_keys.append(key)

        self.general_scheme_data['count_all_invertors'] = len(local_keys)
        self.general_scheme_data['invertor_keys'] = invertor_keys

    def out_params(self):        
        self.general_scheme_data['wifi'] = True if self.checkWifi.isChecked() else False
        self.general_scheme_data['web_server'] = True if self.checkWebServer.isChecked() else False
        self.general_scheme_data['united_internet'] = True if self.checkUnitedInternet.isChecked() else False
        self.general_scheme_data['united_energy_shield'] = True if self.checkUnitedOut.isChecked() else False
        title_project = self.main_window.inputTitleProject.text()
        code_project = self.main_window.inputCodeProject.text()                   
        self.gost_frame_params = {'title_project': title_project, 'code_project': code_project}

    def draw(self):
        self.total_calculate()

        if self.general_scheme_data['count_all_invertors'] == 0:
            self.statusBar.showMessage('Сконфигурируйте параметры', 2000)
            self.statusBar.setStyleSheet(styles_responce.status_yellow)
            QTimer.singleShot(2000, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))
            return 
        
        self.out_params()
        invertors = self.main_window.invertors

        self.btnDraw.setEnabled(False)
        self.btnDraw.setText('Построение...')
        self.painter_draw_struct = DrawStructural(invertors, self.gost_frame_params, self.general_scheme_data)
        self.painter_draw_struct.finished.connect(self.drawFinished)
        self.painter_draw_struct.start()

    def drawFinished(self):
        self.statusBar.showMessage('Чертеж успешно построен', 4000)
        self.statusBar.setStyleSheet(styles_responce.status_green)
        QTimer.singleShot(4000, lambda: self.statusBar.setStyleSheet(styles_responce.status_white))
        self.btnDraw.setEnabled(True)
        self.btnDraw.setText('Построить')
        self.btnOpenScheme.show()
        del self.painter_draw_struct