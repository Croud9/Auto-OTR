from encodings.utf_8 import encode
import schemdraw
import schemdraw.elements as elm
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from fontTools.ttLib import TTFont
import gost_frame
import encode_file

def closer(slr):
    slr += elm.Line().left().length(0.125)
    slr += elm.Line().up().length(0.05)
    slr += elm.Line().down().length(0.45)
    slr += elm.Line().up().length(0.05)
    slr += elm.Line().right().length(0.125)

def draw_frame_module(slr, params):
    slr += (block_top := elm.Line().right().length(5))
    slr += elm.Line().left().length(5)

    for i in range(3):
        slr += elm.Line().down().length(1)
        slr += elm.Line().right().length(5).label(params[i], ofst=(0, 0.75))
        slr += elm.Line().left().length(5)

    slr += elm.Line().down().length(1.5)
    slr += (right_17 :=elm.Line().right().length(5))
    slr += elm.Label().at(right_17.center).label(params[0], ofst=(0,2))
    slr += elm.Label().at(right_17.center).label(params[3], ofst=(0,1))
    slr += elm.Line().up().length(4.5)

    return block_top

def draw_color_line(slr, switch_or_line, names):
    slr += (antenna := elm.Antenna())
    slr += (antenna_end := elm.Line().up().at(antenna.end, dy=0.6).length(0.01))

    slr += (bottom_blue_line := elm.Line().up().at(antenna_end.end, dy=0.5, dx=1).length(0.5).color('blue'))
    slr += elm.Label().at(bottom_blue_line.start).label(names[3], loc="bottom", ofst=(3,-0.5))
    slr += elm.Label().at(bottom_blue_line.start).label(names[4], loc="bottom", ofst=(2.25,-0.5))
    slr += elm.Label().at(bottom_blue_line.start).label(names[5], loc="bottom", ofst=(1.5,-0.5))
    slr += elm.Label().at(bottom_blue_line.start).label(names[6], loc="bottom", ofst=(0.75,-0.5))
    slr += elm.Line().endpoints(antenna_end.end, bottom_blue_line.start).color('blue')
    if switch_or_line[0] == True:
        slr += (bottom_black_line := elm.Line().up().at(antenna_end.end, dy=0.5, dx=0.6).dot().length(2).color('black')).linestyle('--')
        slr += elm.Line().endpoints(antenna_end.end, bottom_black_line.start).color('black').linestyle('--')

    if switch_or_line[1][0] == False:
        slr += elm.Line().up().at(bottom_blue_line.end).length(1.75).dot().color('blue')
    else:
        slr += elm.Switch().up().at(bottom_blue_line.end).length(1)
        slr += elm.Line().up().length(0.75).dot().color('blue')

    if switch_or_line[2][0] == True and switch_or_line[2][1] == True:
        slr += (bottom_red_line := elm.Line().up().at(antenna_end.end, dy=0.5, dx=0.25).length(0.5).color('red'))
        slr += elm.Line().endpoints(antenna_end.end, bottom_red_line.start).color('red')
        slr += elm.Switch().up().at(bottom_red_line.end).length(1)
        slr += elm.Line().up().length(1).dot().color('red')
    elif switch_or_line[2][0] == False and switch_or_line[2][1] == True:
        slr += (bottom_red_line := elm.Line().up().at(antenna_end.end, dy=0.5, dx=0.25).length(2.5).color('red').dot())
        slr += elm.Line().endpoints(antenna_end.end, bottom_red_line.start).color('red')

    if switch_or_line[3][0] == True and switch_or_line[3][1] == True:
        slr += (bottom_green_line := elm.Line().up().at(antenna_end.end, dy=0.5, dx=-0.25).length(0.5).color('lightgreen'))
        slr += elm.Line().endpoints(antenna_end.end, bottom_green_line.start).color('lightgreen')
        slr += elm.Switch().up().at(bottom_green_line.end).length(1)
        slr += elm.Line().up().length(1.25).dot().color('lightgreen')
    elif switch_or_line[3][0] == False and switch_or_line[3][1] == True:
        slr += (bottom_green_line := elm.Line().up().at(antenna_end.end, dy=0.5, dx=-0.25).length(2.75).color('lightgreen').dot())
        slr += elm.Line().endpoints(antenna_end.end, bottom_green_line.start).color('lightgreen')

    if switch_or_line[4][0] == True and switch_or_line[4][1] == True:
        slr += (bottom_yellow_line := elm.Line().up().at(antenna_end.end, dy=0.5, dx=-0.75).length(0.5).color('yellow'))
        slr += elm.Line().endpoints(antenna_end.end, bottom_yellow_line.start).color('yellow')
        slr += elm.Switch().up().at(bottom_yellow_line.end).length(1)
        slr += elm.Line().up().length(1.5).dot().color('yellow')
    elif switch_or_line[4][0] == False and switch_or_line[4][1] == True:
        slr += (bottom_yellow_line := elm.Line().up().at(antenna_end.end, dy=0.5, dx=-0.75).length(3).color('yellow').dot())
        slr += elm.Line().endpoints(antenna_end.end, bottom_yellow_line.start).color('yellow')

def draw_invertor(slr, params, names, switch_or_line):
    block_top = draw_frame_module(slr, params)

    slr += elm.Line().up().at(block_top.center, dx = -0.5).length(0.25).color('white')

    slr += elm.Line().up().length(1)
    slr += ( box_top := elm.Line().right().length(1))
    slr += elm.Label().at(box_top.center, dx = -0.3).label('~', ofst=(0,-0.8))
    slr += elm.Line().down().length(1)
    slr += ( box_bot := elm.Line().left().length(1))
    slr += elm.Label().at(box_bot.center, dx = 0.3).label('-', ofst=(0, -0.5) )
    slr += elm.Line().endpoints(box_top.end, box_bot.end)

    slr += (connect_antenna := elm.Line().up().at(box_top.center).length(4))
    slr += elm.Label().at(connect_antenna.center).label(names[0], ofst=(0,1.2), rotate = 90)
    slr += elm.Label().at(connect_antenna.center).label(names[1], ofst=(0,0.6), rotate = 90)
    slr += elm.Label().at(connect_antenna.center).label(names[2], ofst=(0,-0.6), rotate = 90).color('red')

    draw_color_line(slr, switch_or_line, names)

def custom_module(slr, params, names, switch_or_line):
    block_top = draw_frame_module(slr, params)

    slr += elm.Line().up().at(block_top.center, dx = -1.5).length(0.25).color('white')
    slr += elm.Line().up().length(1)
    slr += ( box_top := elm.Line().right().length(3))
    slr += elm.Line().down().length(1)
    slr += elm.Line().left().length(3)

    slr += (connect_antenna := elm.Line().up().at(box_top.center).length(4))
    slr += elm.Label().at(connect_antenna.center).label(names[0], ofst=(0,1.2), rotate = 90)
    slr += elm.Label().at(connect_antenna.center).label(names[1], ofst=(0,0.6), rotate = 90)
    slr += elm.Label().at(connect_antenna.center).label(names[2], ofst=(0,-0.6), rotate = 90).color('red')

    draw_color_line(slr, switch_or_line, names)

def grounding_module(slr, names, switch_or_line):
    slr += (block_top := elm.Line().right().length(5).color('white'))
    slr += ( white_line := elm.Line().up().at(block_top.center).length(3).color('white'))

    slr += elm.Ground()
    slr += elm.Thermistor().flip().label(names[2], loc='bottom').length(2.5)
    slr += elm.Line().up().at(white_line.end).length(2.25)

    draw_color_line(slr, switch_or_line, names)

def general_line(slr, three_phase):
    slr.push()
    slr.here = (6, -7.15)
    slr += (start_all_general_line := elm.Line().right().length(0.5).color('white'))
    slr += (start_yellow := elm.Line().right().at(start_all_general_line.start, dy = -1).length(0.5).color('yellow')).label("L1", loc="left", color="black")
    slr += (start_blue := elm.Line().right().at(start_all_general_line.start, dy = -1.75).length(0.5).color('blue')).label("N", loc="left", color="black")
    slr += (start_black := elm.Line().right().at(start_all_general_line.start, dy = -2).length(0.5)).label("PE", loc="left", color="black").linestyle('--')

    slr.pop()# Правый конец
    slr += (end_white_general_line := elm.Line().right().length(1).color('white'))
    slr += (general_blue_line := elm.Line().right().at(end_white_general_line.end, dy=-1.75).length(1).color('blue'))
    slr += (black_ground := elm.Line().right().at(general_blue_line.end, dy = -0.25).length(0.5).linestyle('--'))
    slr += elm.Ground()
    slr += (general_yellow_line := elm.Line().right().at(general_blue_line.start, dy=0.75).length(1).color('yellow'))
    
    slr += elm.Line().endpoints(general_blue_line.start, start_blue.end).color("blue")
    slr += elm.Line().endpoints(general_yellow_line.start, start_yellow.end).color("yellow")
    slr += elm.Line().endpoints(black_ground.start, start_black.end).linestyle('--')

    if three_phase == True:
        slr.push()
        slr.here = (6, -7.15)
        slr += (start_green := elm.Line().right().at(start_all_general_line.start, dy = -1.25).length(0.5).color('lightgreen')).label("L2", loc="left", color="black")
        slr += (start_red := elm.Line().right().at(start_all_general_line.start, dy = -1.5).length(0.5).color('red')).label("L3", loc="left", color="black")
        
        slr.pop() # Правый конец
        slr += (general_red_line := elm.Line().at(general_blue_line.start, dy=0.25).right().length(1).color('red'))
        slr += (general_green_line := elm.Line().at(general_blue_line.start, dy=0.5).right().length(1).color('lightgreen'))
        slr += elm.Line().endpoints(general_red_line.start, start_red.end).color("red")
        slr += elm.Line().endpoints(general_green_line.start, start_green.end).color("lightgreen")

def generate_frame(slr):
    slr += (main_top :=elm.Line().right().length(5))
    slr += elm.Label().at(main_top.center).label('Обозначение - марка и', ofst=(0,-3.5))
    slr += elm.Label().at(main_top.center).label('сечение проводника', ofst=(0,-4.5))
    slr +=  elm.Line().down().length(4)
    slr +=  elm.Line().left().length(2.5)
    slr.push()

    names_main_frame = ['Обозначение', 'Тип', 'Ном. ток, А', 'Тип \n расцепителя', 'Обозначение', 'Тип', 'Ном. ток, А', 'Хар-ка \n срабатывания']
    for i in names_main_frame:
        slr += elm.Line().down().length(1)
        slr += elm.Line().right().length(2.5).label(i, ofst=(0,0.6))
        slr += elm.Line().left().length(2.5)

    slr += elm.Line().right().length(2.5)
    slr += elm.Line().up().length(8)

    slr.pop()
    slr += (left_top_1 := elm.Line().left().length(2.5))
    slr += elm.Label().at(left_top_1.center).label('Аппарат', ofst=(0,3.5))
    slr += elm.Label().at(left_top_1.center).label('на вводе', ofst=(0,4.5))
    slr += elm.Line().down().length(4)
    slr += elm.Line().right().length(2.5)
    slr += elm.Line().down().length(4)
    slr += (left_top_2 := elm.Line().left().length(2.5))
    slr += elm.Label().at(left_top_2.center).label('Аппарат', ofst=(0,-4.5))
    slr += elm.Label().at(left_top_2.center).label('отходящ.', ofst=(0,-3.5))
    slr += elm.Label().at(left_top_2.center).label('линии', ofst=(0,-2.5))
    slr += elm.Line().up().length(12)
    slr += elm.Line().left().length(0.5)
    slr += (left_side_1 := elm.Line().down().length(4))
    slr += elm.Label().at(left_side_1.center).label('Кабельная линия', ofst=(0,0.4), rotate=90)
    slr += elm.Line().right().length(0.5)
    slr += elm.Line().left().length(0.5)
    slr += (left_side_2 := elm.Line().down().length(8))
    slr += elm.Label().at(left_side_2.center).label('Щит распределительный 0,4 кВ', ofst=(0,0.4), rotate=90)
    slr += elm.Line().right().length(0.5)
    slr += elm.Line().left().length(0.5)
    slr += (left_side_3 := elm.Line().down().length(4))
    slr += elm.Label().at(left_side_3.center).label('Кабельная линия', ofst=(0,0.4), rotate=90)
    slr += elm.Line().right().length(0.5)
    slr += elm.Line().left().length(0.5)
    slr += (left_side_4 := elm.Line().down().length(6))
    slr += elm.Label().at(left_side_4.center).label('Эл. приемник', ofst=(0,0.4), rotate=90)
    slr += elm.Line().right().length(0.5)
    slr += (left_side_4 := elm.Line().up().length(10))

    slr += (second_top := elm.Line().right().length(5))
    slr += elm.Label().at(second_top.center).label('Обозначение - марка и', ofst=(0,-3.5))
    slr += elm.Label().at(second_top.center).label('сечение проводника', ofst=(0,-4.5))
    slr += elm.Line().down().length(4)
    slr += elm.Line().left().length(5)

    slr += elm.Line().down().length(1.5)
    slr += (right_9 :=elm.Line().right().length(5))
    slr += elm.Label().at(right_9.center).label('Условное графическое', ofst=(0,2))
    slr += elm.Label().at(right_9.center).label('обозначение', ofst=(0,1))
    slr += elm.Line().left().length(5)

    slr += elm.Line().down().length(1)
    slr += (right_10 :=elm.Line().right().length(5))
    slr += elm.Label().at(right_10.center).label('Номер по плану', ofst=(0, 1))
    slr += elm.Line().left().length(5)

    slr += elm.Line().down().length(1)
    slr += (right_11 :=elm.Line().right().length(5))
    slr += elm.Label().at(right_11.center).label('Pнам, кВт', ofst=(0, 1))
    slr += elm.Line().left().length(5)

    slr += elm.Line().down().length(1)
    slr += (right_12 :=elm.Line().right().length(5))
    slr += elm.Label().at(right_12.center).label('Iрасч, А', ofst=(0, 1))
    slr += elm.Line().left().length(5)

    slr += elm.Line().down().length(1.5)
    slr += (right_13 :=elm.Line().right().length(5))
    slr += elm.Label().at(right_13.center).label('Наименование', ofst=(0, 1.5))

    slr += elm.Line().up().length(6)
    slr += elm.Line().down().length(1.5)

def little_frame(slr):
    slr += elm.Line().up().length(0.35)
    slr += elm.Line().left().length(0.625)
    slr += elm.Line().down().length(0.175)
    slr += elm.Line().down().length(0.35)

def top_counter(slr, three_phase, counter, names):
    
    kraja = 0.625
    
    slr.here = (9, -7.9)
    slr += (start_all_general_line := elm.Line().right().length(0.625).color("white"))
    slr += elm.Dot().at(start_all_general_line.end, dy=-1.25, dx=0.75)
    slr += elm.Dot().at(start_all_general_line.end, dy=-1, dx=0.5).color('blue')
    slr += elm.Dot().at(start_all_general_line.end, dy=-0.25, dx=-1).color('yellow')
    
    slr += (bottom_black_line := elm.Line().up().at(start_all_general_line.end, dy=-1.25, dx=0.75).length(1.25 + 7).color('black').linestyle('--'))
    slr += (bottom_blue_line := elm.Line().up().at(start_all_general_line.end, dy=-1, dx=0.5).length(1 + 7).color('blue'))
    slr += (bottom_yellow_line := elm.Line().up().at(start_all_general_line.end, dy=-0.25, dx=-1).length(0.25 + 5).color('yellow'))

    slr += elm.Switch().at(bottom_yellow_line.end).length(1)
    slr += (top_yellow_line := elm.Line().up().length(1).color('yellow'))

    slr += (antenna := elm.Antenna().flip().at(bottom_blue_line.end, dy=1, dx=-0.5).color("gray"))
    slr += (antenna_end := elm.Line().up().at(antenna.end, dy=-0.65).length(0.05))
    slr += elm.Line().endpoints(antenna_end.end, bottom_blue_line.end).color('blue')
    slr += elm.Line().endpoints(antenna_end.end, top_yellow_line.end).color('yellow')
    slr += elm.Line().endpoints(antenna_end.end, bottom_black_line.end).color('black').linestyle('--')
    slr += (last_line := elm.Line().up().at(antenna.end).length(5).color("gray"))
    slr += elm.Label().at(last_line.center).label(names[0], ofst=(0,2), rotate = 90)
    slr += elm.Label().at(last_line.center).label(names[1], ofst=(0,1.4), rotate = 90)
    slr += elm.Label().at(last_line.center).label(names[2], ofst=(0,0.6), rotate = 90)
    slr += elm.Label().at(last_line.center).label(names[3], ofst=(0,-0.6), rotate = 90).color('red')
    slr += elm.Label().at(last_line.center).label(names[4], ofst=(5.5, 0))

    if three_phase == True:
        slr += elm.Dot().at(start_all_general_line.end, dy=-0.75, dx=0).color('red')
        slr += elm.Dot().at(start_all_general_line.end, dy=-0.5, dx=-0.5).color('lightgreen')
        slr += (bottom_red_line := elm.Line().up().at(start_all_general_line.end, dy=-0.75, dx=0).length(0.625 + 5).color('red'))
        slr += (bottom_green_line := elm.Line().up().at(start_all_general_line.end, dy=-0.5, dx=-0.5).length(0.5 + 5).color('lightgreen'))
        slr += elm.Switch().at(bottom_red_line.end).length(1)
        slr += (top_red_line := elm.Line().up().length(1).color('red'))
        slr += elm.Switch().at(bottom_green_line.end).length(1)
        slr += (top_green_line := elm.Line().up().length(1).color('lightgreen'))
        slr += elm.Line().endpoints(antenna_end.end, top_red_line.end).color('red')
        slr += elm.Line().endpoints(antenna_end.end, top_green_line.end).color('lightgreen')

    if counter == True:
        slr += elm.Dot().at(bottom_yellow_line.end, dy=-0.5).color('yellow')
        slr += elm.Line().right().at(bottom_yellow_line.end, dy=-0.5).length(2.5).color('yellow')
        slr += elm.Switch().reverse().length(1)
        slr += elm.Line().right().length(1).color('yellow')
        slr += elm.Line().down().length(0.175)
        slr += elm.Line().right().length(kraja).label('2', "center", color='black', ofst=(0,0.55))
        slr += elm.Line().up().length(0.35)
        slr += elm.Line().left().length(kraja)
        slr += elm.Line().down().length(0.5)

        if three_phase == True:
            slr += elm.Dot().at(bottom_green_line.end, dy=-1).color('lightgreen')
            slr += elm.Line().right().at(bottom_green_line.end, dy=-1).length(2).color('lightgreen')
            slr += elm.Switch().reverse().length(1)
            slr += elm.Line().right().length(1).color('lightgreen')
            slr += elm.Line().down().length(0.175)
            slr += elm.Line().right().length(kraja).label('5', "center", color='black', ofst=(0,0.55))
            slr += elm.Line().up().length(0.35)
            slr += elm.Line().left().length(kraja)
            slr += elm.Line().down().length(0.5)

            slr += elm.Dot().at(bottom_red_line.end, dy=-1.35).color('red')
            slr += elm.Line().right().at(bottom_red_line.end, dy=-1.35).length(1.5).color('red')
            slr += elm.Switch().reverse().length(1)
            slr += elm.Line().right().length(1).color('red')
            slr += elm.Line().down().length(0.175)
            slr += elm.Line().right().length(kraja).label('8', "center", color='black', ofst=(0,0.55))
            slr += elm.Line().up().length(0.35)
            slr += elm.Line().left().length(kraja)
            slr += elm.Line().down().length(0.5)
        else:
            slr += elm.Line().down().length(1)

        # начало построения счетчика
        slr += elm.Dot().at(bottom_blue_line.end, dy=-4).color('blue')
        slr += elm.Line().right().at(bottom_blue_line.end, dy=-4).length(3).color('blue')
        slr += elm.Line().down().length(0.175)
        slr += elm.Line().right().length(kraja).label('10', "center", color='black', ofst=(0,0.55))
        slr += elm.Line().up().length(0.35)
        slr += elm.Line().left().length(kraja)
        slr += elm.Line().down().length(0.5)

        slr += elm.Line().down().length(0.5)

        slr += (little_frame_one := elm.Line().down().length(0.175))
        slr += elm.Line().right().length(kraja).label('1', "center", color='black', ofst=(0,0.55))
        little_frame(slr)

        slr += (little_frame_two := elm.Line().down().length(0.175))
        slr += elm.Line().right().length(kraja).label('3', "center", color='black', ofst=(0,0.55))
        little_frame(slr)

        if three_phase == False:
            slr.push()
            slr += elm.Line().left().length(4.25).dot(open = True).at(little_frame_one.start)
            closer(slr)
            slr += elm.Line().left().length(4.25).dot(open = True).at(little_frame_two.start)
            slr += elm.Ground()
            slr.pop()
            slr += elm.Line().down().length(1.4)
        else:
            slr += (little_frame_three := elm.Line().down().length(0.175))
            slr += elm.Line().right().length(kraja).label('4', "center", color='black', ofst=(0,0.55))
            little_frame(slr)

            slr += (little_frame_four := elm.Line().down().length(0.175))
            slr += elm.Line().right().length(kraja).label('6', "center", color='black', ofst=(0,0.55))
            little_frame(slr)

            slr += (little_frame_five := elm.Line().down().length(0.175))
            slr += elm.Line().right().length(kraja).label('7', "center", color='black', ofst=(0,0.55))
            little_frame(slr)

            slr += (little_frame_six := elm.Line().down().length(0.175))
            slr += elm.Line().right().length(kraja).label('9', "center", color='black', ofst=(0,0.55))
            little_frame(slr)

            slr.push()
            slr += elm.Line().left().length(4.25).dot(open = True).at(little_frame_one.start)
            closer(slr)
            slr += elm.Line().left().length(4.25).dot(open = True).at(little_frame_two.start)
            slr += elm.Ground()

            slr += elm.Line().left().length(3.75).dot(open = True).at(little_frame_three.start)
            closer(slr)
            slr += elm.Dot().at(little_frame_four.start, dx=-2)
            slr += elm.Line().left().length(1.75).dot(open = True).at(little_frame_four.start, dx=-2)
            slr += elm.Ground()
            slr += elm.Line().left().length(3.25).dot(open = True).at(little_frame_five.start)
            closer(slr)
            slr += (little_frame_left_line := elm.Line().left().length(1.25).dot(open = True).at(little_frame_six.start, dx=-2))
            slr += elm.Ground()
            slr += elm.Line().up().length(1.4).dot().at(little_frame_left_line.start)

            slr += elm.Line().length(0.35).at(little_frame_six.start).theta(130).color('purple')
            slr += elm.Line().up().length(0.15).color('purple')
            slr += elm.Line().length(0.35).at(little_frame_four.start).theta(130).color('purple')
            slr += elm.Line().up().length(0.15).color('purple')
            slr += elm.Line().length(0.35).at(little_frame_four.start).theta(230).color('purple')
            slr += elm.Line().length(0.35).at(little_frame_two.start).theta(230).color('purple')
            slr.pop()

        slr += elm.Line().right().length(5)
        slr += elm.Line().up().length(5)
        slr += elm.Line().left().length(5)
        slr += elm.Line().down().length(0.5)
        slr += elm.Line().up().length(2)
        slr += elm.Line().right().length(5).label("Wh \n Счетчик э/э двунаправленный", "center", ofst=(0,-1))
        slr += elm.Line().down().length(1.5)

def draw(all_params, gost_frame_params):
    print('paraaaaaams',gost_frame_params)
    schemdraw.config(fontsize = 10)
    with schemdraw.Drawing(file=f'Data/Schemes/connect_system.svg', show = False, scale = 0.5, lw = 0.7) as slr:
        module_offset = 5 # начало чертежа модулей
        count_all_modules = all_params[0][3] + all_params[1][4]
        yzip = all_params[3][0]# УЗИП
        counter = all_params[3][1] # Счетчик
        three_phase = all_params[3][2] #Трёхфазная система?
        count_invertor = all_params[0][3]

        generate_frame(slr) # левая рамка
        names = [all_params[2][5], all_params[2][6], all_params[2][7], all_params[2][8], all_params[2][9]]
        top_counter(slr, three_phase, counter, names) # Верхний счетчик

        for_del1 = all_params.copy()
        for_del2 = all_params.copy()
        for t in range(len(all_params[0]) // 20):
            count_invertor = all_params[0][3]
            all_params = for_del1
            print('До', len(all_params[0]) // 20)
            print(all_params[0])
            for i in range(count_invertor):
                l2_phase = all_params[0][12]
                l3_phase = all_params[0][14]
                if three_phase == False:
                    phase2 = False
                    phase3 = False
                else:
                    phase2 = l2_phase
                    phase3 = l3_phase

                yellow_switch_and_line = [all_params[0][16], all_params[0][11]] #l1
                red_switch_and_line = [all_params[0][17], phase2] #L2
                blue_switch_and_line = [all_params[0][18], all_params[0][13]] #ноль
                green_switch_and_line = [all_params[0][19], phase3] #L3
                black_switch_and_line = all_params[0][15] #земля
                switch_or_line = [black_switch_and_line, blue_switch_and_line, red_switch_and_line, green_switch_and_line, yellow_switch_and_line]

                slr.here = (module_offset, -17.5)
                params = ["Инвертор", all_params[0][1], all_params[0][2], all_params[0][0]]
                names = [all_params[0][8], all_params[0][9], all_params[0][10], f"{all_params[0][4]} {t+1}.{i+1}", all_params[0][5], all_params[0][6], all_params[0][7]]

                draw_invertor(slr, params, names, switch_or_line) # инвертор
                module_offset += 5

            del all_params[0][0:20]
            print('После', len(all_params[0]) // 20)
            print(all_params[0])
            if not all_params:
                return
                
        for t in range(len(all_params[1]) // 21):
            count_custom = all_params[1][4]
            all_params = for_del2
            print('До', len(all_params[1]) // 21)
            print("Кол-во допов",count_custom)
            for i in range(count_custom):
                l2_phase = all_params[1][13]
                l3_phase = all_params[1][15]
                if three_phase == False:
                    phase2 = False
                    phase3 = False
                else:
                    phase2 = l2_phase
                    phase3 = l3_phase

                yellow_switch_and_line = [all_params[1][17], all_params[1][12]] #l1
                red_switch_and_line = [all_params[1][18], phase2] #L2
                blue_switch_and_line = [all_params[1][19], all_params[1][14]] #ноль
                green_switch_and_line = [all_params[1][20], phase3] #L3
                black_switch_and_line = all_params[1][16] #земля
                switch_or_line = [black_switch_and_line, blue_switch_and_line, red_switch_and_line, green_switch_and_line, yellow_switch_and_line]

                slr.here = (module_offset, -17.5)
                # params = ['Анализатор мощности', '0.01', '0.05', 'Janitza UMG 604 E PRO']
                params = [all_params[1][3], all_params[1][1], all_params[1][2], all_params[1][0]]
                names = [all_params[1][9], all_params[1][10], all_params[1][11], f"{all_params[1][5]} {t+1}.{i+1}", all_params[1][6], all_params[1][7], all_params[1][8]]

                custom_module(slr, params, names, switch_or_line) # изменяемый моудуль
                module_offset += 5

            del all_params[1][0:21]
            print('После', len(all_params[1]) // 21)
            print(all_params[1])
            if not all_params:
                return

        if yzip == True:
            if three_phase == False:
                phase2 = False
                phase3 = False
            else:
                phase2 = True
                phase3 = True

            slr.here = (module_offset, -17.5)
            black_switch_and_line = False #земля
            blue_switch_and_line = [True, True] #ноль
            red_switch_and_line = [True, phase2] #L2
            green_switch_and_line = [True, phase3] #L3
            yellow_switch_and_line = [True, True] #l1
            switch_or_line = [black_switch_and_line, blue_switch_and_line, red_switch_and_line, green_switch_and_line, yellow_switch_and_line]
            names = ['', '', all_params[2][0], all_params[2][1], all_params[2][2], all_params[2][3], all_params[2][4]]
            grounding_module(slr, names, switch_or_line) # ВЗаземление
            module_offset += 5

        slr.here = (module_offset, -7.125)
        general_line(slr, three_phase)
        width = 30.5 if count_all_modules == 1 else 30.5 + ((count_all_modules - 1) * 5)
        height = 29
        slr.here = (-1, 5)
        data = {'width': width, 'height': height, 'title_prjct': gost_frame_params['title_project'],
                'code_prjct': gost_frame_params['code_project'], 'type_scheme': 'Cхема электрическая \n принципиальная'}
        gost_frame.all_frame(slr, **data)
    srcfile = 'Data/Schemes/connect_system.svg'
    trgfile = 'Data/Schemes/connect_system_codec.svg'
    encode_file.to_utf8(srcfile, trgfile)