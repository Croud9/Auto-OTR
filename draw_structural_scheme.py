import schemdraw
import schemdraw.elements as elm
from schemdraw import flow
import gost_frame
import encode_file
width_box = 1.8
height_box = 1.5 
end_points = width_box / 2
length_line_between_device = 2.5

def box(slr, title):
    y_ofst = 1.25 if title == 'Анализатор' else -0.5
        
    slr += elm.Line().up().length(height_box)
    slr += (top_side_box := elm.Line().right().length(width_box))
    slr += (right_side_box := elm.Line().down().length(height_box))
    slr += (bottom_side_box := elm.Line().left().length(width_box))
    slr += elm.Label().at(top_side_box.center).label(title, ofst=(-0.1, y_ofst))
    if title == 'УЗИП' or title == 'РП':
        energy_icon(slr, right_side_box)
    return {'top': top_side_box, 'bottom': bottom_side_box, 'right': right_side_box}

def controller_and_r_yzip(slr, box_sides_inv, invertor_orange_connect, local_data):
    if local_data['right_yzip'] == True:
        slr += elm.Line().right().at(invertor_orange_connect.end).length(length_line_between_device).color('orange')
        slr += elm.Line(arrow='->').up().length(0.5).color('orange')
        slr += elm.Line().left().length(end_points / 2)

        box_sides = box(slr, 'УЗИП')
        slr += (invertor_orange_connect := elm.Line().down().at(box_sides['bottom'].center, dx = end_points / 2).length(0.5).color('orange'))
        len_to_analizer = 1.5 * length_line_between_device + end_points
        len_to_commutator = 4 * length_line_between_device - 1.15
        len_to_rp = 5 - end_points / 2
    else:
        len_to_analizer = length_line_between_device
        len_to_commutator = 2 * length_line_between_device + 1.8
        len_to_rp = 5 + end_points

    slr += elm.Line().right().at(invertor_orange_connect.end).length(length_line_between_device).color('orange')
    slr += elm.Line(arrow='->').up().length(0.5).color('orange')
    slr += elm.Line().left().length(end_points / 2)
    box_sides_rp = box(slr, 'РП')
    slr += (end_line_rp := elm.Line(arrow='->').right().at(box_sides_rp['right'].center).length(len_to_rp).color('orange'))
    slr += elm.Label().at(end_line_rp.end).label('К потребителю', ofst=(2.5, 0))

    if local_data['controller'] == True:
        slr += (invertor_controller_connect := elm.Line().down().at(box_sides_inv['bottom'].center).length(0.5).color('blue'))
        slr += elm.Line().down().at(invertor_controller_connect.end).length(3.5).color('blue')
        slr += elm.Line().right().length(length_line_between_device + end_points / 2).color('blue')
        slr += elm.Line(arrow='->').up().length(0.5).color('blue')
        slr += elm.Line().left().length(end_points / 2)
        box_sides_controller = controller_icon(slr)
        slr += (blue_connect := elm.Line().right().at(box_sides_controller['right'].center, dy = 0.25).length(0.01).color('blue'))
        
        slr += elm.Line(arrow='->').right().at(blue_connect.end).length(len_to_analizer).color('blue')
        slr += elm.Line().down().length(1.25).color('white').zorder(-1)
        slr += elm.Line().right().length(0.9).color('white').zorder(-1)
        slr += elm.Line().up().length(0.5).color('white').zorder(-1)
        slr += elm.Line().left().length(end_points)
        box_sides_analizer = box(slr, 'Анализатор')
        slr += (left_sensor := elm.Line().up().at(box_sides_analizer['top'].center, dx = -end_points / 4).length(2.35))
        slr += (right_sensor := elm.Line().up().at(box_sides_analizer['top'].center, dx = end_points / 4).length(2.35))
        slr += elm.Line(arrow = '-o').up().at(box_sides_analizer['top'].center, dx = end_points / 1.5).length(2.25)
        slr += elm.Wire('-').at(left_sensor.end).to(right_sensor.end).scale(1)
        slr += elm.Wire('n', k = 0.5, arrow='->').at(box_sides_controller['top'].center).to(box_sides_rp['bottom'].center).color('blue').scale(1)
        slr += elm.Wire('n', k = 0.5, arrow='->').at(box_sides_analizer['top'].center, dx = -end_points / 2).to(box_sides_rp['bottom'].center, dx = end_points / 2).color('blue').scale(1)
        if local_data['commutator'] == True:
            slr += (blue_connect_to_commutator := elm.Line().down().at(box_sides_controller['bottom'].center).length(0.5).color('blue'))
            slr += (end_line_commutator := elm.Line(arrow='->').right().at(blue_connect_to_commutator.end).length(len_to_commutator).color('blue'))
            slr += elm.Label().at(end_line_commutator.end).label('К коммутатору', ofst=(2.5, 0))

def net(slr, num, box_sides_inv, local_data, general_scheme_data, count_all_invertors):
    if local_data['right_yzip'] == True:
        len_to_server = 2 * length_line_between_device - 0.5
        len_to_lvs_united = 5.75
        len_to_lvs_not_united = 10.85
    else:
        len_to_server = 4
        len_to_lvs_united = 4.2 #2.85
        len_to_lvs_not_united = 8.8
    if general_scheme_data['wifi'] == False:
        if general_scheme_data['united_internet'] == True:
            slr += (internet_line := elm.Line().right().at(box_sides_inv['right'].center).length(0.5).color('green'))
            if num + 1 != count_all_invertors: 
                slr += elm.Line().down().at(internet_line.end).length(8).color('green')
            if num == 0: 
                if num + 1 == count_all_invertors: 
                    slr += elm.Line().down().at(internet_line.end).length(5.75).color('green')
                slr += (internet_line_to_server := elm.Line(arrow='->').right().at(internet_line.end, dy = -5.75).length(len_to_server).color('green'))
                
                right_side = server_icon(slr, internet_line_to_server)
                slr += (end_line_net := elm.Line(arrow='->').right().at(right_side.center).length(len_to_lvs_united).color('green'))
                slr += elm.Label().at(end_line_net.end).label('К ЛВС', ofst=(1, 0))
        else:
            slr += (internet_line := elm.Line().right().at(box_sides_inv['right'].center).length(0.5).color('green'))
            slr += elm.Line().up().at(internet_line.end).length(height_box).color('green')
            slr += (end_line_net := elm.Line(arrow='->').right().length(len_to_lvs_not_united).color('green'))
            slr += elm.Label().at(end_line_net.end).label('К ЛВС', ofst=(1, 0))
    else:
        wifi_icon(slr, box_sides_inv['right'])    

def second_pv(slr, box_sides, invertor):
    slr += (invertor_PV_connect_two := elm.Line().down().at(box_sides['bottom'].center, dx = -end_points / 3).length(0.75))
    #PV 2
    slr += elm.Line().left().at(invertor_PV_connect_two.end).length(length_line_between_device + end_points / 3)
    slr += elm.Line().down().length(0.5)
    slr += elm.Line().down().length(1.65).color('white')
    slr += elm.Line().right().length(0.25).color('white')
    pv_icon(slr, f"{invertor['total_count_pv']}")

def invertor_full_block(slr, num, local_data, general_scheme_data, invertor, count_all_invertors, all_r_yzip):
    box_sides_inv = invertor_icon(slr)
    slr += (invertor_orange_connect := elm.Line().down().at(box_sides_inv['bottom'].center, dx = end_points / 2).length(0.5).color('orange'))
    slr += (invertor_PV_connect_one := elm.Line().down().at(box_sides_inv['bottom'].center, dx = -end_points / 1.5).length(0.5))

    net(slr, num, box_sides_inv, local_data, general_scheme_data, count_all_invertors)

    if local_data['left_yzip'] == True:
        slr += elm.Line().left().at(invertor_PV_connect_one.end).length(length_line_between_device)
        slr += elm.Line().up().length(0.5)
        slr += elm.Line().left().length(end_points + end_points / 1.5)
        box_sides_yzip = box(slr, 'УЗИП')
        slr += (invertor_PV_connect_one := elm.Line().down().at(box_sides_yzip['bottom'].center, dx = -end_points / 1.5).length(0.5))
    
    #PV 1
    slr += elm.Line().left().at(invertor_PV_connect_one.end).length(length_line_between_device)
    slr += elm.Line().up().length(0.5)
    slr += elm.Line().right().length(0.25).color('white')

    pv_icon(slr, 1)

    if invertor['total_count_strings'] > 1:
        if local_data['left_yzip'] == True: 
            box_sides = box_sides_yzip 
            slr += (invertor_PV_connect_two := elm.Line().down().at(box_sides_inv['bottom'].center, dx = -end_points / 3).length(0.75))
            slr += elm.Line().down().at(box_sides_yzip['bottom'].center, dx = end_points / 3).length(0.75)
            slr += elm.Wire('-').to(invertor_PV_connect_two.end).scale(1)
        else:
            box_sides = box_sides_inv 
        second_pv(slr, box_sides, invertor)
    
    if general_scheme_data['united_energy_shield'] == True:
        if num == 0:
            controller_and_r_yzip(slr, box_sides_inv, invertor_orange_connect, local_data)
        elif num == 1 and all_r_yzip[0] == True:
            print('arrrrr')
            slr += elm.Line().right().at(invertor_orange_connect.end).length(1.5).color('orange')
            slr += (orange_up_line := elm.Line().up().length(7.75).color('orange'))
            slr += elm.Line().right().at(orange_up_line.end).length(4).color('orange') 
            slr += elm.Line().up().length(0.25).color('orange') 
        else:
            slr += elm.Line().right().at(invertor_orange_connect.end).length(1.5).color('orange')
            slr += elm.Line().up().length(8).color('orange')
    else:   
        controller_and_r_yzip(slr, box_sides_inv, invertor_orange_connect, local_data)

def server_section(slr, start_point, device='server'):
    width_line = 1.5
    if device == 'invertor':
        slr += (top_in_inv := elm.Line().left().at(start_point.center, dy = -height_box / 12, dx = -0.6).length(0.6).linewidth(width_line)) 
        slr += (bottom_in_inv := elm.Line().left().at(start_point.center, dy = -height_box / 4, dx = -0.6).length(0.6).linewidth(width_line)) 
    elif device == 'server':
        slr += (top_in_inv := elm.Line().left().at(start_point.center).length(0.6).linewidth(width_line)) 
        slr += (bottom_in_inv := elm.Line().left().at(start_point.center, dy = -height_box / 6).length(0.6).linewidth(width_line)) 

    slr += (right_in_inv := elm.Line().endpoints(top_in_inv.start, bottom_in_inv.start).linewidth(width_line)) 
    slr += elm.Line().endpoints(top_in_inv.end, bottom_in_inv.end).linewidth(width_line)
    slr += elm.Wire('-').at(top_in_inv.center, dx = 0.05).to(bottom_in_inv.center, dx = 0.05).linewidth(width_line).scale(1)
    slr += elm.Wire('-').at(top_in_inv.center, dx = -0.1).to(bottom_in_inv.center, dx = -0.1).linewidth(width_line).scale(1)
    slr += (r_line_in_inv := elm.Line().down().at(top_in_inv.center, dx = 0.15).length(0.25).linewidth(width_line).scale(1))
    slr += elm.Line().right().at(r_line_in_inv.center).length(0.15).linewidth(width_line).scale(1)
    slr += elm.Line().right().at(r_line_in_inv.center, dy = 0.0675).length(0.15).linewidth(width_line).scale(1)
    slr += elm.Line().right().at(r_line_in_inv.center, dy = -0.0675).length(0.15).linewidth(width_line).scale(1)
    return {'top': top_in_inv, 'right': right_in_inv}

def server_icon(slr, start_point):
    width_elements = 2
    slr += (dot_start := elm.Dot().linewidth(width_elements).color('white').zorder(-1)).at(start_point.end, dx = 0.6, dy = -0.2)
    server_section(slr, dot_start)
    slr += (dot := elm.Dot().at(dot_start.center, dy = 0.35).color('white').linewidth(width_elements).zorder(-1))
    sides_center_section = server_section(slr, dot)
    slr += (dot := elm.Dot().at(dot_start.center, dy = 0.7).color('white').linewidth(width_elements).zorder(-1))
    sides_up_section = server_section(slr, dot)
    slr += elm.Label().at(sides_up_section['top'].center, dy = 0.15).label('Сервер')
    return sides_center_section['right']

def energy_icon(slr, start_point):
    width_line = 1
    width_box = 1.25
    #in_style
    slr += (bottom_triangle := elm.Line().left().at(start_point.center, dy = -0.2, dx = -0.5).length(0.75).linewidth(width_line))
    slr += (dot := elm.Dot().at(bottom_triangle.center, dy = 0.5).color('white').zorder(-1).linewidth(width_line))
    slr += elm.Line().endpoints(bottom_triangle.start, dot.center).linewidth(width_line)
    slr += elm.Line().endpoints(bottom_triangle.end, dot.center).linewidth(width_line)
    slr += (center_lightning := elm.Line().left().at(bottom_triangle.center, dy = 0.2, dx = 0.05).length(0.1).linewidth(width_line))
    slr += elm.Line().at(center_lightning.start).length(0.15).theta(240).linewidth(width_line)
    slr += elm.Line().at(center_lightning.end).length(0.15).theta(60).linewidth(width_line)

def wifi_icon(slr, start_point):
    width_elements = 2
    xy_center = 0.2
    xy_down = 0.12
    slr += (dot := elm.Dot().linewidth(width_elements)).at(start_point.center, dx = 0.5)
    slr += (l := elm.Line().at(dot.center).length(0.4).theta(135).color('white').zorder(-1))
    slr += (r := elm.Line().at(dot.center).length(0.4).theta(45).color('white').zorder(-1))
    slr += flow.Arc2(arrow='-').at(l.start, dy = xy_down, dx = -xy_down).to(r.start, dy = xy_down, dx = xy_down).linewidth(width_elements).scale(1)
    slr += flow.Arc2(arrow='-').at(l.start, dy = xy_center, dx = -xy_center).to(r.start, dy = xy_center, dx = xy_center).linewidth(width_elements).scale(1)
    slr += flow.Arc2(arrow='-').at(l.end).to(r.end).linewidth(width_elements).scale(1)

def invertor_icon(slr):
    width_line = 1.5
    width_box = 1.8
    slr += elm.Line().up().length(height_box).linewidth(width_line)
    slr += (top_side_box := elm.Line().right().length(width_box).linewidth(width_line))
    slr += (right_side_box := elm.Line().down().length(height_box).linewidth(width_line))
    slr += (bottom_side_box := elm.Line().left().length(width_box).linewidth(width_line))
    slr += elm.Label().at(top_side_box.center, dy = 0.3, dx = 0.05).label('Инвертор')

    #in_style
    slr += elm.Wire('-').at(bottom_side_box.center, dx = width_box / 2 - width_box / 15).to(top_side_box.center, dx = width_box / 2 - width_box / 15).linewidth(width_line).scale(1)
    slr += elm.Wire('-').at(bottom_side_box.center, dx = -width_box / 2 + width_box / 15).to(top_side_box.center, dx = -width_box / 2 + width_box / 15).linewidth(width_line).scale(1)
    slr += elm.Line().left().at(right_side_box.center, dy = height_box / 3, dx = -0.75).length(0.3).linewidth(width_line)
    server_section(slr, right_side_box, 'invertor')
    return {'top': top_side_box, 'bottom': bottom_side_box, 'right': right_side_box}

def controller_icon(slr):
    width_line = 1.5
    width_box = 1.8
    height_box = 2
    slr += elm.Line().up().length(height_box).linewidth(width_line)
    slr += (top_side_box := elm.Line().right().length(width_box).linewidth(width_line))
    slr += (right_side_box := elm.Line().down().length(height_box).linewidth(width_line))
    slr += (bottom_side_box := elm.Line().left().length(width_box).linewidth(width_line))
    slr += elm.Label().at(top_side_box.center, dy = -1.15, dx = 0.05).label('Контроллер')

    #in_style
    slr += elm.Line().left().at(right_side_box.center, dy = -height_box / 3, dx = -0.75).length(0.3).linewidth(width_line)
    slr += elm.SourceControlled().left().at(right_side_box.center, dy = height_box / 5).fill(True).length(width_box).linewidth(width_line)
    return {'top': top_side_box, 'bottom': bottom_side_box, 'right': right_side_box}

def pv_icon(slr, count):
    width_line = 1.5
    height_panel = 0.75
    len_leg = 0.5
    len_top_line = 1
    len_bottom_line = 1.5
    
    slr += (connect := elm.Line().up().length(0.2).color('white').zorder(-1))
    slr += (leg := elm.Line().left().at(connect.end).length(len_leg).linewidth(width_line))
    slr += (leg_line := elm.Line().up().at(leg.center).length(0.25).linewidth(width_line))

    slr += (top_line := elm.Line().left().at(leg_line.end, dy = height_panel, dx = len_top_line / 2).length(len_top_line).linewidth(width_line))
    slr += elm.Label().at(top_line.center, dy = 0.25).label(f"ФЭМ {count}")
    slr += (bottom_line := elm.Line().left().at(leg_line.end, dx = len_bottom_line / 2).length(len_bottom_line).linewidth(width_line))
    slr += (far_line_r := elm.Line().at(bottom_line.start).to(top_line.start).linewidth(width_line).scale(1))
    slr += (far_line_l := elm.Line().at(bottom_line.end).to(top_line.end).linewidth(width_line).scale(1))
    # VERTICAL LINES
    slr += elm.Wire('-').at(bottom_line.center, dx = 0.15).to(top_line.center, dx = 0.15).linewidth(width_line).scale(1)
    slr += elm.Wire('-').at(bottom_line.center, dx = -0.15).to(top_line.center, dx = -0.15).linewidth(width_line).scale(1)
    slr += elm.Wire('-').at(bottom_line.center, dx = 0.45).to(top_line.center, dx = 0.35).linewidth(width_line).scale(1)
    slr += elm.Wire('-').at(bottom_line.center, dx = -0.45).to(top_line.center, dx = -0.35).linewidth(width_line).scale(1)
    slr += elm.Wire('-').at(bottom_line.center, dx = -0.45).to(top_line.center, dx = -0.35).linewidth(width_line).scale(1)
    # HORIZONTAL LINES
    slr += elm.Wire('-').at(far_line_r.center).to(far_line_l.center).linewidth(width_line).scale(1)
    slr += elm.Line().left().at(far_line_r.center, 
                                dy = height_panel / 4, dx = -0.065).length(len_bottom_line - len_bottom_line / 4).linewidth(width_line)
    slr += elm.Line().left().at(far_line_r.center, 
                                dy = -height_panel / 4, dx = +0.065).length(len_top_line + len_bottom_line / 4).linewidth(width_line)

def draw(invertors, gost_frame_params, general_scheme_data):
    schemdraw.config(fontsize = 10)  

    with schemdraw.Drawing(file=f'Data/Schemes/structural.svg', show = False, scale = 0.5, lw = 0.7) as slr:
        all_l_yzip = []
        all_r_yzip = []  
        block_offset = -8
        num = 0

        for invertor in general_scheme_data['invertor_keys']:
            local_keys = []    
            for key in invertors[invertor].keys():
                if 'local' in key:
                    local_keys.append(key)

            for local_data in local_keys:
                invertor_full_block(slr, num, invertors[invertor][local_data], general_scheme_data, 
                                    invertors[invertor], general_scheme_data['count_all_invertors'],
                                    all_r_yzip)
                slr.here = (0, block_offset)
                block_offset -= 8
                num += 1
                all_l_yzip.append(invertors[invertor][local_data]['left_yzip'])
                all_r_yzip.append(invertors[invertor][local_data]['right_yzip'])

        print(all_l_yzip)
        print(all_r_yzip)
        x_gost_ofst = -4
        width = 19 
        if True in all_l_yzip and True in all_r_yzip:
            width = 25
            x_gost_ofst = -8
        else: 
            if True in all_r_yzip:
                width = 21
            elif True in all_l_yzip:
                width = 23 
                x_gost_ofst = -8 

        height = 14 + 8 * (general_scheme_data['count_all_invertors'] - 1)
        slr.here = (x_gost_ofst, 2)

        frame_data = {'width': width, 'height': height, 'title_prjct': gost_frame_params['title_project'],
                'code_prjct': gost_frame_params['code_project'], 'type_scheme': 'Структурная схема подключения СЭС'}
        gost_frame.all_frame(slr, **frame_data)
    srcfile = 'Data/Schemes/structural.svg'
    trgfile = 'Data/Schemes/structural_codec.svg'
    encode_file.to_utf8(srcfile, trgfile)