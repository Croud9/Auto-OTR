from PyQt5.QtCore import QTimer

# перевод дизайна
# cd "C:\PythonPRJCT\autoReportPdf"
# pyuic5 designCalcPV.ui -o designCalcPV.py
# pyuic5 designRepPDF.ui -o designRepPDF.py
# pyuic5 designParsing.ui -o designParsing.py
# pyuic5 designDrawSchemes.ui -o designDrawSchemes.py
# pyuic5 designDrawSchemesTwo.ui -o designDrawSchemesTwo.py
# pyuic5 designDrawStructuralScheme.ui -o designDrawStructuralScheme.py
# pyuic5 designAbout.ui -o designAbout.py

'👌✅👍🤟🤘🔥📍🌐'
status_ok = ' ' * 117 +'🔥'
status_info = "background-color: rgba(229,229,234,1); color:  #025238; font-weight: bold;"
status_orange = "background-color:rgba(255, 169, 31, 0.89)"
status_yellow = "background-color:rgb(255, 212, 38)"
status_white = "background-color:rgb(255, 255, 255)"
status_green = "background-color:rgb(48, 219, 91)"
status_red = "background-color:rgb(255, 105, 97)"
default_style_input = 'QLineEdit{ background-color:rgba(229,229,234,1);\
                        border-radius: 6;\
                        border: none;\
                        padding-left: 8px }\
                    QLineEdit:hover{ background-color:rgba(242,242,247,1); }\
                    QLineEdit:pressed{ background-color:rgba(188,188,192,1);\
                        border-radius: 12; }'
default_style_comboBox = 'QComboBox{ background-color:rgba(229,229,234,1);\
                            border: none;\
                            border-radius: 6;\
                            padding-left: 8px;}\
                        QComboBox:drop-down{ width: 0px;\
                            height: 0px;\
                            border: 0px; }\
                        QComboBox:hover{ background-color:rgba(242,242,247,1); }'
warning_style_comboBox = 'QComboBox{background-color:rgba(229,229,234,1);\
                                border: 1.45px solid red;\
                                border-radius: 6;\
                                padding-left: 6.55px;}\
                            QComboBox:drop-down {width: 0px;\
                                height: 0px;\
                                border: 0px;}'
warning_style_input = 'border: 1.45px solid red;\
                        border-radius: 6;\
                        background-color:rgba(242,242,247,1);\
                        padding-left: 6.55px;'

def red_status(self):
    self.statusBar.setStyleSheet("background-color:rgb(255, 105, 97)")
    QTimer.singleShot(5000, lambda: self.statusBar.setStyleSheet("background-color: rgb(255,255,255)"))

def no_fill_field(self, field):
    self.statusBar.showMessage('Введите значение в выделенное поле', 5000)
    red_status(self)
    field.setStyleSheet(warning_style_input)

def animation_start(gif, label):
    gif.start()
    label.show()

def animation_stop(gif, label):
    gif.stop()
    label.hide()