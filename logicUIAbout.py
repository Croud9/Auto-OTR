import designAbout
from PyQt5 import QtWidgets
  
class WindowAbout(QtWidgets.QMainWindow, designAbout.Ui_MainWindow):
    def __init__(self, instance_of_main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = instance_of_main_window

        self.labelGithubLink.setText('<a style="background-color:rgba(112, 215, 255, 0);\
                                        color:rgba(0, 0, 0, 0.5);\
                                        border: none;\
                                        border-radius: 5;\
                                        border-style: outset;\
                                        text-decoration: none;" href="https://github.com/Croud9/Auto-OTR">  Croud9</a>')

        self.labelGithubLink.setOpenExternalLinks(True)



