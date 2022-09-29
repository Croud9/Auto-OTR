import fitz
import re

def cut(line):
    return line.split('=')[1].replace('\n', '')

def null_search_params(type_file):
    if type_file == 'invertor':
        name_params = ('module', 'inputs_x_2', 'model', 'title', 'inputs', 
                        'mppt', 'p_max', 'width', 'height', 
                        'depth', 'weight', 'v_mpp_min', 'v_mpp_max', 
                        'tp_nom', 'p_nom', 'tp_lim', 'p_lim', 'tp_lim_abs', 
                        'p_lim_abs', 'phase', 'v_out', 'i_out_max', 
                        'kpd_max', 'kpd_euro', 'v_abs_max', 'protect')               
    elif type_file == 'pv':
        name_params = ('module_pv', 'title_pv', 'model_pv', 'width_pv','height_pv', 'depth_pv', 
                        'weight_pv', 'p_nom_pv','isc_pv', 'voc_pv', 'imp_pv', 'vmp_pv', 'square_pv')               
    elif type_file == 'pvsyst':
        name_params = ('produced_energy', 'specific_production', 'lati_pdf', 'longi_pdf', 
                        'nb_PV', 'pnom_PV', 'nb_inverters', 'pnom_inverters', 'perf_ratio', 'balances_and_main')             
    elif type_file == 'weather_station':
        name_params = ('view_city', 'strt_monit', 'num_weather_station')
    elif type_file == 'weather':
        name_params = ('num_error', 'min_temp', 'date_min_temp', 'num_weather_station',
                        'max_temp', 'date_max_temp', 'all_range', 'average_temp', 'number_of_observations', 
                        'average_pressure', 'average_humidity', 'main_wind', 'average_speed_wind', 
                        'max_speed_wind', 'precipitation_on_12_hour', 'average_height_snow', 'max_height_snow', 
                        'first_date_snow', 'last_date_snow', 'climate_info')
    return dict.fromkeys(name_params, 'Н/Д')

def search_in_invertor(path):
    found_txt = null_search_params('invertor')

    with open(path, 'r') as fp:
        for l_no, line in enumerate(fp):
            if 'NbInputs=' in line: found_txt['inputs_x_2'] = cut(line) #Кол-во входов до деления int
            if 'TPLimAbs=' in line: found_txt['tp_lim_abs'] = cut(line) #температура окружающей среды
            if 'Manufacturer=' in line: found_txt['title'] = cut(line) #Фирма  
            if 'EfficEuro=' in line: found_txt['kpd_euro'] = cut(line) #Европейский показатель КПД
            if 'Protection:' in line: found_txt['protect'] = cut(line) #Степень защиты
            if 'VMppMin=' in line: found_txt['v_mpp_min'] = cut(line) #напряжение минимальное
            if 'VMPPMax=' in line: found_txt['v_mpp_max'] = cut(line) #напряжение максимальное
            if 'PLimAbs=' in line: found_txt['p_lim_abs'] = cut(line) #выходная мощность долговременной работы
            if 'VAbsMax=' in line: found_txt['v_abs_max'] = cut(line) #Максимальное напряжение цепочки ФЭМ
            if 'EfficMax=' in line: found_txt['kpd_max'] = cut(line) #Максимальный КПД преобразования
            if 'IMaxAC=' in line: found_txt['i_out_max'] = cut(line) #Максимальный выходной ток
            if 'PNomConv=' in line: found_txt['p_nom'] = cut(line) #выходная мощность долговременной работы
            if 'VOutConv=' in line: found_txt['v_out'] = cut(line) #выходного напряжения переменного тока
            if 'Height=' in line: found_txt['height'] = cut(line) # * 1000 высота float
            if 'PMaxOUT=' in line: found_txt['p_max'] = cut(line) #Максимальная мощность
            if 'Weight=' in line: found_txt['weight'] = cut(line) #вес
            if 'MonoTri=' in line: found_txt['phase'] = cut(line) #Фаза
            if 'TPLim1=' in line: found_txt['tp_lim'] = cut(line) #температура окружающей среды
            if 'TPNom=' in line: found_txt['tp_nom'] = cut(line) #температура окружающей среды
            if 'NbMPPT=' in line: found_txt['mppt'] = cut(line) #Кол-во мппт int
            if 'Width=' in line: found_txt['width'] = cut(line) # * 1000 ширина float
            if 'Depth=' in line: found_txt['depth'] = cut(line) # * 1000 глубина float
            if 'Model=' in line: found_txt['model'] = cut(line) #Модель  
            if 'PLim1=' in line: found_txt['p_lim'] = cut(line) #выходная мощность долговременной работы

    false_value = ['Н/Д', '']
    found_txt['module'] = " ".join([found_txt['title'], found_txt['model']])

    if not found_txt['mppt'] in false_value and not found_txt['inputs_x_2'] in false_value:
        found_txt['inputs'] = int(found_txt['inputs_x_2']) // int(found_txt['mppt'])
    if not found_txt['width'] in false_value:
        found_txt['width'] = float(found_txt['width']) * 1000     
    if not found_txt['height'] in false_value:
        found_txt['height'] = float(found_txt['height']) * 1000     
    if not found_txt['depth'] in false_value:
        found_txt['depth'] = float(found_txt['depth']) * 1000     
    if not found_txt['protect'] in false_value:
        found_txt['protect'] = found_txt['protect'].split(':')[1].lstrip()
    if not found_txt['phase'] in false_value:
        if found_txt['phase'] == 'Tri': found_txt['phase'] = 3
        if found_txt['phase'] == 'Mono': found_txt['phase'] = 1 
    return found_txt

def search_in_pv(path):
    found_txt = null_search_params('pv')

    with open(path, 'r') as fp:
        for l_no, line in enumerate(fp):
            if 'Manufacturer=' in line: found_txt['title_pv'] = cut(line) #Фирма  
            if 'Model=' in line: found_txt['model_pv'] = cut(line) #Модель  
            if 'Width=' in line: found_txt['width_pv'] = cut(line) # * 1000 ширина float
            if 'Height=' in line: found_txt['height_pv'] = cut(line) # * 1000 высота float
            if 'Depth=' in line: found_txt['depth_pv'] = cut(line) # * 1000 глубина float
            if 'Weight=' in line: found_txt['weight_pv'] = cut(line) #вес
            if 'PNom=' in line: found_txt['p_nom_pv'] = cut(line) #Максимальная мощность
            if 'Isc=' in line: found_txt['isc_pv'] = cut(line) #Ток короткого замыкания
            if 'Voc=' in line: found_txt['voc_pv'] = cut(line) #Напряжение холостого хода
            if 'Imp=' in line: found_txt['imp_pv'] = cut(line) #Сила тока при максимальной мощности
            if 'Vmp=' in line: found_txt['vmp_pv'] = cut(line) #Напряжение при номинальной мощности

    false_value = ['Н/Д', '']
    found_txt['module_pv'] = " ".join([found_txt['title_pv'], found_txt['model_pv']])

    if not found_txt['height_pv'] in false_value and not found_txt['width_pv'] in false_value: 
        found_txt['square_pv'] = round(float(found_txt['height_pv']) * float(found_txt['width_pv']), 3)
    if not found_txt['width_pv'] in false_value:
        found_txt['width_pv'] = float(found_txt['width_pv']) * 1000     
    if not found_txt['height_pv'] in false_value:
        found_txt['height_pv'] = float(found_txt['height_pv']) * 1000     
    if not found_txt['depth_pv'] in false_value:
        found_txt['depth_pv'] = float(found_txt['depth_pv']) * 1000  
    return found_txt

def search_in_pdf(path): 
    found_pdf = null_search_params('pvsyst')

    with fitz.open(path) as doc: 
        for page in doc:
            content_begin = page.search_for("summary")
            if len(content_begin) != 0:
                num_page_begin = page.number
                break
        for page in doc:
            content_end = page.search_for("January")
            if len(content_end) != 0:
                num_page_end = page.number
                break
                 
        content_begin = doc[num_page_begin].get_text()
        content_end = doc[num_page_end].get_text()

        situation = content_begin.split('Situation')[1].split('Project')[0].strip("\n").replace('\n', ' ').split(' ')
        situation_int = list(filter(lambda x: re.search('^[1-9]\d*(\.\d+)?$', x), situation))
        found_pdf['lati_pdf'] = situation_int[0]
        found_pdf['longi_pdf'] = situation_int[1]

        bgn_system_info = content_begin.split('information')[1].split('Results')[0].strip("\n").replace('\n', ' ').split(' ')
        bgn_system_info_int = list(filter(lambda x: re.search('^[1-9]\d*(\.\d+)?$', x), bgn_system_info))
        found_pdf['nb_PV'] = bgn_system_info_int[0]
        found_pdf['pnom_PV'] = bgn_system_info_int[1]
        found_pdf['nb_inverters'] = bgn_system_info_int[2]
        found_pdf['pnom_inverters'] = bgn_system_info_int[3]

        main_result = content_end.split('Production')[1].split('Normalized')[0].strip("\n").replace('\n', ' ').split(' ')
        main_result_int = list(filter(lambda x: re.search('^[1-9]\d*(\.\d+)?$', x), main_result))
        main_result_P = list(filter(lambda x: re.search('P[0-9]', x), main_result))

        if len(main_result_P) != 0:
            step = (len(main_result_P) // 2) 
            del main_result_P[step:]
            found_pdf['produced_energy'] = dict(zip(main_result_P, main_result_int[0:step]))
            found_pdf['specific_production'] = dict(zip(main_result_P, main_result_int[step:-1]))
            found_pdf['perf_ratio'] = main_result_int[-1]             
        else:
            found_pdf['produced_energy'] = main_result_int[0]
            found_pdf['specific_production'] = main_result_int[1]
            found_pdf['perf_ratio'] = main_result_int[2]         
        
        found_pdf['balances_and_main'] = content_end.split('ratio')[-1].split('Legends')[0].strip("\n").split('\n')
    return found_pdf
        
# search_in_invertor("Data/Modules/Invertors/Sungrow/Sungrow_SG110CX_Pvsyst668.OND")
# search_in_pv("Data/Modules/PV's/Hevel/HJT 390 m2+ (08.2020).PAN")
# search_in_pdf("Data/PDF in/PVsyst/PVsyst_отчет3.pdf")