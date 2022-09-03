import schemdraw
import schemdraw.elements as elm
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from fontTools.ttLib import TTFont

def generate_frame(slr, names, bot_line_invertor, three_phase, five_line, len_title):
    offset_r_side_txt = 0.4
    slr += (top_invertor := elm.Line().right().length(5)).hold()
    slr += elm.Line().endpoints(bot_line_invertor.start, top_invertor.start)
    slr += elm.Line().endpoints(bot_line_invertor.end, top_invertor.end)

    r_side_line_len = 1.75
    slr += elm.Line().down().length(1)
    slr += (title_invertor := elm.Line().left().length(5))
    slr += elm.Line().down().length(1)
    slr += (num_title_invertor := elm.Line().right().length(5))
    slr += elm.Line().left().length(r_side_line_len)
    slr.push()
    slr += elm.Line().down().length(0.5)
    slr += (right_1 := elm.Line().right().length(r_side_line_len))
    slr += elm.Line().left().length(r_side_line_len)
    slr += elm.Line().down().length(0.5)
    slr += (right_2 := elm.Line().right().length(r_side_line_len))
    slr += elm.Line().left().length(r_side_line_len)
    slr += elm.Line().down().length(0.5)
    slr += (right_3 := elm.Line().right().length(r_side_line_len))
    slr += elm.Line().left().length(r_side_line_len)
    slr += elm.Line().down().length(0.5)
    slr += (right_4 := elm.Line().right().length(r_side_line_len))
    slr += elm.Line().left().length(r_side_line_len)
    slr.pop()
    slr += elm.Line().left().length(0.5)
    slr += (down_rotate_1 := elm.Line().down().length(2))
    slr += elm.Line().right().length(2.25)

    slr += elm.Line().down().length(0.5)

    slr += elm.Line().left().length(r_side_line_len)
    slr.push()
    slr += elm.Line().down().length(0.5)
    slr += (right_5 := elm.Line().right().length(r_side_line_len))
    slr += elm.Line().left().length(r_side_line_len)
    slr += elm.Line().down().length(0.5)
    slr += (right_6 := elm.Line().right().length(r_side_line_len))
    slr += elm.Line().left().length(r_side_line_len)
    slr += elm.Line().down().length(0.5)
    slr += (right_7 := elm.Line().right().length(r_side_line_len))
    slr += elm.Line().left().length(r_side_line_len)
    slr += elm.Line().down().length(0.5)
    slr += (right_8 := elm.Line().right().length(r_side_line_len))
    slr += elm.Line().left().length(r_side_line_len)
    slr.pop()
    slr += elm.Line().left().length(0.5)
    slr += (down_rotate_2 := elm.Line().down().length(2))
    slr += elm.Line().right().length(2.25)

    slr += elm.Line().down().length(1)
    dash_phase = 3
    if three_phase == False:
        five_line = True
        dash_phase = 1
    
    slr += elm.Line().left().length(r_side_line_len)
    slr.push()
    slr += elm.Line().down().length(0.5)
    slr += (right_9 := elm.Line().right().length(r_side_line_len))
    slr += elm.Line().left().length(r_side_line_len)

    if five_line == True:
        black_line_down_len = 2
        slr += elm.Line().down().length(0.5)
        slr += (right_9_5or4 := elm.Line().right().length(r_side_line_len))
        slr += elm.Line().left().length(r_side_line_len)
        slr += elm.Label().at(right_9.center).label("PE", ofst=(0, offset_r_side_txt - 1))
        slr += elm.Label().at(right_9_5or4.center).label("N", ofst=(0, offset_r_side_txt - 1))
        slr.push()
        slr += elm.Line().right().at(right_9_5or4.end, dy=0.25).length(1).color("blue")
        slr += elm.Line().right().at(right_9.end, dy=0.25).length(0.25).color("yellow")
        slr += elm.Line().right().length(0.25).color("green")
        slr += elm.Line().right().length(0.25).color("yellow")
        slr += (r_black_line := elm.Line().right().length(0.25).color("green"))
        slr.pop()
    else:
        black_line_down_len = 1.5 
        slr += elm.Label().at(right_9.center).label("PEN", ofst=(0, offset_r_side_txt - 1))
        slr.push()
        slr += elm.Line().right().at(right_9.end, dy=0.25).length(0.125).color("yellow")
        slr += elm.Line().right().length(0.125).color("green")
        slr += elm.Line().right().length(0.5).color("blue")
        slr += elm.Line().right().length(0.125).color("yellow")
        slr += (r_black_line := elm.Line().right().length(0.125).color("green"))
        slr.pop()
    
    if three_phase == True:
        slr += elm.Line().down().length(0.5)
        slr += (right_10 := elm.Line().right().length(r_side_line_len))
        slr += elm.Label().at(right_10.center).label("L3", ofst=(0, offset_r_side_txt))
        slr += elm.Line().left().length(r_side_line_len)
        slr += elm.Line().down().length(0.5)
        slr += (right_11 := elm.Line().right().length(r_side_line_len))
        slr += elm.Label().at(right_11.center).label("L2", ofst=(0, offset_r_side_txt))
        slr += elm.Line().left().length(r_side_line_len)
        slr += elm.Line().down().length(0.5)
        slr += (right_12 := elm.Line().right().length(r_side_line_len))
        slr += elm.Label().at(right_12.center).label("L1", ofst=(0, offset_r_side_txt))
        slr += elm.Line().left().length(r_side_line_len)
        slr += elm.Line().right().at(right_10.end, dy=0.25).length(1).color("red")
        slr += elm.Line().right().at(right_11.end, dy=0.25).length(1).color("lightgreen")
        slr += elm.Line().right().at(right_12.end, dy=0.25).length(1).color("yellow")
    else:
        black_line_down_len = 1
        slr += elm.Line().down().length(0.5)
        slr += (right_10 := elm.Line().right().length(r_side_line_len))
        slr += elm.Label().at(right_10.center).label("L", ofst=(0, offset_r_side_txt))
        slr += elm.Line().left().length(r_side_line_len)
        slr += elm.Line().right().at(right_10.end, dy=0.25).length(1).color("red")
        
    slr.pop()
    slr += elm.Line().left().length(0.5)
    slr += (down_rotate_3 := elm.Line().down().length(black_line_down_len + 0.5))
    slr += elm.Line().right().length(2.25)
    slr += elm.Label().at(down_rotate_3.center).label("Grid", ofst=(offset_r_side_txt,0), rotate=90)
    
    slr.push()
# правая ветка
    slr += elm.Line().down().at(r_black_line.end).length(black_line_down_len)
    slr += elm.Line().right().length(5)
    slr += elm.Line().up().length(5).label(names[2], ofst=(0, 0.5), rotate=True)
    slr += elm.Label().label(len_title, ofst=(-5, -0.75), rotate=True)
    slr += (groundsignal := elm.GroundSignal())
    
    if five_line == True:
        slr += elm.Line().at(groundsignal.end).theta(45).length(0.5)
        slr += (r_line_1 := elm.Line().up().length(2).dot()).hold
        slr += elm.Line().theta(45).length(0.5)
        slr += (r_line_2 := elm.Line().up().length(2).dot())
        slr += elm.Line().right().at(r_line_1.end).linestyle("--").length(1)
        slr += elm.Line().left().at(r_line_1.end).length(4).linestyle("--").label("PE","left")
    else:
        slr += elm.Line().at(groundsignal.end).theta(45).length(1)
        slr += (r_line_1 := elm.Line().up().length(1.5).dot())
        slr += (r_line_2 := elm.Line().up().length(0.375).dot())
        slr += elm.Line().right().at(r_line_1.end).linestyle("--").length(0.625)
        slr += elm.Line().left().at(r_line_1.end).length(4.375).linestyle("--").label("PE","left")
        
    slr += elm.Line().up().at(groundsignal.end).length(0.5)
    slr += elm.Line().theta(125).length(1).label(names[4], "left")
    slr.push()
    slr += elm.Line().theta(-55).length(0.25)
    slr += elm.Line().theta(215).length(0.125)
    slr += elm.Line().theta(305).length(0.375)
    slr += elm.Line().theta(395).length(0.125)
    slr.pop()
    slr += elm.Line().right().color("white").length(0.5)
    slr += elm.Line().theta(45).length(0.075).hold()
    slr += elm.Line().theta(135).length(0.075).hold()
    slr += elm.Line().theta(225).length(0.075).hold()
    slr += elm.Line().theta(315).length(0.075).hold()
    slr += elm.Line().up().length(0.375)
    for i in range(dash_phase):
        slr += elm.Line().theta(-20).length(0.175).hold()
        slr += elm.Line().theta(160).length(0.175).hold()
        slr += elm.Line().up().length(0.125)    
        
    if three_phase == False:
        slr += (r_line_3 := elm.Line().up().length(1.5).dot())
    else: 
        slr += (r_line_3 := elm.Line().up().length(1.25).dot())

    slr += elm.Line().right().at(r_line_2.end).length(0.625)
    slr += elm.Line().right().at(r_line_3.end, dy=-0.1).length(1.425)
    slr += elm.Line().right().at(r_line_3.end, dy=0.1).length(1.425)
    
    slr.push()
    slr += elm.Line().up().length(0.6).hold()
    slr += elm.Line().down().length(0.25)
    slr += elm.Line().theta(-15).length(0.25)
    slr += elm.Line().theta(205).length(0.5)
    slr += elm.Line().theta(-15).length(0.25)
    slr += elm.Line().down().length(1.175)
    slr.pop()

    slr += elm.Line().left().at(r_line_2.end).length(4.375).label("N","left")
    slr += elm.Line().left().at(r_line_3.end, dy=-0.1).length(2)
    
    slr.push()
    slr += elm.Line().up().length(0.7).hold()
    slr += elm.Line().down().length(0.15)
    slr += elm.Line().theta(-15).length(0.25)
    slr += elm.Line().theta(205).length(0.5)
    slr += elm.Line().theta(-15).length(0.25)
    slr += elm.Line().down().length(1.025)
    slr.pop()
    
    slr += elm.Line().left().length(1)
    for i in range(dash_phase):
        slr += elm.Line().theta(60).length(0.225).hold()
        slr += elm.Line().theta(240).length(0.125).hold()
        slr += elm.Line().left().length(0.125)  
        
    if three_phase == False:
        slr += elm.Line().left().length(0.45)
    else: 
        slr += elm.Line().left().length(0.2)  
    
    if three_phase == True:
        slr += elm.Line().left().at(r_line_3.end, dy=0.1).length(3.575).label("L1, L2, L3","left")
    else:
        slr += elm.Line().left().at(r_line_3.end, dy=0.1).length(3.575).label("L","left")
    slr += elm.Label().at(r_line_3.end, dy=1, dx=-0.5).label(names[3])
    slr.pop()

    slr += elm.Label().at(title_invertor.center).label(names[0], ofst=(0,1))
    slr += elm.Label().at(num_title_invertor.center).label(names[1], ofst=(0,1))
    slr += elm.Label().at(down_rotate_1.center).label("RS485 out", ofst=(offset_r_side_txt,0), rotate=90)
    slr += elm.Label().at(right_1.center).label("Reference", ofst=(0,offset_r_side_txt))
    slr += elm.Label().at(right_2.center).label("RS485 -", ofst=(0,offset_r_side_txt))
    slr += elm.Label().at(right_3.center).label("RS485 +", ofst=(0,offset_r_side_txt))
    slr += elm.Label().at(right_4.center).label("termination", ofst=(0,offset_r_side_txt))

    slr += elm.Label().at(down_rotate_2.center).label("RS485 in", ofst=(offset_r_side_txt,0), rotate=90)
    slr += elm.Label().at(right_5.center).label("Reference", ofst=(0,offset_r_side_txt))
    slr += elm.Label().at(right_6.center).label("RS485 -", ofst=(0,offset_r_side_txt))
    slr += elm.Label().at(right_7.center).label("RS485 +", ofst=(0,offset_r_side_txt))
    slr += elm.Label().at(right_8.center).label("termination", ofst=(0,offset_r_side_txt))

def build_fem(slr, solar_count_on_the_top_side, solar_count_on_the_bot_side, num, two_num):
    for i in range(solar_count_on_the_top_side):
        slr += elm.Solar().left().length(1.5).reverse().flip().label("-      +", loc="bottom").idot(open=True).scale(0.5)
    slr += elm.Dot()
    slr += elm.Line().down().dot().label(f"{solar_count_on_the_top_side + solar_count_on_the_bot_side} ФЭМ - {num}.{two_num}", rotate=90).length(2)
    for i in range(solar_count_on_the_bot_side):
        slr += elm.Solar().right().length(1.5).reverse().flip().label("+      -").dot(open=True).scale(0.5)

def one_fem(slr, num, in_dot, fem_offset, solar_count_on_the_top_side, solar_count_on_the_bot_side, count_input_mppt, count_chain, flag, blue_len, use_all_mppt):
    global two_num
    
    one_fem_offset = 4 
    two_fem_offset = 8 
    count_input_mppt = int(count_input_mppt/2)
    
    # забивает постепенно все верхние без Y 
    if flag == 0:
        two_num += 1
        slr.here = (0, fem_offset)
        slr += (pin_plus := elm.Line().left().length(3.5).at(in_dot[0].center).color("red"))
        build_fem(slr, solar_count_on_the_top_side, solar_count_on_the_bot_side, num, two_num)
        slr += (pin_minus := elm.Line().right().length(blue_len).color("mediumblue"))
        # fem_offset -= 1

        for i in range(count_chain - 1):
            two_num += 1
            slr.here = (0, fem_offset)
            slr += (line_start := elm.Line().left().length(3.5).color("red"))
            build_fem(slr, solar_count_on_the_top_side, solar_count_on_the_bot_side, num, two_num)
            slr += (line_end := elm.Line().right().length(blue_len).color("mediumblue"))
            fem_offset -= one_fem_offset

    # распределяет по всем без Y
    if flag == 1:
        dot_num = 2
        two_num += 1
        slr.here = (0, fem_offset)
        slr += (pin_plus := elm.Line().left().length(3.5).at(in_dot[0].center).color("red"))
        build_fem(slr, solar_count_on_the_top_side, solar_count_on_the_bot_side, num, two_num)
        slr += (pin_minus := elm.Line().right().length(blue_len).color("mediumblue"))
        # fem_offset -= 1

        for i in range(count_chain - 1):
            two_num += 1
            slr.here = (0, fem_offset)
            slr += (line_start := elm.Line().left().length(3.5).color("red"))
            build_fem(slr, solar_count_on_the_top_side, solar_count_on_the_bot_side, num, two_num)
            slr += (line_end := elm.Line().right().length(blue_len).color("mediumblue"))
            fem_offset -= one_fem_offset

        two_num += 1
        slr.here = (-5.5, fem_offset)
        slr += (line_start := elm.Line().left().length(0.75).color("red"))
        build_fem(slr, solar_count_on_the_top_side, solar_count_on_the_bot_side, num, two_num)
        slr += (line_end := elm.Line().right().length(blue_len - 2).color("mediumblue"))
        slr+= elm.Wire("-|").at(in_dot[-2].center).to(line_start.start).color("red").scale(1)
        slr+= elm.Wire("-|").at(in_dot[-1].center).to(line_end.end).color("mediumblue").scale(1)

    # распределяет по всем с Y
    if flag == 2:
        full_mppt = 1
        dot_num = 2
        two_num += 1
        double_cicle = count_chain - count_input_mppt
        slr.here = (0, fem_offset)
        slr += (pin_plus := elm.Line().left().length(3.5).at(in_dot[0].center).color("red"))
        build_fem(slr, solar_count_on_the_top_side, solar_count_on_the_bot_side, num, two_num)
        slr += (pin_minus := elm.Line().right().length(blue_len - 2).color("mediumblue"))
        slr+= elm.Wire("|-").to(in_dot[1].center).color("mediumblue").scale(1)


        if use_all_mppt == 1:
            if double_cicle == count_input_mppt:
                two_num += 1
                slr.here = (-2.75, fem_offset)
                slr += (line_start := elm.Line().left().length(0.75).color("red"))
                build_fem(slr, solar_count_on_the_top_side, solar_count_on_the_bot_side, num, two_num)
                slr += (line_end := elm.Line().right().length(blue_len - 2).color("mediumblue"))
                slr+= elm.Wire("-|").at(pin_plus.center).to(line_start.start).color("red").scale(1)
                slr+= elm.Wire("-|").at(in_dot[1].center).to(line_end.end).color("mediumblue").scale(1)
                double_cicle -= 1
                full_mppt = 2
            fem_offset -= one_fem_offset

            for i in range(count_chain - (full_mppt + 2 * (double_cicle))): #одиночные цепочки
                dot_num += 1
                two_num += 1
                slr.here = (0, fem_offset)
                slr += (line_start := elm.Line().left().length(3.5).color("red"))
                build_fem(slr, solar_count_on_the_top_side, solar_count_on_the_bot_side, num, two_num)
                slr += (line_end_2 := elm.Line().right().length(blue_len - 2).color("mediumblue"))
                slr+= elm.Wire("|-").to(in_dot[dot_num].center).color("mediumblue").scale(1)
                dot_num += 1
                fem_offset -= two_fem_offset
            #
            for i in range(double_cicle): #двойные цепочки
                dot_num += 1
                two_num += 1
                slr.here = (0, fem_offset)
                slr += (line_start := elm.Line().left().length(3.5).color("red"))
                build_fem(slr, solar_count_on_the_top_side, solar_count_on_the_bot_side, num, two_num)
                slr += (line_end_2 := elm.Line().right().length(blue_len - 2).color("mediumblue"))
                slr+= elm.Wire("|-").to(in_dot[dot_num].center).color("mediumblue").scale(1)
                fem_offset -= one_fem_offset

                two_num += 1
                slr.here = (-2.75, fem_offset)
                slr += (line_start := elm.Line().left().length(0.75).color("red"))
                build_fem(slr, solar_count_on_the_top_side, solar_count_on_the_bot_side, num, two_num)
                slr += (line_end := elm.Line().right().length(blue_len - 2).color("mediumblue"))
                slr+= elm.Wire("-|").at(in_dot[dot_num-1].center).to(line_start.start).color("red").scale(1)
                slr+= elm.Wire("-|").at(in_dot[dot_num].center).to(line_end.end).color("mediumblue").scale(1)
                dot_num += 1
                fem_offset -= one_fem_offset
                
        elif use_all_mppt == False:
            if count_chain > 1:
                two_num += 1
                slr.here = (-2.75, fem_offset)
                slr += (line_start := elm.Line().left().length(0.75).color("red"))
                build_fem(slr, solar_count_on_the_top_side, solar_count_on_the_bot_side, num, two_num)
                slr += (line_end := elm.Line().right().length(blue_len - 2).color("mediumblue"))
                slr+= elm.Wire("-|").at(pin_plus.center).to(line_start.start).color("red").scale(1)
                slr+= elm.Wire("-|").at(in_dot[1].center).to(line_end.end).color("mediumblue").scale(1)
                double_cicle -= 1
                full_mppt = 2

                fem_offset -= one_fem_offset
                count_chain -= 2
                print("count_chain", count_chain)

                count_chain_add = count_chain % 2 if count_chain % 2 != 0 else 0

                for i in range(count_chain // 2): #двойные цепочки
                    dot_num += 1
                    two_num += 1
                    slr.here = (0, fem_offset)
                    slr += (line_start := elm.Line().left().length(3.5).color("red"))
                    build_fem(slr, solar_count_on_the_top_side, solar_count_on_the_bot_side, num, two_num)
                    slr += (line_end_2 := elm.Line().right().length(blue_len - 2).color("mediumblue"))
                    slr+= elm.Wire("|-").to(in_dot[dot_num].center).color("mediumblue").scale(1)
                    fem_offset -= one_fem_offset

                    two_num += 1
                    slr.here = (-2.75, fem_offset)
                    slr += (line_start := elm.Line().left().length(0.75).color("red"))
                    build_fem(slr, solar_count_on_the_top_side, solar_count_on_the_bot_side, num, two_num)
                    slr += (line_end := elm.Line().right().length(blue_len - 2).color("mediumblue"))
                    slr+= elm.Wire("-|").at(in_dot[dot_num-1].center).to(line_start.start).color("red").scale(1)
                    slr+= elm.Wire("-|").at(in_dot[dot_num].center).to(line_end.end).color("mediumblue").scale(1)
                    dot_num += 1
                    fem_offset -= one_fem_offset

                for i in range(count_chain_add): #одиночные цепочки
                    dot_num += 1
                    two_num += 1
                    slr.here = (0, fem_offset)
                    slr += (line_start := elm.Line().left().length(3.5).color("red"))
                    build_fem(slr, solar_count_on_the_top_side, solar_count_on_the_bot_side, num, two_num)
                    slr += (line_end_2 := elm.Line().right().length(blue_len - 2).color("mediumblue"))
                    slr+= elm.Wire("|-").to(in_dot[dot_num].center).color("mediumblue").scale(1)
                    dot_num += 1
                    fem_offset -= two_fem_offset

def gen_frame_mppt(slr, num, fem_offset, count_input_mppt, flag):
    # входы надписи и точки МРРТ
    slr.push()
    if flag <= 1:
        high_input = 2
    elif flag == 2:
        high_input = 4

    cicle_num = 0
    arrrr = []
    input_symbols = ["a+", "a-", "b+", "b-", "c+", "c-", "d+", "d-", "e+", "e-", "f+", "f-", "g+", "g-", "h+", "h-", "i+", "i-", "j+", "j-", "k+", "k-", "l+", "l-", "m+", "m-", "n+", "n-", "o+", "o-", "p+", "p-", "q+", "q-", "r+", "r-", "s+", "s-", "t+", "t-", "u+", "u-", "v+", "v-", "w+", "w-", "x+", "x-", "y+", "y-", "z+", "z-",
                    "aa+", "aa-", "bb+", "bb-", "cc+", "cc-", "dd+", "dd-", "e+", "e-", "f+", "f-", "g+", "g-", "h+", "h-", "i+", "i-", "j+", "j-", "k+", "k-", "l+", "l-", "m+", "m-", "n+", "n-", "o+", "o-", "p+", "p-", "q+", "q-", "r+", "r-", "s+", "s-", "t+", "t-", "u+", "u-", "v+", "v-", "w+", "w-", "x+", "x-", "y+", "y-", "z+", "z-",
                    "aaa+", "aaa-", "bbb+", "bbb-", "ccc+", "ccc-", "dd+", "dd-", "e+", "e-", "f+", "f-", "g+", "g-", "h+", "h-", "i+", "i-", "j+", "j-", "k+", "k-", "l+", "l-", "m+", "m-", "n+", "n-", "o+", "o-", "p+", "p-", "q+", "q-", "r+", "r-", "s+", "s-", "t+", "t-", "u+", "u-", "v+", "v-", "w+", "w-", "x+", "x-", "y+", "y-", "z+", "z-",
                    "aa+", "aa-", "bb+", "bb-", "cc+", "cc-", "dd+", "dd-", "e+", "e-", "f+", "f-", "g+", "g-", "h+", "h-", "i+", "i-", "j+", "j-", "k+", "k-", "l+", "l-", "m+", "m-", "n+", "n-", "o+", "o-", "p+", "p-", "q+", "q-", "r+", "r-", "s+", "s-", "t+", "t-", "u+", "u-", "v+", "v-", "w+", "w-", "x+", "x-", "y+", "y-", "z+", "z-"
                    ]
    for i in range(count_input_mppt):
        slr += (dot_plus := elm.Dot().at((0, fem_offset-cicle_num)).label(f"{num}{input_symbols[i]}", ofst=(1, 0)))
        i += 1
        arrrr.append(dot_plus)
        cicle_num += high_input
    slr.pop()
    dot_plus = arrrr
    # рамка под МРРТ
    slr += elm.Line().up().length(1)
    slr += elm.Line().right().length(1)
    slr.push()
    for i in range(count_input_mppt):
        slr += elm.Line().down().length(high_input)
        slr += elm.Line().left().length(1)
        slr += elm.Line().right().length(1)
    slr.pop()
    slr += elm.Line().right().length(0.5)
    slr += (line_for_mppt_title := elm.Line().down().length(count_input_mppt * high_input))
    slr += elm.Label().at(line_for_mppt_title.center).label(f"MPPT {num} (DC)", ofst=(0, -0.5), rotate=270)
    slr += elm.Line().left().length(0.5)
    return dot_plus

def generate_fem(slr, solar_count_on_the_chain, fem_offset, count_mppt, count_chain, use_y_connector, use_all_mppt, flag, count_input_mppt, one, onest, remains, double, double_remains, add):
    global number_mppt
    global num
    count_input_single_mppt = count_input_mppt * 2  # Число входов и выходов 1 mppt
    remains_full_mppt = count_mppt
    high_input = 2
    one_fem_offset = 4 
    
        # Распредедение модулей на каждую сторону цепочки
    if solar_count_on_the_chain % 2 != 0:
        solar_count_on_the_top_side = int(solar_count_on_the_chain/2) + 1
        solar_count_on_the_bot_side = int(solar_count_on_the_chain/2)
        blue_len = 5
    else:
        solar_count_on_the_top_side = int(solar_count_on_the_chain/2)
        solar_count_on_the_bot_side = int(solar_count_on_the_chain/2)
        blue_len = 3.5
        print("Модулей в цепочке:", solar_count_on_the_bot_side + solar_count_on_the_top_side)

    if flag <= 1:
        high_input = 2
    elif flag == 2:
        high_input = 4
        
    # забивает постепенно все верхние без Y / c Y    
    if flag == 0: 
        for i in range(double): #двойные
            num = number_mppt + i + 1
            in_dot = gen_frame_mppt(slr, num, fem_offset, count_input_single_mppt, 2)
            fem_offset -= one_fem_offset
            one_fem(slr, num, in_dot, fem_offset, solar_count_on_the_top_side, solar_count_on_the_bot_side, count_input_single_mppt, count_input_mppt*2, 2, blue_len, use_all_mppt )
            fem_offset -= count_input_single_mppt * 4
            slr.here = (0, fem_offset)
        number_mppt = num

        for i in range(double_remains): #остаток
            print(count_input_single_mppt)
            num = number_mppt + i + 1
            in_dot = gen_frame_mppt(slr, num, fem_offset, count_input_single_mppt, 2)
            fem_offset -= one_fem_offset
            one_fem(slr, num, in_dot, fem_offset, solar_count_on_the_top_side, solar_count_on_the_bot_side, count_input_single_mppt, onest, 2, blue_len, use_all_mppt )
            fem_offset -= count_input_single_mppt * 4
            slr.here = (0, fem_offset)
        number_mppt = num

        for i in range(one):
            num = number_mppt + i + 1
            in_dot = gen_frame_mppt(slr, num, fem_offset, count_input_single_mppt, flag)
            fem_offset -= one_fem_offset
            one_fem(slr, num, in_dot, fem_offset, solar_count_on_the_top_side, solar_count_on_the_bot_side, count_input_single_mppt, count_input_mppt , flag, blue_len, use_all_mppt )
            fem_offset -= count_input_single_mppt * high_input
            slr.here = (0, fem_offset)
        number_mppt = num

        for i in range(remains): #генерация mppt c остатком
            num = number_mppt + i + 1
            in_dot = gen_frame_mppt(slr, num, fem_offset, count_input_single_mppt, flag)
            fem_offset -= one_fem_offset
            one_fem(slr, num, in_dot, fem_offset, solar_count_on_the_top_side, solar_count_on_the_bot_side, count_input_single_mppt, onest, flag, blue_len, use_all_mppt )
            fem_offset -= count_input_single_mppt * high_input
            slr.here = (0, fem_offset)
        number_mppt = num

        if use_y_connector == True:
            remains = double_remains
            one = double

        for i in range(count_mppt - remains - one): #Генерирует пустые mppt
            num = number_mppt + i + 1
            in_dot = gen_frame_mppt(slr, num, fem_offset, count_input_single_mppt, flag)
            fem_offset -= one_fem_offset
            fem_offset -= count_input_single_mppt * 2
            slr.here = (0, fem_offset)
        number_mppt = num
        
    # распределяет по всем без Y
    elif flag == 1:
        for i in range(add): #полные одиночныйе
            num = number_mppt + i + 1
            in_dot = gen_frame_mppt(slr, num, fem_offset, count_input_single_mppt, 1)
            fem_offset -= one_fem_offset
            one_fem(slr, num, in_dot, fem_offset, solar_count_on_the_top_side, solar_count_on_the_bot_side, count_input_single_mppt, count_input_mppt, 0, blue_len, use_all_mppt )
            fem_offset -= count_input_single_mppt * 2
            slr.here = (0, fem_offset)
        number_mppt = num

        for i in range(remains): #остаток
            num = number_mppt + i + 1
            in_dot = gen_frame_mppt(slr, num, fem_offset, count_input_single_mppt, 0)
            fem_offset -= one_fem_offset
            one_fem(slr, num, in_dot, fem_offset, solar_count_on_the_top_side, solar_count_on_the_bot_side, count_input_single_mppt, onest, 0, blue_len, use_all_mppt )
            fem_offset -= count_input_single_mppt * high_input
            slr.here = (0, fem_offset)
        number_mppt = num

        for i in range(one): #одинаковые одиночные
            num = number_mppt + i + 1
            in_dot = gen_frame_mppt(slr, num, fem_offset, count_input_single_mppt, 0)
            fem_offset -= one_fem_offset
            one_fem(slr, num, in_dot, fem_offset, solar_count_on_the_top_side, solar_count_on_the_bot_side, count_input_single_mppt, double, 0, blue_len, use_all_mppt )
            fem_offset -= count_input_single_mppt * 2
            slr.here = (0, fem_offset)
        number_mppt = num
        
    # распределяет по всем с Y
    elif flag == 2:
        for i in range(double): #двойные
            num = number_mppt + i + 1
            in_dot = gen_frame_mppt(slr, num, fem_offset, count_input_single_mppt, flag)
            fem_offset -= one_fem_offset
            one_fem(slr, num, in_dot, fem_offset, solar_count_on_the_top_side, solar_count_on_the_bot_side, count_input_single_mppt, count_input_mppt*2, flag, blue_len, use_all_mppt )
            fem_offset -= count_input_single_mppt * high_input
            slr.here = (0, fem_offset)
        number_mppt = num

        for i in range(remains): #остаток
            num = number_mppt + i + 1
            in_dot = gen_frame_mppt(slr, num, fem_offset, count_input_single_mppt, flag)
            fem_offset -= one_fem_offset
            one_fem(slr, num, in_dot, fem_offset, solar_count_on_the_top_side, solar_count_on_the_bot_side, count_input_single_mppt, count_input_mppt + onest, flag, blue_len, use_all_mppt )
            fem_offset -= count_input_single_mppt * high_input
            slr.here = (0, fem_offset)
        number_mppt = num

        for i in range(one): #полные одиночныйе
            num = number_mppt + i + 1
            in_dot = gen_frame_mppt(slr, num, fem_offset, count_input_single_mppt, 1)
            fem_offset -= one_fem_offset
            one_fem(slr, num, in_dot, fem_offset, solar_count_on_the_top_side, solar_count_on_the_bot_side, count_input_single_mppt, count_input_mppt, 0, blue_len, use_all_mppt )
            fem_offset -= count_input_single_mppt * 2
            slr.here = (0, fem_offset)
        number_mppt = num

    all_fem = (solar_count_on_the_bot_side + solar_count_on_the_top_side) * two_num
    print("Всего модулей:", all_fem)
    return fem_offset, in_dot, all_fem

def calculation(slr, fem_offset, use_y_connector, use_all_mppt, count_diffirent_mppt, input_parametrs):
    print("")
    print("---- Изначальный массив входных параметров ----",input_parametrs)
    for i in range(count_diffirent_mppt):
        # Входные данные
        count_mppt = input_parametrs[0]# Число mppt
        count_input_mppt = input_parametrs[1] # Число входов mppt
        solar_count_on_the_chain = input_parametrs[2]  #Число фэм модулей в цепочке
        all_chain = input_parametrs[3]#  число цепочек

        # Расчет
        count_chain = all_chain // count_mppt #  число цепочек в одном MPPT
        remains_chain = all_chain % count_mppt
        max_input = count_input_mppt * count_mppt
        max_input_y = count_input_mppt * count_mppt * 2

        one = all_chain // count_input_mppt # Число необходимых mppts
        onest = all_chain % count_input_mppt # остаток
        double = 0
        double_remains = 0
        add = 0
        remains = 0

        print("Число mppt:", count_mppt)
        print("Число входов mppt:", count_input_mppt)
        print("Число фэм модулей в цепочке:", solar_count_on_the_chain)
        print("Число цепочек:", all_chain)
        print("Максимальное кол-во входов без Y коннектора:", max_input)
        print("Максимальное кол-во входов при использовании Y коннектора:", max_input_y)
        print("Кол-во цепочек в одном mppt:", count_chain)
        # print("Кол-во отстатка в цепочках", remains_chain)

        if use_y_connector == False and use_all_mppt == False and all_chain <= max_input: # забивает постепенно все верхние
            print("Без Y коннектора")
            flag = 0
            if onest == 0:
                remains = 0
            elif onest < count_input_mppt:
                remains = 1
            elif onest > count_input_mppt:
                remains = onest // count_input_mppt

        elif use_y_connector == True and use_all_mppt == False : # забивает постепенно все верхние с Y
            flag = 0
            one = 0
            remains = 0
            double = all_chain // (count_input_mppt * 2)
            double_remains = 0 if onest == 0 and double != 0 and all_chain % (count_input_mppt * 2) != count_input_mppt else 1
            onest = all_chain % (count_input_mppt * 2)

        elif use_y_connector == True and use_all_mppt == True and all_chain > max_input and all_chain <= max_input_y: # распределяет по всем с Y
            flag = 2
            if onest == 0:
                remains = 0
                double = count_mppt - (2 * count_mppt - one)
                one = 2 * count_mppt - one
            elif onest < count_input_mppt:
                remains = 1
                double = count_mppt - (2 * count_mppt - one)
                one = 2 * count_mppt - one - 1

        elif use_y_connector == False and use_all_mppt == True and all_chain <= max_input: # распределяет по всем
            flag = 1
            if remains_chain == 0:
                remains = 0
                one = count_mppt
                double = count_chain
            else:
                onest = count_chain + remains_chain
                if onest <= count_input_mppt:
                    remains = 1
                    one = count_mppt - remains
                    double = count_chain
                elif onest > count_input_mppt:
                    add = remains_chain // (count_input_mppt - count_chain)
                    remains = 0 if remains_chain % (count_input_mppt - count_chain) == 0 else 1
                    # onest = onest - count_input_mppt + count_chain
                    one = count_mppt - remains - add
                    onest = all_chain - (one * count_chain) - (add * count_input_mppt)
                    double = count_chain

        print("Одиночные цепочки:", one)
        print("Полные одиночные:", add)
        print("Двойные цепочки:", double)
        print("Доп. цепочки:", remains)
        print("Остаток:", onest)
        num_error = 0
        if all_chain < count_mppt and use_all_mppt == True:
            print("!!Кол-во цепочек меньше числа MPPT, невозможно заполгнить все MPPT!!")
            num_error = 1
            return num_error, 0
        elif all_chain > max_input and use_y_connector == False:
            print("Данное количесво цепочек не вмещается, примените Y коннекторы, либо измените конфигурацию MPPT")
            num_error = 3
            return num_error, 0
        elif all_chain <= max_input and use_y_connector == True and use_all_mppt == True:
            print("Данное количесво цепочек слишком мало чтобы заполнить все MPPT применяя Y коннекторы, уберите Y коннекторы или полное заполнение")
            num_error = 4
            return num_error, 0
        elif all_chain > max_input_y:
            print("!!Слишком большое количество цепочек!!")
            num_error = 5
            return num_error, 0

        fem_plus_chain = generate_fem(slr, solar_count_on_the_chain, fem_offset, count_mppt, count_chain, use_y_connector, use_all_mppt, flag, count_input_mppt, one, onest, remains, double, double_remains, add)
        fem_offset = fem_plus_chain[0]
        del input_parametrs[0:4]
        print("---- Массив после итерации ----",input_parametrs)
        print("")
        # fem_plus_chain.append(num_error)
    return num_error, fem_plus_chain, max_input, max_input_y

def draw(input_parametrs, parametrs, i):
    global two_num
    global number_mppt
    global num
    two_num = 0 # НОМЕР ЦЕПОЧКИ
    number_mppt = 0
    num = 0

    schemdraw.config(fontsize = 10)
    with schemdraw.Drawing(file=f'Data/Schemes/invertor{i}.svg', show=False, scale = 0.5, lw = 0.7, font = 'sans-serif') as slr:

        fem_offset = 0 # начало чертежа

        # использовать Y коннекторы Да(True) Нет(False)?
        use_y_connector = parametrs[5]

        # распределять по всем mppt(True) или оставлять пустые(False)?
        use_all_mppt = parametrs[6]

        #Режим разных mppt вкл(True)/выкл(False)
        use_different_mppt = parametrs[7]
        
        three_phase = parametrs[9]
        five_line = parametrs[10]
        len_title = parametrs[11]

        # Расчет
        count_diffirent_mppt = parametrs[8] if use_different_mppt == True else 1 # количество разных mppt
        fem_plus_chain = calculation(slr, fem_offset, use_y_connector, use_all_mppt, count_diffirent_mppt, input_parametrs)
        if fem_plus_chain[0] != 0:
            return fem_plus_chain[0], 0

        # Построение общей рамки и правой части
        slr += (bot_line_invertor := elm.Line().right().at(fem_plus_chain[1][1][-1].center, dy = -5).length(5))
        slr.here = (0, 3)

        names = [parametrs[0], f"{parametrs[1]} {str(i)}", parametrs[2], parametrs[3], parametrs[4]]
        generate_frame(slr, names, bot_line_invertor, three_phase, five_line, len_title)
        print("Чертеж построен")
        print("Всего цепочек:", two_num)

        return 0, two_num, fem_plus_chain[1][2]

