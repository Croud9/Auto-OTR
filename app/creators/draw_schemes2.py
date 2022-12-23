import os 
import schemdraw
import schemdraw.elements as elm
from os.path import isfile, join
from helpers import gost_frame, encode_file
scale_coff = 0.65

def closer(slr):
    slr += elm.Line().left().length(scale_coff*0.125)
    slr += elm.Line().up().length(scale_coff*0.05)
    slr += elm.Line().down().length(scale_coff*0.45)
    slr += elm.Line().up().length(scale_coff*0.05)
    slr += elm.Line().right().length(scale_coff*0.125)

def draw_frame_module(slr, params):
    slr += (block_top := elm.Line().right().length(scale_coff*5))
    slr += elm.Line().left().length(scale_coff*5)

    for i in range(3):
        slr += elm.Line().down().length(scale_coff*1)
        slr += elm.Line().right().length(scale_coff*5).label(params[i], ofst=(0, 0.75))
        slr += elm.Line().left().length(scale_coff*5)

    slr += elm.Line().down().length(scale_coff*1.5)
    slr += (right_17 :=elm.Line().right().length(scale_coff*5))
    slr += elm.Label().at(right_17.center).label(params[3], ofst=(0,2))
    slr += elm.Label().at(right_17.center).label(params[4], ofst=(0,1))
    slr += elm.Line().up().length(scale_coff*4.5)

    return block_top

def draw_color_line(slr, switch_or_line, names):
    slr += (antenna := elm.Antenna())
    slr += (antenna_end := elm.Line().up().at(antenna.end, dy=0.45).length(scale_coff*0.01))

    slr += (bottom_blue_line := elm.Line().up().at(antenna_end.end, dy=0.5, dx=1).length(scale_coff*0.5).color('blue'))
    slr += elm.Label().at(bottom_blue_line.start).label(names[2], loc="bottom", ofst=(3,-0.5))
    slr += elm.Label().at(bottom_blue_line.start).label(names[3], loc="bottom", ofst=(2.25,-0.5))
    slr += elm.Label().at(bottom_blue_line.start).label('', loc="bottom", ofst=(1.5,-0.5))
    slr += elm.Label().at(bottom_blue_line.start).label('', loc="bottom", ofst=(0.75,-0.5))
    slr += elm.Line().endpoints(antenna_end.end, bottom_blue_line.start).color('blue')
    if switch_or_line[0] == True:
        slr += (bottom_black_line := elm.Line().up().at(antenna_end.end, dy=0.5, dx=0.6).dot().length(scale_coff*2.01).color('black')).linestyle('--')
        slr += elm.Line().endpoints(antenna_end.end, bottom_black_line.start).color('black').linestyle('--')

    if switch_or_line[1][0] == False:
        slr += elm.Line().up().at(bottom_blue_line.end).length(scale_coff*1.75).dot().color('blue')
    else:
        slr += elm.Switch().up().at(bottom_blue_line.end).length(scale_coff*1)
        slr += elm.Line().up().length(scale_coff*0.9).dot().color('blue')

    if switch_or_line[2][0] == True and switch_or_line[2][1] == True:
        slr += (bottom_red_line := elm.Line().up().at(antenna_end.end, dy=0.5, dx=0.25).length(scale_coff*0.5).color('red'))
        slr += elm.Line().endpoints(antenna_end.end, bottom_red_line.start).color('red')
        slr += elm.Switch().up().at(bottom_red_line.end).length(scale_coff*1)
        slr += elm.Line().up().length(scale_coff*1.28).dot().color('red')
    elif switch_or_line[2][0] == False and switch_or_line[2][1] == True:
        slr += (bottom_red_line := elm.Line().up().at(antenna_end.end, dy=0.5, dx=0.25).length(scale_coff*2.5).color('red').dot())
        slr += elm.Line().endpoints(antenna_end.end, bottom_red_line.start).color('red')

    if switch_or_line[3][0] == True and switch_or_line[3][1] == True:
        slr += (bottom_green_line := elm.Line().up().at(antenna_end.end, dy=0.5, dx=-0.25).length(scale_coff*0.5).color('lightgreen'))
        slr += elm.Line().endpoints(antenna_end.end, bottom_green_line.start).color('lightgreen')
        slr += elm.Switch().up().at(bottom_green_line.end).length(scale_coff*1)
        slr += elm.Line().up().length(scale_coff*1.65).dot().color('lightgreen')
    elif switch_or_line[3][0] == False and switch_or_line[3][1] == True:
        slr += (bottom_green_line := elm.Line().up().at(antenna_end.end, dy=0.5, dx=-0.25).length(scale_coff*2.75).color('lightgreen').dot())
        slr += elm.Line().endpoints(antenna_end.end, bottom_green_line.start).color('lightgreen')

    if switch_or_line[4][0] == True and switch_or_line[4][1] == True:
        slr += (bottom_yellow_line := elm.Line().up().at(antenna_end.end, dy=0.5, dx=-0.75).length(scale_coff*0.5).color('yellow'))
        slr += elm.Line().endpoints(antenna_end.end, bottom_yellow_line.start).color('yellow')
        slr += elm.Switch().up().at(bottom_yellow_line.end).length(scale_coff*1)
        slr += elm.Line().up().length(scale_coff*2.05).dot().color('yellow')
    elif switch_or_line[4][0] == False and switch_or_line[4][1] == True:
        slr += (bottom_yellow_line := elm.Line().up().at(antenna_end.end, dy=0.5, dx=-0.75).length(scale_coff*3).color('yellow').dot())
        slr += elm.Line().endpoints(antenna_end.end, bottom_yellow_line.start).color('yellow')

def draw_invertor(slr, params, names, switch_or_line, repeat):
    block_top = draw_frame_module(slr, params)

    slr += elm.Line().up().at(block_top.center, dx = -0.3).length(scale_coff*0.25).color('white').zorder(-1)

    slr += elm.Line().up().length(scale_coff*1)
    slr += ( box_top := elm.Line().right().length(scale_coff*1))
    slr += elm.Label().at(box_top.center, dx = -0.15).label('~', ofst=(0,-0.8))
    slr += elm.Line().down().length(scale_coff*1)
    slr += ( box_bot := elm.Line().left().length(scale_coff*1))
    slr += elm.Label().at(box_bot.center, dx = 0.15).label('-', ofst=(0, -0.5) )
    slr += elm.Line().endpoints(box_top.end, box_bot.end)

    slr += (connect_antenna := elm.Line().up().at(box_top.center).length(scale_coff*3.5))
    slr += elm.Label().at(connect_antenna.center).label('', ofst=(0,1.2), rotate = 90)
    slr += elm.Label().at(connect_antenna.center).label(names[0], ofst=(0,0.6), rotate = 90)
    slr += elm.Label().at(connect_antenna.center).label(names[1], ofst=(0,-0.6), rotate = 90).color('red')
    if repeat == True:
        slr.push()
        dot_x = 1.1
        slr += elm.Dot().at(connect_antenna.center, dx = dot_x)
        slr += elm.Dot().at(connect_antenna.center, dx = dot_x + 0.5)
        slr += elm.Dot().at(connect_antenna.center, dx = dot_x + 1)
        slr.pop()

    draw_color_line(slr, switch_or_line, names)

def custom_module(slr, params, names, switch_or_line):
    block_top = draw_frame_module(slr, params)

    slr += elm.Line().up().at(block_top.center, dx = -1).length(scale_coff*0.25).color('white').zorder(-1)
    slr += elm.Line().up().length(scale_coff*1)
    slr += ( box_top := elm.Line().right().length(scale_coff*3))
    slr += elm.Line().down().length(scale_coff*1)
    slr += elm.Line().left().length(scale_coff*3)

    slr += (connect_antenna := elm.Line().up().at(box_top.center).length(scale_coff*3.5))
    slr += elm.Label().at(connect_antenna.center).label('', ofst=(0,1.2), rotate = 90)
    slr += elm.Label().at(connect_antenna.center).label(names[0], ofst=(0,0.6), rotate = 90)
    slr += elm.Label().at(connect_antenna.center).label(names[1], ofst=(0,-0.6), rotate = 90).color('red')

    draw_color_line(slr, switch_or_line, names)

def grounding_module(slr, names, switch_or_line):
    slr += (block_top := elm.Line().right().length(scale_coff*5).color('white'))
    slr += ( white_line := elm.Line().up().at(block_top.center).length(scale_coff*2.5).color('white'))

    slr += elm.Ground()
    slr += elm.Thermistor().flip().label(names[2], loc='bottom').length(scale_coff*2.5)
    slr += elm.Line().up().at(white_line.end).length(scale_coff*2.25)

    draw_color_line(slr, switch_or_line, names)

def general_line(slr, three_phase):
    slr.push()
    slr.here = (3.7, -6.4)
    slr += (start_all_general_line := elm.Line().right().length(scale_coff*0.5).color('white'))
    slr += (start_yellow := elm.Line().right().at(start_all_general_line.start, dy = -1).length(scale_coff*0.5).color('yellow')).label("L1", loc="left", color="black")
    slr += (start_blue := elm.Line().right().at(start_all_general_line.start, dy = -1.75).length(scale_coff*0.5).color('blue')).label("N", loc="left", color="black")
    slr += (start_black := elm.Line().right().at(start_all_general_line.start, dy = -2).length(scale_coff*0.5)).label("PE", loc="left", color="black").linestyle('--')

    slr.pop()# Правый конец
    slr += (end_white_general_line := elm.Line().right().length(scale_coff*0.15).color('white'))
    slr += (general_blue_line := elm.Line().right().at(end_white_general_line.end, dy=-1.75).length(scale_coff*1).color('blue'))
    slr += (black_ground := elm.Line().right().at(general_blue_line.end, dy = -0.25).length(scale_coff*0.25).linestyle('--'))
    slr += elm.Ground()
    slr += (general_yellow_line := elm.Line().right().at(general_blue_line.start, dy=0.75).length(scale_coff*1).color('yellow'))
    
    slr += elm.Line().endpoints(general_blue_line.start, start_blue.end).color("blue")
    slr += elm.Line().endpoints(general_yellow_line.start, start_yellow.end).color("yellow")
    slr += elm.Line().endpoints(black_ground.start, start_black.end).linestyle('--')

    if three_phase == True:
        slr.push()
        slr.here = (6, -7.15)
        slr += (start_green := elm.Line().right().at(start_all_general_line.start, dy = -1.25).length(scale_coff*0.5).color('lightgreen')).label("L2", loc="left", color="black")
        slr += (start_red := elm.Line().right().at(start_all_general_line.start, dy = -1.5).length(scale_coff*0.5).color('red')).label("L3", loc="left", color="black")
        
        slr.pop() # Правый конец
        slr += (general_red_line := elm.Line().at(general_blue_line.start, dy=0.25).right().length(scale_coff*1).color('red'))
        slr += (general_green_line := elm.Line().at(general_blue_line.start, dy=0.5).right().length(scale_coff*1).color('lightgreen'))
        slr += elm.Line().endpoints(general_red_line.start, start_red.end).color("red")
        slr += elm.Line().endpoints(general_green_line.start, start_green.end).color("lightgreen")

def generate_frame(slr):
    slr += (main_top :=elm.Line().right().length(scale_coff*5))
    slr += elm.Label().at(main_top.center).label('Обозначение - марка и', ofst=(0,-3.5))
    slr += elm.Label().at(main_top.center).label('сечение проводника', ofst=(0,-4.5))
    slr +=  elm.Line().down().length(scale_coff*4)
    slr +=  elm.Line().left().length(scale_coff*2.5)
    slr.push()

    names_main_frame = ['Обозначение', 'Тип', 'Ном. ток, А', 'Тип \n расцепителя', 'Обозначение', 'Тип', 'Ном. ток, А', 'Хар-ка \n срабатывания']
    for i in names_main_frame:
        y_ofst = 0.6
        if '\n' in i:
            y_ofst = 0.3
        slr += elm.Line().down().length(scale_coff*1)
        slr += elm.Line().right().length(scale_coff*2.5).label(i, ofst=(0, y_ofst))
        slr += elm.Line().left().length(scale_coff*2.5)

    slr += elm.Line().right().length(scale_coff*2.5)
    slr += elm.Line().up().length(scale_coff*8)

    slr.pop()
    slr += (left_top_1 := elm.Line().left().length(scale_coff*2.5))
    slr += elm.Label().at(left_top_1.center).label('Аппарат', ofst=(0,3.5))
    slr += elm.Label().at(left_top_1.center).label('на вводе', ofst=(0,4.5))
    slr += elm.Line().down().length(scale_coff*4)
    slr += elm.Line().right().length(scale_coff*2.5)
    slr += elm.Line().down().length(scale_coff*4)
    slr += (left_top_2 := elm.Line().left().length(scale_coff*2.5))
    slr += elm.Label().at(left_top_2.center).label('Аппарат', ofst=(0,-4.5))
    slr += elm.Label().at(left_top_2.center).label('отходящ.', ofst=(0,-3.5))
    slr += elm.Label().at(left_top_2.center).label('линии', ofst=(0,-2.5))
    slr += elm.Line().up().length(scale_coff*12)
    slr += elm.Line().left().length(scale_coff*0.5)
    slr += (left_side_1 := elm.Line().down().length(scale_coff*4))
    slr += elm.Label().at(left_side_1.center).label('Кабельная линия', ofst=(0,0.3), rotate=90)
    slr += elm.Line().right().length(scale_coff*0.5)
    slr += elm.Line().left().length(scale_coff*0.5)
    slr += (left_side_2 := elm.Line().down().length(scale_coff*8))
    slr += elm.Label().at(left_side_2.center).label('Щит распределительный 0,4 кВ', ofst=(0,0.3), rotate=90)
    slr += elm.Line().right().length(scale_coff*0.5)
    slr += elm.Line().left().length(scale_coff*0.5)
    slr += (left_side_3 := elm.Line().down().length(scale_coff*4))
    slr += elm.Label().at(left_side_3.center).label('Кабельная линия', ofst=(0,0.3), rotate=90)
    slr += elm.Line().right().length(scale_coff*0.5)
    slr += elm.Line().left().length(scale_coff*0.5)
    slr += (left_side_4 := elm.Line().down().length(scale_coff*6))
    slr += elm.Label().at(left_side_4.center).label('Эл. приемник', ofst=(0,0.3), rotate=90)
    slr += elm.Line().right().length(scale_coff*0.5)
    slr += (left_side_4 := elm.Line().up().length(scale_coff*10))

    slr += (second_top := elm.Line().right().length(scale_coff*5))
    slr += elm.Label().at(second_top.center).label('Обозначение - марка и', ofst=(0,-3.5))
    slr += elm.Label().at(second_top.center).label('сечение проводника', ofst=(0,-4.5))
    slr += elm.Line().down().length(scale_coff*4)
    slr += elm.Line().left().length(scale_coff*5)

    slr += elm.Line().down().length(scale_coff*1.5)
    slr += (right_9 :=elm.Line().right().length(scale_coff*5))
    slr += elm.Label().at(right_9.center).label('Условное графическое', ofst=(0,2))
    slr += elm.Label().at(right_9.center).label('обозначение', ofst=(0,1))
    slr += elm.Line().left().length(scale_coff*5)

    slr += elm.Line().down().length(scale_coff*1)
    slr += (right_10 :=elm.Line().right().length(scale_coff*5))
    slr += elm.Label().at(right_10.center).label('Номер по плану', ofst=(0, 1))
    slr += elm.Line().left().length(scale_coff*5)

    slr += elm.Line().down().length(scale_coff*1)
    slr += (right_11 :=elm.Line().right().length(scale_coff*5))
    slr += elm.Label().at(right_11.center).label('Pнам, кВт', ofst=(0, 1))
    slr += elm.Line().left().length(scale_coff*5)

    slr += elm.Line().down().length(scale_coff*1)
    slr += (right_12 :=elm.Line().right().length(scale_coff*5))
    slr += elm.Label().at(right_12.center).label('Iрасч, А', ofst=(0, 1))
    slr += elm.Line().left().length(scale_coff*5)

    slr += elm.Line().down().length(scale_coff*1.5)
    slr += (right_13 :=elm.Line().right().length(scale_coff*5))
    slr += elm.Label().at(right_13.center).label('Наименование', ofst=(0, 1.5))

    slr += elm.Line().up().length(scale_coff*6)
    slr += elm.Line().down().length(scale_coff*1.5)

def little_frame(slr):
    slr += elm.Line().up().length(scale_coff*0.35)
    slr += elm.Line().left().length(scale_coff*0.625)
    slr += elm.Line().down().length(scale_coff*0.175)
    slr += elm.Line().down().length(scale_coff*0.35)

def top_counter(slr, three_phase, counter, names):
    kraja = 0.625
    slr.here = (5.75, -7.15)
    slr += (start_all_general_line := elm.Line().right().length(scale_coff*0.625).color("white"))
    slr += elm.Dot().at(start_all_general_line.end, dy=-1.25, dx=0.75)
    slr += elm.Dot().at(start_all_general_line.end, dy=-1, dx=0.5).color('blue')
    slr += elm.Dot().at(start_all_general_line.end, dy=-0.25, dx=-1).color('yellow')
    
    slr += (bottom_black_line := elm.Line().up().at(start_all_general_line.end, dy=-1.25, dx=0.75).length(scale_coff*0.5 + 6).color('black').linestyle('--'))
    slr += (bottom_blue_line := elm.Line().up().at(start_all_general_line.end, dy=-1, dx=0.5).length(scale_coff*0.25 + 6).color('blue'))
    slr += (bottom_yellow_line := elm.Line().up().at(start_all_general_line.end, dy=-0.25, dx=-1).length(scale_coff*0.25 + 4).color('yellow'))

    slr += elm.Switch().at(bottom_yellow_line.end).length(scale_coff*1)
    slr += (top_yellow_line := elm.Line().up().length(scale_coff*1).color('yellow'))

    slr += (antenna := elm.Antenna().flip().at(bottom_blue_line.end, dy=1, dx=-0.5).color("gray"))
    slr += (antenna_end := elm.Line().up().at(antenna.end, dy=-0.45).length(scale_coff*0.05))
    slr += elm.Line().endpoints(antenna_end.end, bottom_blue_line.end).color('blue')
    slr += elm.Line().endpoints(antenna_end.end, top_yellow_line.end).color('yellow')
    slr += elm.Line().endpoints(antenna_end.end, bottom_black_line.end).color('black').linestyle('--')
    slr += (last_line := elm.Line().up().at(antenna.end).length(scale_coff*5).color("gray"))
    slr += elm.Label().at(last_line.center).label('', ofst=(0,2), rotate = 90)
    slr += elm.Label().at(last_line.center).label(names[0], ofst=(0,1.4), rotate = 90)
    slr += elm.Label().at(last_line.center).label(names[1], ofst=(0,0.6), rotate = 90)
    slr += elm.Label().at(last_line.center).label(names[2], ofst=(0,-0.6), rotate = 90).color('red')
    slr += elm.Label().at(last_line.center).label(names[3], ofst=(5.5, 0))

    if three_phase == True:
        slr += elm.Dot().at(start_all_general_line.end, dy=-0.75, dx=0).color('red')
        slr += elm.Dot().at(start_all_general_line.end, dy=-0.5, dx=-0.5).color('lightgreen')
        slr += (bottom_red_line := elm.Line().up().at(start_all_general_line.end, dy=-0.75, dx=0).length(scale_coff*0.625 + 4).color('red'))
        slr += (bottom_green_line := elm.Line().up().at(start_all_general_line.end, dy=-0.5, dx=-0.5).length(scale_coff*0.5 + 4).color('lightgreen'))
        slr += elm.Switch().at(bottom_red_line.end).length(scale_coff*1)
        slr += (top_red_line := elm.Line().up().length(scale_coff*1).color('red'))
        slr += elm.Switch().at(bottom_green_line.end).length(scale_coff*1)
        slr += (top_green_line := elm.Line().up().length(scale_coff*1).color('lightgreen'))
        slr += elm.Line().endpoints(antenna_end.end, top_red_line.end).color('red')
        slr += elm.Line().endpoints(antenna_end.end, top_green_line.end).color('lightgreen')

    if counter == True:
        slr += elm.Dot().at(bottom_yellow_line.end, dy=-0.73).color('yellow')
        slr += elm.Line().right().at(bottom_yellow_line.end, dy=-0.73).length(scale_coff*2.998).color('yellow')
        slr += elm.Switch().reverse().length(scale_coff*1)
        slr += elm.Line().right().length(scale_coff*1.31).color('yellow')
        slr += elm.Line().down().length(scale_coff*0.175)
        slr += elm.Line().right().length(scale_coff*kraja).label('2', "center", color='black', ofst=(0,0.55))
        slr += elm.Line().up().length(scale_coff*0.35)
        slr += elm.Line().left().length(scale_coff*kraja)
        slr += elm.Line().down().length(scale_coff*0.5)

        if three_phase == True:
            slr += elm.Dot().at(bottom_green_line.end, dy=-0.98).color('lightgreen')
            slr += elm.Line().right().at(bottom_green_line.end, dy=-0.98).length(scale_coff*2.229).color('lightgreen')
            slr += elm.Switch().reverse().length(scale_coff*1)
            slr += elm.Line().right().length(scale_coff*1.31).color('lightgreen')
            slr += elm.Line().down().length(scale_coff*0.175)
            slr += elm.Line().right().length(scale_coff*kraja).label('5', "center", color='black', ofst=(0,0.55))
            slr += elm.Line().up().length(scale_coff*0.35)
            slr += elm.Line().left().length(scale_coff*kraja)
            slr += elm.Line().down().length(scale_coff*0.5)

            slr += elm.Dot().at(bottom_red_line.end, dy=-1.15).color('red')
            slr += elm.Line().right().at(bottom_red_line.end, dy=-1.15).length(scale_coff*1.46).color('red')
            slr += elm.Switch().reverse().length(scale_coff*1)
            slr += elm.Line().right().length(scale_coff*1.31).color('red')
            slr += elm.Line().down().length(scale_coff*0.175)
            slr += elm.Line().right().length(scale_coff*kraja).label('8', "center", color='black', ofst=(0,0.55))
            slr += elm.Line().up().length(scale_coff*0.35)
            slr += elm.Line().left().length(scale_coff*kraja)
            slr += elm.Line().down().length(scale_coff*0.5)
        else:
            slr += elm.Line().down().length(scale_coff*1)
        # начало построения счетчика
        slr += elm.Dot().at(bottom_blue_line.end, dy=-3).color('blue')
        slr += elm.Line().right().at(bottom_blue_line.end, dy=-3).length(scale_coff*3).color('blue')
        slr += elm.Line().down().length(scale_coff*0.175)
        slr += elm.Line().right().length(scale_coff*kraja).label('10', "center", color='black', ofst=(0,0.55))
        slr += elm.Line().up().length(scale_coff*0.35)
        slr += elm.Line().left().length(scale_coff*kraja)
        slr += elm.Line().down().length(scale_coff*0.5)
        slr += elm.Line().down().length(scale_coff*0.5)
        slr += (little_frame_one := elm.Line().down().length(scale_coff*0.175))
        slr += elm.Line().right().length(scale_coff*kraja).label('1', "center", color='black', ofst=(0,0.55))
        little_frame(slr)
        slr += (little_frame_two := elm.Line().down().length(scale_coff*0.175))
        slr += elm.Line().right().length(scale_coff*kraja).label('3', "center", color='black', ofst=(0,0.55))
        little_frame(slr)

        if three_phase == False:
            slr.push()
            slr += elm.Line().left().length(scale_coff*4.25).dot(open = True).at(little_frame_one.start)
            closer(slr)
            slr += elm.Line().left().length(scale_coff*4.25).dot(open = True).at(little_frame_two.start)
            slr += elm.Ground()
            slr.pop()
            slr += elm.Line().down().length(scale_coff*1.4)
        else:
            slr += (little_frame_three := elm.Line().down().length(scale_coff*0.175))
            slr += elm.Line().right().length(scale_coff*kraja).label('4', "center", color='black', ofst=(0,0.55))
            little_frame(slr)
            slr += (little_frame_four := elm.Line().down().length(scale_coff*0.175))
            slr += elm.Line().right().length(scale_coff*kraja).label('6', "center", color='black', ofst=(0,0.55))
            little_frame(slr)
            slr += (little_frame_five := elm.Line().down().length(scale_coff*0.175))
            slr += elm.Line().right().length(scale_coff*kraja).label('7', "center", color='black', ofst=(0,0.55))
            little_frame(slr)
            slr += (little_frame_six := elm.Line().down().length(scale_coff*0.175))
            slr += elm.Line().right().length(scale_coff*kraja).label('9', "center", color='black', ofst=(0,0.55))
            little_frame(slr)
            slr.push()
            slr += elm.Line().left().length(scale_coff*5).dot(open = True).at(little_frame_one.start)
            closer(slr)
            slr += elm.Line().left().length(scale_coff*5).dot(open = True).at(little_frame_two.start)
            slr += elm.Ground()
            slr += elm.Line().left().length(scale_coff*4.2).dot(open = True).at(little_frame_three.start)
            closer(slr)
            slr += elm.Dot().at(little_frame_four.start, dx=-1.465)
            slr += elm.Line().left().length(scale_coff*1.95).dot(open = True).at(little_frame_four.start, dx=-1.465)
            slr += elm.Ground()
            slr += elm.Line().left().length(scale_coff*3.5).dot(open = True).at(little_frame_five.start)
            closer(slr)
            slr += (little_frame_left_line := elm.Line().left().length(scale_coff*1.25).dot(open = True).at(little_frame_six.start, dx=-1.465))
            slr += elm.Ground()
            slr += elm.Line().up().length(scale_coff*1.4).dot().at(little_frame_left_line.start)
            slr += elm.Line().length(scale_coff*0.35).at(little_frame_six.start).theta(130).color('purple')
            slr += elm.Line().up().length(scale_coff*0.15).color('purple')
            slr += elm.Line().length(scale_coff*0.35).at(little_frame_four.start).theta(130).color('purple')
            slr += elm.Line().up().length(scale_coff*0.15).color('purple')
            slr += elm.Line().length(scale_coff*0.35).at(little_frame_four.start).theta(230).color('purple')
            slr += elm.Line().length(scale_coff*0.35).at(little_frame_two.start).theta(230).color('purple')
            slr.pop()

        slr += elm.Line().right().length(scale_coff*5)
        slr += elm.Line().up().length(scale_coff*5)
        slr += elm.Line().left().length(scale_coff*5)
        slr += elm.Line().down().length(scale_coff*0.5)
        slr += elm.Line().up().length(scale_coff*2)
        slr += elm.Line().right().length(scale_coff*5).label("Wh \n Счетчик э/э двунаправленный", "center", ofst=(0,-1))
        slr += elm.Line().down().length(scale_coff*1.5)

def draw(data, gost_frame_params):
    schemdraw.config(fontsize = 7.2)

    fp_general = 'Data/Schemes/General/'
    files_in_general = [f for f in os.listdir(fp_general) if isfile(join(fp_general, f))]
    if len(files_in_general) != 0:
        for file in files_in_general:
            os.remove(fp_general + f"/{file}")  

    with schemdraw.Drawing(file=f'Data/Schemes/General/connect_system.svg', show = False, scale = 0.35, lw = 0.6) as slr:
        module_offset = 3.25 # начало чертежа модулей
        count_all_modules = 0
        counter = data['use_counter'] 
        three_phase = data['use_threePhase'] 
        slr.here = (0, -2.375)
        generate_frame(slr) # левая рамка
        names = [data['brand_cable_out'], data['cable_out'], data['length_cable_out'], data['type_param_out']]
        top_counter(slr, three_phase, counter, names) # Верхний счетчик

        all_invertors = []
        all_others = []

        for key in data.keys():
            if 'found_invertor' in key:
                all_invertors.append(key)
            elif 'found_other' in key:
                all_others.append(key)

        num_device = 0
        for current in all_invertors:
            num_device  += 1
            invertor = data[current]
            count_inv = int(invertor['count_invertor'])
            repeat = False
            if count_inv >= 8:
                count_all_inv = count_inv
                count_inv = 2
                repeat = True
            count_all_modules += count_inv
            for i in range(1, count_inv + 1):
                if repeat == True and i == 2:
                    i = count_all_inv
                    repeat = False
                if three_phase == False:
                    phase2 = False
                    phase3 = False
                else:
                    phase2 = invertor['red_line_inv']
                    phase3 = invertor['green_line_inv']

                yellow_switch_and_line = [invertor['yellow_switch_inv'], invertor['yellow_line_inv']] #l1
                red_switch_and_line = [invertor['red_switch_inv'], phase2] #L2
                blue_switch_and_line = [invertor['blue_switch_inv'], invertor['blue_line_inv']] #ноль
                green_switch_and_line = [invertor['green_switch_inv'], phase3] #L3
                black_line = invertor['black_line_inv'] #земля
                switch_or_line = [black_line, blue_switch_and_line, red_switch_and_line, green_switch_and_line, yellow_switch_and_line]

                slr.here = (module_offset, -13.75)
                params = [f"Инвертор {num_device }.{i}", invertor['p_max'], invertor['i_out_max'], "Инвертор", invertor['module']]
                names = [invertor['brand_cable_inv'], invertor['length_cable_inv'], f"{invertor['type_inv']}", invertor['i_nom_inv']]

                draw_invertor(slr, params, names, switch_or_line, repeat) # инвертор
                module_offset += 3.25

        for current in all_others:
            if data[current] != {}:
                num_device += 1
                custom = data[current]
                count_all_modules += int(custom['count_other'])
                for i in range(custom['count_other']):
                    if three_phase == False:
                        phase2 = False
                        phase3 = False
                    else:
                        phase2 = custom['red_line_other']
                        phase3 = custom['green_line_other']

                    yellow_switch_and_line = [custom['yellow_switch_other'], custom['yellow_line_other']] #l1
                    red_switch_and_line = [custom['red_switch_other'], phase2] #L2
                    blue_switch_and_line = [custom['blue_switch_other'], custom['blue_line_other']] #ноль
                    green_switch_and_line = [custom['green_switch_other'], phase3] #L3
                    black_line = custom['black_line_other'] #земля
                    switch_or_line = [black_line, blue_switch_and_line, red_switch_and_line, green_switch_and_line, yellow_switch_and_line]

                    slr.here = (module_offset, -13.75)
                    params = [f"{custom['type_other']} {num_device}.{i+1}", custom['power_other'], custom['i_other'], f"{custom['type_other']}", custom['title_other']]
                    names = [custom['brand_cable_other'], custom['length_cable_other'], f"{custom['type_param_other']}", custom['i_nom_other']]

                    custom_module(slr, params, names, switch_or_line) # изменяемый моудуль
                    module_offset += 3.25

        if data['use_yzip'] == True:
            if three_phase == False:
                phase2 = False
                phase3 = False
            else:
                phase2 = True
                phase3 = True

            slr.here = (module_offset, -13.75)
            black_switch_and_line = False #земля
            blue_switch_and_line = [True, True] #ноль
            red_switch_and_line = [True, phase2] #L2
            green_switch_and_line = [True, phase3] #L3
            yellow_switch_and_line = [True, True] #l1
            switch_or_line = [black_switch_and_line, blue_switch_and_line, red_switch_and_line, green_switch_and_line, yellow_switch_and_line]
            names = ['', data['brand_cable_yzip'], data['type_param_yzip'], data['i_nom_yzip']]
            grounding_module(slr, names, switch_or_line) # ВЗаземление
            module_offset += 3.25

        slr.here = (module_offset, -6.4)
        general_line(slr, three_phase)
        width = 34.65 if count_all_modules <= 8 else 34.65 + ((count_all_modules - 8) * 3.25)
        height = 24.84 #1см = 0.875
        slr.here = (-1, 2.5)
        data = {'width': width, 'height': height, 'title_prjct': gost_frame_params['title_project'],
                'code_prjct': gost_frame_params['code_project'], 'controller': False, 'type_scheme': 'Cхема электрическая \n принципиальная'}
        gost_frame.all_frame(slr, **data)
    srcfile = 'Data/Schemes/General/connect_system.svg'
    trgfile = 'Data/Schemes/General/connect_system_codec.svg'
    encode_file.to_utf8(srcfile, trgfile)

# gost_frame_params = {'title_project': 'ШЛЮМБЕРЖЕ. ЛИПЕЦК. СЭС 363,4 КВТ', 'code_project': 'ШЛМ2022'}
# data = {'found_invertor_0': {'module': 'Deye SUN 5K-G03', 'inputs_x_2': '2', 'model': 'SUN 5K-G03', 'title': 'Deye', 'inputs': 1, 'mppt': '2', 'p_max': '5.500', 'width': 330.0, 'height': 323.0, 'depth': 190.0, 'weight': '7.500', 'v_mpp_min': '120', 'v_mpp_max': '850', 'tp_nom': '50.0', 'p_nom': '5.000', 'tp_lim': '60.0', 'p_lim': '60.0', 'tp_lim_abs': '70.0', 'p_lim_abs': '70.0', 'phase': 3, 'v_out': '230.0', 'i_out_max': '8.3', 'kpd_max': '97.50', 'kpd_euro': '97.30', 'v_abs_max': '1000', 'protect': 'Н/Д', 'count_invertor': 1, 'diff_mppt': False, 'broken_file': False, 'type_inv': 'QF', 'title_grid_line': 'ВБШвнг(A)-LS 4x95', 'title_grid_line_length': '180 м', 'title_grid_top': 'ЩР 0.4 кВ (ВИЭ)', 'title_grid_switch': 'QF1 3P 160A', 'use_5or4_line': False, 'local_0': {'controller': False, 'commutator': False, 'left_yzip': False, 'right_yzip': False, 'title_other_device': 'УЗИП', 'strings': 2}, 'i_nom_inv': 'C160', 'brand_cable_inv': 'ВБШвнг(А)-LS 4x95', 'length_cable_inv': '180 м*', 'yellow_line_inv': True, 'red_line_inv': True, 'blue_line_inv': True, 'green_line_inv': True, 'black_line_inv': True, 'yellow_switch_inv': True, 'red_switch_inv': True, 'blue_switch_inv': True, 'green_switch_inv': True, 'total_count_strings': 2, 'file': 14, 'folder': 1, 'config_0': {'count_mppt': 2, 'count_invertor': '1', 'count_string': 2, 'count_pv': '11', 'use_y_connector': False, 'use_all_mppt': False}}, 'found_invertor_1': {'module': 'Deye SUN-12K-SG04LP3', 'inputs_x_2': '3', 'model': 'SUN-12K-SG04LP3', 'title': 'Deye', 'inputs': 1, 'mppt': '2', 'p_max': '13.200', 'width': 422.0, 'height': 702.0, 'depth': 281.0, 'weight': '30.000', 'v_mpp_min': '200', 'v_mpp_max': '800', 'tp_nom': '45.0', 'p_nom': '12.000', 'tp_lim': '60.0', 'p_lim': '10.000', 'tp_lim_abs': '80.0', 'p_lim_abs': '7.500', 'phase': 3, 'v_out': '400.0', 'i_out_max': '26.0', 'kpd_max': '97.47', 'kpd_euro': '97.05', 'v_abs_max': '1000', 'protect': 'IP65 (outdoor)', 'count_invertor': 1, 'diff_mppt': True, 'broken_file': False, 'type_inv': 'QF', 'title_grid_line': 'ВБШвнг(A)-LS 4x95', 'title_grid_line_length': '180 м', 'title_grid_top': 'ЩР 0.4 кВ (ВИЭ)', 'title_grid_switch': 'QF1 3P 160A', 'use_5or4_line': False, 'local_0': {'controller': False, 'commutator': False, 'left_yzip': False, 'right_yzip': False, 'title_other_device': 'УЗИП', 'strings': 3}, 'i_nom_inv': 'C160', 'brand_cable_inv': 'ВБШвнг(А)-LS 4x95', 'length_cable_inv': '180 м*', 'yellow_line_inv': True, 'red_line_inv': True, 'blue_line_inv': True, 'green_line_inv': True, 'black_line_inv': True, 'yellow_switch_inv': True, 'red_switch_inv': True, 'blue_switch_inv': True, 'green_switch_inv': True, 'file': 9, 'folder': 1, 'config_0': {'count_mppt': '1', 'count_string': '2', 'count_pv': '14', 'use_y_connector': True, 'use_all_mppt': False}, 'config_1': {'count_mppt': '1', 'count_string': '1', 'count_pv': '14', 'use_y_connector': False, 'use_all_mppt': False}}, 'found_other_0': {'table_data': {'broken_file': False, 'Тип оборудования': 'КТП', 'Название оборудования': 'КТПНУ-250/10/0,4-T-KK-УХЛ1', 'Габаритные размеры, ДхШхВ, мм': '5000x4800x3300', 'Кол-во транспортных единиц, шт': '2', 'Масса, кг': '13000', 'Сила тока, А': '600', 'Номинальное напряжение ВН, кВ': '10', 'Наибольшее рабочее напряжение, кВ': '12', 'Номинальная частота переменного тока, Гц': '50', 'Номинальный ток главный цепей вводных ячеек ВН, А': '630', 'Номинальный ток главный цепей, А': '630', 'Номинальный ток сборных шин, А': '630', 'Ток термической стойкости в  течение 1 сек. со стороны ВН, не менее, кА': '13', 'Ток электродинамической стойкости в  течение 1 сек. со стороны ВН, не менее, кА': '17', 'Номинальное напряжение НН, кВ': '0,4', 'Номинальный ток РУНН, А': '400', 'Тип системы заземления со стороны НН': 'TN-C-S', 'Тип силового трансформатора Т1': 'ТЛС', 'Мощность силового трансформатора Т1, кВ*А': '250', 'Способ и диапазон регулирования': 'ПБВ±2х2,5%', 'Схема и группа соединения обмоток': 'Д/Ун-11'}, 'file': 1, 'folder': 1, 'title_other': 'КТПНУ-250/10/0,4-T-KK-УХЛ1', 'type_other': 'КТП', 'power_other': '250', 'i_other': '600', 'count_other': 1, 'type_param_other': 'QF', 'i_nom_other': 'C160', 'brand_cable_other': 'ВБШвнг(А)-LS 4x95', 'length_cable_other': '180 м*', 'red_line_other': False, 'green_line_other': False, 'red_switch_other': False, 'green_switch_other': False, 'yellow_line_other': True, 'blue_line_other': True, 'black_line_other': True, 'yellow_switch_other': True, 'blue_switch_other': True}, 'use_yzip': True, 'use_counter': True, 'use_threePhase': True, 'brand_cable_yzip': 'ОПН 0.4 кВ, 10 кА', 'type_param_yzip': 'QF', 'i_nom_yzip': 'C125', 'brand_cable_out': '2*3 ВВГнг(А)-LS 1x120 (3L)+', 'cable_out': '2 ВВГнг(А)-LS 1x120 (PE+N)+', 'length_cable_out': '20 м*', 'type_param_out': 'РУ-0.4кВ, Шкаф РП-3.4, сущ. АВ 3QF14'}
# draw(data, gost_frame_params)