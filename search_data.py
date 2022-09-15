from queue import Empty
import fitz
import re

def cut(line):
    return line.split('=')[1].replace('\n', '')

def search_in_txt():
    found_txt = {'module':'Н/Д', 'inputs_x_2':'Н/Д', 'model':'Н/Д', 'title':'Н/Д', 
        'inputs':'Н/Д', 'mppt':'Н/Д', 'p_max':'Н/Д', 'i_max':'Н/Д', 'width':'Н/Д', 
        'height':'Н/Д', 'depth':'Н/Д', 'weight':'Н/Д', 'v_mpp_min':'Н/Д', 'v_mpp_max':'Н/Д', 
        'tp_nom':'Н/Д', 'p_nom':'Н/Д', 'tp_lim':'Н/Д', 'p_lim':'Н/Д', 'tp_lim_abs':'Н/Д', 
        'p_lim_abs':'Н/Д', 'phase':'Н/Д', 'v_out':'Н/Д', 'i_out_max':'Н/Д', 'kpd_max':'Н/Д',
        'kpd_euro':'Н/Д', 'v_abs_max':'Н/Д', 'protect':'Н/Д'}

    with open(r"Data/Modules/Invertors/Sungrow/Sungrow_SG110CX_Pvsyst668.OND", 'r') as fp:
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
            if 'IMaxAC=' in line: found_txt['i_max'] = cut(line) #Максимальный ток
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
    print(found_txt)
    return found_txt

def search_in_pdf():
    with fitz.open("Data/PDF in/PVsyst/PVsyst_отчет3.pdf") as doc: 
        for page in doc:
            content_end = page.search_for("January")
            if len(content_end) != 0:
                num_page_end = page.number
                break
            
        for page in doc:
            content_begin = page.search_for("summary")
            if len(content_begin) != 0:
                num_page_begin = page.number
                break
            
        content_begin = doc[num_page_begin].get_text()
        content_end = doc[num_page_end].get_text()
        
        # print(content_begin.split('information')[1].split('Results')[0])
        content_begin_result = content_begin.split('information')[1].split('Results')[0].strip("\n").replace('\n', ' ').split(' ')
        int_content_begin_result = list(filter(lambda x: re.search('^[1-9]\d*(\.\d+)?$', x), content_begin_result))
        print(content_begin_result)
        print(int_content_begin_result)

        content_end_result = content_end.split('Production')[1].split('Normalized')[0].strip("\n").replace('\n', ' ').split(' ')
        int_content_end_result = list(filter(lambda x: re.search('^[1-9]\d*(\.\d+)?$', x), content_end_result))
        int_content = list(filter(lambda x: re.search('P[0-9]', x), content_end_result))
        print(content_end_result)
        print(int_content_end_result)
        print(int_content)
        
        balances_and_main_result = content_end.split('ratio')[-1].split('Legends')[0].strip("\n").split('\n')
        # print(balances_and_main_result)
        
        
# search_in_txt()
search_in_pdf()