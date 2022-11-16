import sys
from PyQt5 import QtSvg
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyGraphicsView(QGraphicsView):
    def __init__(self, w, h):
        super().__init__()
        # QGraphicsView.__init__(self)
        self.setGeometry(0, 0, w, h)                # screen size

class MyGraphicsScene(QGraphicsScene):
    def __init__(self, w, h, svgItem):
        super().__init__()
        # QGraphicsScene.__init__(self)

        self.setSceneRect(0, 0, w, h)           # screen size

        svgItem.setScale(1)                     # scale the svg to an appropriate size
        self.addItem(svgItem)
        svgItem.setPos(0, 0)

def main(file):
    app = QApplication(sys.argv)
    screen_size = app.primaryScreen().size() 
    svgItem = QtSvg.QGraphicsSvgItem(file)
    svgSize = svgItem.renderer().defaultSize()     
    width = svgSize.width()
    height = svgSize.height() 
    graphicsScene = MyGraphicsScene(width, height, svgItem)
    graphicsView = MyGraphicsView(width, height)
    graphicsView.setScene(graphicsScene)
    graphicsView.show()
    app.exec_() 

file = "Data\Schemes\Invertor\invertor2.svg"
file2 = "Data\Schemes\General\connect_system.svg"
# main(file)










