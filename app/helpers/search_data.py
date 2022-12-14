import fitz, re, traceback

def cut(line):
    return line.split('=')[1].replace('\n', '')

def null_search_params(type_file):
    if type_file == 'invertor':
        name_params = ('module', 'inputs_x_2', 'model', 'title', 'inputs', 
                        'mppt', 'p_max', 'width', 'height', 
                        'depth', 'weight', 'v_mpp_min', 'v_mpp_max', 
                        'tp_nom', 'p_nom', 'tp_lim', 'p_lim', 'tp_lim_abs', 
                        'p_lim_abs', 'phase', 'v_out', 'i_out_max', 
                        'kpd_max', 'kpd_euro', 'v_abs_max', 'protect', 'count_invertor',
                        'diff_mppt', 'broken_file')            
    elif type_file == 'pv':
        name_params = ('module_pv', 'title_pv', 'model_pv', 'width_pv','height_pv', 'depth_pv', 
                        'weight_pv', 'p_nom_pv','isc_pv', 'voc_pv', 'imp_pv', 'vmp_pv', 'square_pv',
                        'mu_isc_pv', 'mu_voc_spec_pv', 'v_max_iec_pv', 'r_shunt_pv', 'ncels_pv', 'type_pv', 'broken_file')               
    elif type_file == 'pvsyst':
        name_params = ('produced_energy', 'specific_production', 'produced_and_specific_measure_units', 'lati_pdf', 'longi_pdf', 'nb_PV', 
                        'pnom_PV', 'pnom_PV_measure_unit', 'nb_inverters', 'pnom_inverters', 'perf_ratio', 'e_grid_measure_unit', 
                        'balances_and_main', 'found_pv_invertor', 'module_area', 'months_e_grid', 'voltage_level', 'tilts_and_azimuths', 'broken_file')             
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
        try:
            found_txt['broken_file'] = False
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
        except Exception:
            found_txt['broken_file'] = True

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
        try:
            found_txt['broken_file'] = False
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
                if 'Technol=' in line: found_txt['type_pv'] = cut(line) #Тип ФЭМ

                if 'muISC=' in line: found_txt['mu_isc_pv'] = cut(line) #Напряжение при номинальной мощности
                if 'muVocSpec=' in line: found_txt['mu_voc_spec_pv'] = cut(line) #Напряжение при номинальной мощности
                if 'VMaxIEC=' in line: found_txt['v_max_iec_pv'] = cut(line) #Напряжение при номинальной мощности
                if 'RShunt=' in line: found_txt['r_shunt_pv'] = cut(line) #Напряжение при номинальной мощности
                if 'NCelS=' in line: found_txt['ncels_pv'] = cut(line) #Напряжение при номинальной мощности
        except Exception:
            found_txt['broken_file'] = True

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
    if not found_txt['mu_isc_pv'] in false_value:
        found_txt['mu_isc_pv'] = float(found_txt['mu_isc_pv']) / 1000  
    if not found_txt['mu_voc_spec_pv'] in false_value:
        found_txt['mu_voc_spec_pv'] = float(found_txt['mu_voc_spec_pv']) / 1000  
    if not found_txt['type_pv'] in false_value and found_txt['type_pv'] == 'mtHIT':
        found_txt['type_pv'] = 'HJT'
    return found_txt

def search_in_others_device(path):
    found_txt = {}
    with open(path, 'r') as fp:
        try:
            found_txt['broken_file'] = False
            input_text = fp.read().split('\n')
            for line in input_text:
                if not line:
                    pass
                else:
                    key = line.split('=')[0]
                    value = line.split('=')[1]
                    found_txt[key] = value
        except Exception:
            found_txt['broken_file'] = True
    return found_txt

def search_in_pdf(path): 
    found_pdf = null_search_params('pvsyst')
    pv_array_pages = []
    found_pv_invertor = {}

    with fitz.open(path) as doc: 
        try:
            found_pdf['broken_file'] = False
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
            for page in doc:
                content_losses = page.search_for("Vac")
                if len(content_losses) != 0:
                    num_page_losses = page.number
                    break
            for page in doc:
                content_end = page.search_for("PV Array Characteristics\n")
                if len(content_end) != 0:
                    num_page_pv_array = page.number
                    pv_array_pages.append(num_page_pv_array)

            content_begin = doc[num_page_begin].get_text()
            content_end = doc[num_page_end].get_text()
            content_losses = doc[num_page_losses].get_text()
            content_pv_array = ''
            for num in pv_array_pages:
                content = doc[num].get_text()
                content_pv_array += content.split('PV Array Characteristics')[1].split('Array losses')[0].strip("\n").replace('\n', '; ') + '; '
            
            total_pv_array = content_pv_array.split('Total PV power')[1].strip("\n").replace('\n', ' ').split('; ')
            total_pv_array_int = list(filter(lambda x: re.search('^[1-9]\d*(\.\d+)?$', x), total_pv_array))
            found_pv_invertor['total_num_pv_pdf'] = total_pv_array_int[1]
            found_pdf['module_area'] = total_pv_array_int[2]
            found_pv_invertor['total_num_invertor_pdf'] = total_pv_array_int[-2]

            content_pv_array = content_pv_array.split('Total PV power')[0].split('PV module; ')
            if not 'Manufacturer' in content_pv_array[0]:
                del content_pv_array[0]
            
            different_module = 0
            for uniq in content_pv_array:
                config_module = f'pv_array_config_{different_module}'
                found_pv_invertor[config_module] = {}

                unique_elements = uniq.split('; ')
                nom_power = list(filter(lambda x: ' kWac' in x, unique_elements)) 
                nom_power = nom_power[0].split(' ')

                if float(nom_power[0]) > 500:
                    found_pv_invertor[config_module] = f'Мощность инвертора {nom_power[0]} кВА > 500 кВА, AutoOTR пока не может обработать параметры данного инвертора и ФЭМ'
                    break

                indx_pv = unique_elements.index('(Custom parameters definition)')
                indx_invertor = unique_elements.index('(Custom parameters definition)', 6)
                title_pv = unique_elements[indx_pv - 2]
                model_pv = unique_elements[indx_pv - 1]
                title_invertor = unique_elements[indx_invertor- 2]
                model_invertor = unique_elements[indx_invertor - 1]

                found_pv_invertor[config_module][f'title_pv'] = title_pv
                found_pv_invertor[config_module][f'model_pv'] = model_pv
                found_pv_invertor[config_module][f'title_invertor'] = title_invertor
                found_pv_invertor[config_module][f'model_invertor'] = model_invertor

                mppt_elements = list(filter(lambda x: 'MPPT' in x, unique_elements)) 
                string_elements = list(filter(lambda x: 'String' in x, unique_elements)) 
                for i in range(len(mppt_elements)):
                    sub_array = f'config_{i}'
                    found_pv_invertor[config_module][sub_array] = {}

                    element = mppt_elements[i].split(' ')
                    found_pv_invertor[config_module][sub_array]['count_mppt'] = element[0]
                    found_pv_invertor[config_module][sub_array]['count_invertor'] = element[-1]

                    element = string_elements[i].split(' ')
                    found_pv_invertor[config_module][sub_array]['count_string'] = element[0]
                    found_pv_invertor[config_module][sub_array]['count_pv'] = element[-1]
                different_module += 1
            found_pdf['found_pv_invertor'] = found_pv_invertor

            situation = content_begin.split('Situation')[1].split('Project')[0].strip("\n").replace('\n', ' ').split(' ')
            situation_int = list(filter(lambda x: re.search('^[1-9]\d*(\.\d+)?$', x), situation))
            found_pdf['lati_pdf'] = situation_int[0]
            found_pdf['longi_pdf'] = situation_int[1]

            system_info = content_begin.split('Orientation')[1].split('°')[0].strip("\n").replace('\n', ' ').split(' ')
            system_info_int = list(filter(lambda x: re.search('^[+-]?[0-9]\d*(\.\d+)?$', x), system_info))

            if 'Tilts/azimuths' in system_info:
                del system_info_int[0]

            if len(system_info_int) % 2 == 0:
                i = 0
                found_pdf['tilts_and_azimuths'] = {}
                for num in range(len(system_info_int) // 2):
                    found_pdf['tilts_and_azimuths'][f"azim_{num}"] = {'tilt': int(system_info_int[i]), 'azimuth': int(system_info_int[i + 1])}
                    i += 2
            else:
                found_pdf['tilts_and_azimuths'] = 'Данные не консистентны'

            bgn_system_info = content_begin.split('information')[1].split('Results')[0].strip("\n").replace('\n', ' ').split(' ')
            bgn_system_info_int = list(filter(lambda x: re.search('^[1-9]\d*(\.\d+)?$', x), bgn_system_info))
            
            for el in bgn_system_info:
                if el.find('W') != -1:
                    found_pdf['pnom_PV_measure_unit'] = el
                    break

            found_pdf['nb_PV'] = bgn_system_info_int[0]
            found_pdf['pnom_PV'] = bgn_system_info_int[1]
            found_pdf['nb_inverters'] = bgn_system_info_int[2]
            found_pdf['pnom_inverters'] = bgn_system_info_int[3]

            main_result = content_end.split('Production')[1].split('Normalized')[0].strip("\n").replace('\n', ' ').split(' ')
            main_result_int = list(filter(lambda x: re.search('^[1-9]\d*(\.\d+)?$', x), main_result))
            main_result_P = list(filter(lambda x: re.search('P[0-9]', x), main_result))

            produced_and_specific_measure_units = []
            for el in main_result:
                if el.find('/') != -1:
                    produced_and_specific_measure_units.append(el)
            uniq = [] 
            for x in produced_and_specific_measure_units: 
                if x not in uniq: 
                    uniq.append(x) 

            found_pdf['produced_and_specific_measure_units'] = uniq

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
            month_data = found_pdf['balances_and_main']
            jan = float(month_data[month_data.index('January') + 7])
            feb = float(month_data[month_data.index('February') + 7])
            mar = float(month_data[month_data.index('March') + 7])
            apr = float(month_data[month_data.index('April') + 7])
            may = float(month_data[month_data.index('May') + 7])
            jun = float(month_data[month_data.index('June') + 7])
            jul = float(month_data[month_data.index('July') + 7])
            aug = float(month_data[month_data.index('August') + 7])
            sep = float(month_data[month_data.index('September') + 7])
            oct = float(month_data[month_data.index('October') + 7])
            nov = float(month_data[month_data.index('November') + 7])
            dec = float(month_data[month_data.index('December') + 7])
            found_pdf['months_e_grid'] = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
            e_grid_measure_unit = content_end.split('Balances')[1].split('ratio')[0].strip("\n").split('\n')
            found_pdf['e_grid_measure_unit']  = e_grid_measure_unit[-1]
            losses = content_losses.split('AC wiring losses')[1].split('Vac')[0].strip("\n").replace('\n', ' ').split(' ')
            losses_int = list(filter(lambda x: re.search('^[1-9]\d*(\.\d+)?$', x), losses))
            found_pdf['voltage_level'] = float(losses_int[0]) / 1000
        except Exception:
            traceback.print_exc()
            found_pdf['broken_file'] = True
    return found_pdf
        
# search_in_invertor("Data/Modules/Invertors/Sungrow/Sungrow_SG110CX_Pvsyst668.OND")
# search_in_pv("Data/Modules/PV's/Hevel LLC/HJT 390 m2+ (08.2020).PAN")
# print(search_in_pdf("Data/PDF in/PVsyst/PVsyst_отчет3.pdf"))
# search_in_pdf("Data/PDF in/PVsyst/PVsyst_отчет.pdf")
# print(search_in_others_device("Data/Modules/KTP's/New/КТП1.txt"))