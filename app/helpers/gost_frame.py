import schemdraw.elements as elm

width_line = 1.5

def frame_legend(slr, data):
    width = 2.5
    height = 0.4
 
    slr += elm.Line().left().length(10)
    slr += elm.Line().up().length(height*3).linewidth(width_line)
    slr.push()
    slr += elm.Line().right().length(6).label(data['type_scheme'],"center", ofst=(0,-0.7), fontsize=10).linewidth(width_line).scale(0.5)
    slr += elm.Line().down().length(height*3).linewidth(width_line).hold()
    slr += elm.Line().right().length(4).linewidth(width_line)
    slr.pop()
    
    slr += elm.Line().up().length(height*3).linewidth(width_line)
    slr.push()
    slr += elm.Line().right().length(6).label('Основные технические решения',"center", ofst=(0,-1), fontsize=10).linewidth(width_line).scale(0.5)
    
    slr.push()
    slr += elm.Line().down().length(height).linewidth(width_line)
    slr += elm.Line().right().length(1.25).label('ОТР',"center", ofst=(0,-0.5), fontsize=10).linewidth(width_line).hold().scale(0.5)
    slr += elm.Line().down().length(height*2).linewidth(width_line)
    slr.pop()
    
    slr += elm.Line().right().length(1.25).label('Стадия',"center", ofst=(0,-0.2), fontsize=10).linewidth(width_line).scale(0.5)
    slr.push()
    slr += elm.Line().down().length(height).linewidth(width_line)
    slr += elm.Line().right().length(1.25).label('1',"center", ofst=(0,-0.5), fontsize=10).linewidth(width_line).hold().scale(0.5)
    slr += elm.Line().down().length(height*2).linewidth(width_line)
    slr.pop()
    
    slr += elm.Line().right().length(1.25).label('Лист',"center", ofst=(0,-0.2), fontsize=10).linewidth(width_line).scale(0.5)
    slr.push()
    slr += elm.Line().down().length(height).linewidth(width_line)
    slr += elm.Line().right().length(1.5).label(' ',"center", ofst=(0,-0.5), fontsize=10).linewidth(width_line).hold().scale(0.5)
    slr += elm.Line().down().length(height*2).linewidth(width_line)
    slr.pop()
    slr += elm.Line().right().length(1.5).label('Листов',"center", ofst=(0,-0.2), fontsize=10).linewidth(width_line).scale(0.5)
    slr.pop()
    
    slr += elm.Line().up().length(height*3).linewidth(width_line)
    slr += elm.Line().right().length(10).label(data['title_prjct'],"center", ofst=(0,-1), fontsize=10).linewidth(width_line).hold().scale(0.5)
    slr += elm.Line().up().length(height*2).linewidth(width_line)
    slr += elm.Line().right().length(10).label(data['code_prjct'],"center", ofst=(0,-0.5), fontsize=14).linewidth(width_line).hold().scale(0.5)
    
    #
    slr += elm.Line().left().length(1).linewidth(width_line)
    slr.push()
    for i in range(3):
        slr += elm.Line().down().length(height).linewidth(width_line)
        slr += elm.Line().right().length(1).hold()
    slr += elm.Line().down().length(height).linewidth(width_line)
    slr += elm.Line().right().length(1).label('Дата',"center", ofst=(0,-0.2), fontsize=10).linewidth(width_line).hold().scale(0.5)
    slr += elm.Line().down().length(height).linewidth(width_line)
    slr += elm.Line().right().length(1).linewidth(width_line).hold()
    for i in range(6):
        slr += elm.Line().down().length(height).linewidth(width_line)
        slr += elm.Line().right().length(1).hold()
    slr.pop()
    
    #
    slr += elm.Line().left().length(1.5).linewidth(width_line)
    slr.push()
    for i in range(3):
        slr += elm.Line().down().length(height).linewidth(width_line)
        slr += elm.Line().right().length(1.5).hold()
    slr += elm.Line().down().length(height).linewidth(width_line)
    slr += elm.Line().right().length(1.5).label('Подпись',"center", ofst=(0,-0.2), fontsize=10).linewidth(width_line).hold().scale(0.5)
    slr += elm.Line().down().length(height).linewidth(width_line)
    slr += elm.Line().right().length(1.5).linewidth(width_line).hold()
    for i in range(6):
        slr += elm.Line().down().length(height).linewidth(width_line)
        slr += elm.Line().right().length(1.5).hold()
    slr.pop()
    
    #
    slr += elm.Line().left().length(1.25).linewidth(width_line)
    slr.push()
    for i in range(3):
        slr += elm.Line().down().length(height).linewidth(width_line)
        slr += elm.Line().right().length(1.25).hold()
    slr += elm.Line().down().length(height).linewidth(width_line)
    slr += elm.Line().right().length(1.25).label('N. док.',"center", ofst=(0,-0.2), fontsize=10).linewidth(width_line).hold().scale(0.5)
    slr += elm.Line().down().length(height).linewidth(width_line)
    slr += elm.Line().right().length(1.25).linewidth(width_line).hold()
    slr.pop()
    
    slr += elm.Line().left().length(1).linewidth(width_line)
    slr.push()
    for i in range(3):
        slr += elm.Line().down().length(height).linewidth(width_line)
        slr += elm.Line().right().length(1).hold()
    slr += elm.Line().down().length(height).linewidth(width_line)
    slr += elm.Line().right().length(1).label('Лист',"center", ofst=(0,-0.2), fontsize=10).linewidth(width_line).hold().scale(0.5)
    slr += elm.Line().down().length(height).linewidth(width_line)
    slr += elm.Line().right().length(1).linewidth(width_line).hold()
    for i in range(6):
        slr += elm.Line().down().length(height).linewidth(width_line)
        slr += elm.Line().right().length(2.25).hold()
    slr.pop()
    
    #
    slr += elm.Line().left().length(1.25).linewidth(width_line)
    slr.push()
    for i in range(3):
        slr += elm.Line().down().length(height).linewidth(width_line)
        slr += elm.Line().right().length(1.25).hold()
    slr += elm.Line().down().length(height).linewidth(width_line)
    slr += elm.Line().right().length(1.25).label('Кол. уч.',"center", ofst=(0,-0.2), fontsize=10).linewidth(width_line).hold().scale(0.5)
    slr += elm.Line().down().length(height).linewidth(width_line)
    slr += elm.Line().right().length(1.25).linewidth(width_line).hold()
    slr.pop()
    
    slr += elm.Line().left().length(1).linewidth(width_line)
    slr.push()
    for i in range(3):
        slr += elm.Line().down().length(height).linewidth(width_line)
        slr += elm.Line().right().length(1).hold()
    slr += elm.Line().down().length(height).linewidth(width_line)
    slr += elm.Line().right().length(1).label('Изм.',"center", ofst=(0,-0.2), fontsize=10).linewidth(width_line).hold().scale(0.5)
    slr += elm.Line().down().length(height).linewidth(width_line)
    slr += elm.Line().right().length(1).label('Разраб.',"center", ofst=(1.25,-0.2), fontsize=10).linewidth(width_line).hold().scale(0.5)
    notations = [' ',' ', 'Нач. отд.', 'Н. контр.', 'ГИП',' ']
    for notation in notations:
        slr += elm.Line().down().length(height).linewidth(width_line)
        slr += elm.Line().right().length(2.25).label(notation,"center", ofst=(0,-0.2), fontsize=10).hold().scale(0.5)
    slr.pop()
  
def small_left_frame(slr):
    width = 0.4
    height = 2.75
    notations = ['Инв. N подл.', 'Подпись и дата', 'Взам. инв. N']
    data = [' ', ' ', ' ']
    
    slr += elm.Line().left().length(width*1.5).linewidth(width_line)
    slr.push()
    for data in data:
        slr += elm.Line().up().length(height).label(data, ofst=(0,-1), rotate=90, fontsize=10).linewidth(width_line).scale(0.5)
        slr += elm.Line().right().length(width*1.5).hold().linewidth(width_line)
    slr.pop()
    
    slr += elm.Line().left().length(width).linewidth(width_line)
    for notation in notations:
        slr += elm.Line().up().length(height).label(notation,"center", ofst=(0,-0.1), rotate=90, fontsize=10).linewidth(width_line).scale(0.5)
        slr += elm.Line().right().length(width).hold().linewidth(width_line)

def frame_legend_for_structural(slr, data):
    slr += elm.Line().up().length(0.4*12.5).linewidth(width_line)
    colors = ['orange', 'black', 'green']
    titles_line = [' Кабель переменного тока', ' Кабель постоянного тока', ' Кабель связи']
    if data['controller'] == True:
        colors.append('blue')
        titles_line.append(' Контрольный кабель')
    for clr, ttl in zip(colors, titles_line):
        slr += elm.Line().up().length(0.5).linewidth(width_line)
        slr.push()
        slr += elm.Line().left().length(5.7).linewidth(width_line).color('white').zorder(-1)
        slr += (left_side := elm.Line().down().length(0.4*2).linewidth(width_line).color('white').zorder(-1))
        slr += elm.Line().right().at(left_side.center, dx = 0.3).length(0.6).linewidth(2).color(clr).label(ttl,"right", ofst=(0.4, 0), color = 'black', fontsize=10).scale(0.5)
        slr.pop()

def all_frame(slr, **data):  
    slr += elm.Line().up().length(1).color('white')
    slr += elm.Line().up().length(0.5).hold().color('white')
    slr += elm.Line().right().length(data['width']).linewidth(1.75)
    slr += elm.Line().down().length(data['height']).linewidth(1.75)
    slr.push()
    frame_legend(slr, data)
    slr.pop()
    if data['type_scheme'] == 'Структурная схема подключения СЭС':
        slr.push()
        frame_legend_for_structural(slr, data)
        slr.pop()
    slr += elm.Line().left().length(data['width']).linewidth(1.75)
    slr.push()
    small_left_frame(slr)
    slr.pop()
    slr += elm.Line().up().length(data['height']).linewidth(1.75)
    
        
