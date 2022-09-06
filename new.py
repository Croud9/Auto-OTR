from turtle import width
import schemdraw
import schemdraw.elements as elm
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from fontTools.ttLib import TTFont



def frame_legend(slr):
    width = 2.5
    height = 0.4
 
    slr += elm.Line().left().length(10)
    slr += elm.Line().up().length(height*3).linewidth(1.75)
    slr.push()
    slr += elm.Line().right().length(6).label('Cхема электрическая \n принципиальная ЩР 0,4 кВ (ВИЭ)',"center", ofst=(0,-0.7)).linewidth(1.75)
    slr += elm.Line().down().length(height*3).linewidth(1.75).hold()
    slr += elm.Line().right().length(4).linewidth(1.75)
    slr.pop()
    
    slr += elm.Line().up().length(height*3).linewidth(1.75)
    slr.push()
    slr += elm.Line().right().length(6).label('Основные технические решения',"center", ofst=(0,-1)).linewidth(1.75)
    
    slr.push()
    slr += elm.Line().down().length(height).linewidth(1.75)
    slr += elm.Line().right().length(1.25).label('ОТР',"center", ofst=(0,-0.5)).linewidth(1.75).hold()
    slr += elm.Line().down().length(height*2).linewidth(1.75)
    slr.pop()
    
    slr += elm.Line().right().length(1.25).label('Стадия',"center", ofst=(0,-0.2)).linewidth(1.75)
    slr.push()
    slr += elm.Line().down().length(height).linewidth(1.75)
    slr += elm.Line().right().length(1.25).label('3',"center", ofst=(0,-0.5)).linewidth(1.75).hold()
    slr += elm.Line().down().length(height*2).linewidth(1.75)
    slr.pop()
    
    slr += elm.Line().right().length(1.25).label('Лист',"center", ofst=(0,-0.2)).linewidth(1.75)
    slr.push()
    slr += elm.Line().down().length(height).linewidth(1.75)
    slr += elm.Line().right().length(1.5).label('36',"center", ofst=(0,-0.5)).linewidth(1.75).hold()
    slr += elm.Line().down().length(height*2).linewidth(1.75)
    slr.pop()
    slr += elm.Line().right().length(1.5).label('Листов',"center", ofst=(0,-0.2)).linewidth(1.75)
    slr.pop()
    
    slr += elm.Line().up().length(height*3).linewidth(1.75)
    slr += elm.Line().right().length(10).label('"Шлюмберже. Липецк. СЭС 363,4 кВт"',"center", ofst=(0,-1)).linewidth(1.75).hold()
    slr += elm.Line().up().length(height*2).linewidth(1.75)
    slr += elm.Line().right().length(10).label('2215ШЛБ-СЭС-ОТР',"center", ofst=(0,-0.5), fontsize=14).linewidth(1.75).hold()
    
    #
    slr += elm.Line().left().length(1).linewidth(1.75)
    slr.push()
    for i in range(3):
        slr += elm.Line().down().length(height).linewidth(1.75)
        slr += elm.Line().right().length(1).hold()
    slr += elm.Line().down().length(height).linewidth(1.75)
    slr += elm.Line().right().length(1).label('Дата',"center", ofst=(0,-0.2)).linewidth(1.75).hold()
    slr += elm.Line().down().length(height).linewidth(1.75)
    slr += elm.Line().right().length(1).linewidth(1.75).hold()
    for i in range(6):
        slr += elm.Line().down().length(height).linewidth(1.75)
        slr += elm.Line().right().length(1).hold()
    slr.pop()
    
    #
    slr += elm.Line().left().length(1.5).linewidth(1.75)
    slr.push()
    for i in range(3):
        slr += elm.Line().down().length(height).linewidth(1.75)
        slr += elm.Line().right().length(1.5).hold()
    slr += elm.Line().down().length(height).linewidth(1.75)
    slr += elm.Line().right().length(1.5).label('Подпись',"center", ofst=(0,-0.2)).linewidth(1.75).hold()
    slr += elm.Line().down().length(height).linewidth(1.75)
    slr += elm.Line().right().length(1.5).linewidth(1.75).hold()
    for i in range(6):
        slr += elm.Line().down().length(height).linewidth(1.75)
        slr += elm.Line().right().length(1.5).hold()
    slr.pop()
    
    #
    slr += elm.Line().left().length(1).linewidth(1.75)
    slr.push()
    for i in range(3):
        slr += elm.Line().down().length(height).linewidth(1.75)
        slr += elm.Line().right().length(1).hold()
    slr += elm.Line().down().length(height).linewidth(1.75)
    slr += elm.Line().right().length(1).label('N.док.',"center", ofst=(0,-0.2)).linewidth(1.75).hold()
    slr += elm.Line().down().length(height).linewidth(1.75)
    slr += elm.Line().right().length(1).linewidth(1.75).hold()
    slr.pop()
    
    slr += elm.Line().left().length(1).linewidth(1.75)
    slr.push()
    for i in range(3):
        slr += elm.Line().down().length(height).linewidth(1.75)
        slr += elm.Line().right().length(1).hold()
    slr += elm.Line().down().length(height).linewidth(1.75)
    slr += elm.Line().right().length(1).label('Лист',"center", ofst=(0,-0.2)).linewidth(1.75).hold()
    slr += elm.Line().down().length(height).linewidth(1.75)
    slr += elm.Line().right().length(1).linewidth(1.75).hold()
    for i in range(6):
        slr += elm.Line().down().length(height).linewidth(1.75)
        slr += elm.Line().right().length(2).hold()
    slr.pop()
    
    #
    slr += elm.Line().left().length(1).linewidth(1.75)
    slr.push()
    for i in range(3):
        slr += elm.Line().down().length(height).linewidth(1.75)
        slr += elm.Line().right().length(1).hold()
    slr += elm.Line().down().length(height).linewidth(1.75)
    slr += elm.Line().right().length(1).label('Кол.уч.',"center", ofst=(0,-0.2)).linewidth(1.75).hold()
    slr += elm.Line().down().length(height).linewidth(1.75)
    slr += elm.Line().right().length(1).linewidth(1.75).hold()
    slr.pop()
    
    slr += elm.Line().left().length(1).linewidth(1.75)
    slr.push()
    for i in range(3):
        slr += elm.Line().down().length(height).linewidth(1.75)
        slr += elm.Line().right().length(1).hold()
    slr += elm.Line().down().length(height).linewidth(1.75)
    slr += elm.Line().right().length(1).label('Изм.',"center", ofst=(0,-0.2)).linewidth(1.75).hold()
    slr += elm.Line().down().length(height).linewidth(1.75)
    slr += elm.Line().right().length(1).label('Разраб.',"center", ofst=(0,-0.2)).linewidth(1.75).hold()
    notations = [' ',' ', 'Нач. отд.', 'Н. контр.', 'ГИП',' ']
    for notation in notations:
        slr += elm.Line().down().length(height).linewidth(1.75)
        slr += elm.Line().right().length(2).label(notation,"center", ofst=(0,-0.2)).hold()
    slr.pop()

    
def small_left_frame(slr):
    width = 0.4
    height = 2.5
    notations = ['Инв. N подл.', 'Подпись и дата', 'Взам. инв. N']
    data = ['1', '2', '3']
    
    slr += elm.Line().left().length(width).linewidth(2)
    slr.push()
    for data in data:
        slr += elm.Line().up().length(height).label(data, ofst=(0,-0.75), rotate=90).linewidth(2)
        slr += elm.Line().right().length(width).hold().linewidth(2)
    slr.pop()
    
    slr += elm.Line().left().length(width).linewidth(2)
    for notation in notations:
        slr += elm.Line().up().length(height).label(notation,"center", ofst=(0,-0.2), rotate=90).linewidth(2)
        slr += elm.Line().right().length(width).hold().linewidth(2)


def all_frame(slr):
    slr += elm.Line().up().length(1)
    slr += elm.Line().up().length(1).hold()
    slr += (start_frame := elm.Line().right().length(52.75)).linewidth(2)
    slr += elm.Line().down().length(35.35).linewidth(2)
    slr.push()
    frame_legend(slr)
    slr.pop()
    slr += elm.Line().left().length(52.75).linewidth(2)
    slr.push()
    small_left_frame(slr)
    slr.pop()
    slr += elm.Line().up().length(35.35).linewidth(2)
    


schemdraw.config(fontsize = 10)
with schemdraw.Drawing(file=f'Data/Schemes/frame.svg', show=False, scale = 0.5, lw = 0.7, font = 'sans-serif') as slr:
    all_frame(slr)
        
