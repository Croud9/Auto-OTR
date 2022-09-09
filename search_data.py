from queue import Empty
import fitz
import re

def search_in_txt():
    model = "Н/Д"
    title = "Н/Д"
    inputs_x_2 = "Н/Д" 
    mppt = "Н/Д" 
    with open(r"Data/Modules/Invertors/Sungrow/Sungrow_SG110CX_Pvsyst668.OND", 'r') as fp:
        for l_no, line in enumerate(fp):
            # search string
            if 'Model=' in line: model = line.split('=')[1].replace('\n', '') #Модель  
            if 'Manufacturer=' in line: title = line.split('=')[1].replace('\n', '') #Фирма  
            if 'NbInputs=' in line: inputs_x_2 = int(line.split('=')[1].replace('\n', '')) #Кол-во входов до деления
            if 'NbMPPT=' in line: mppt = int(line.split('=')[1].replace('\n', '')) #Кол-во мппт
            if 'PMaxOUT=' in line: p_max = float(line.split('=')[1].replace('\n', '')) #Максимальная мощность
            if 'IMaxAC=' in line: i_max = float(line.split('=')[1].replace('\n', '')) #Максимальный ток
            if 'Width=' in line: width = float(line.split('=')[1].replace('\n', '')) * 1000 #ширина
            if 'Height=' in line: height = float(line.split('=')[1].replace('\n', '')) * 1000 #высота
            if 'Depth=' in line: depth = float(line.split('=')[1].replace('\n', '')) * 1000 #глубина
            if 'Weight=' in line: weight = float(line.split('=')[1].replace('\n', '')) #вес
            if 'VMppMin=' in line: v_mpp_min = int(line.split('=')[1].replace('\n', '')) #напряжение минимальное
            if 'VMPPMax=' in line: v_mpp_max = int(line.split('=')[1].replace('\n', '')) #напряжение максимальное
            
            if 'TPNom=' in line: tp_nom = float(line.split('=')[1].replace('\n', '')) #температура окружающей среды
            if 'PNomConv=' in line: p_nom = float(line.split('=')[1].replace('\n', '')) #выходная мощность долговременной работы
            if 'TPLim1=' in line: tp_lim = float(line.split('=')[1].replace('\n', '')) #температура окружающей среды
            if 'PLim1=' in line: p_lim = float(line.split('=')[1].replace('\n', '')) #выходная мощность долговременной работы
            if 'TPLimAbs=' in line: tp_lim_abs = float(line.split('=')[1].replace('\n', '')) #температура окружающей среды
            if 'PLimAbs=' in line: p_lim_abs = float(line.split('=')[1].replace('\n', '')) #выходная мощность долговременной работы
            if 'MonoTri=' in line: phase = line.split('=')[1].replace('\n', '') #Фаза
            if 'VOutConv=' in line: v_out = float(line.split('=')[1].replace('\n', '')) #выходного напряжения переменного тока
            if 'IMaxAC=' in line: i_out_max = float(line.split('=')[1].replace('\n', '')) #Максимальный выходной ток
            if 'EfficMax=' in line: kpd_max = float(line.split('=')[1].replace('\n', '')) #Максимальный КПД преобразования
            if 'EfficEuro=' in line: kpd_euro = float(line.split('=')[1].replace('\n', '')) #Европейский показатель КПД
            if 'VAbsMax=' in line: v_abs_max = int(line.split('=')[1].replace('\n', '')) #Максимальное напряжение цепочки ФЭМ
            if 'Protection:' in line: protect = line.split(':')[1].replace('\n', '') #Степень защиты

    module = " ".join([title, model])
    if inputs_x_2 != "Н/Д" and mppt != "Н/Д":
        inputs = inputs_x_2 // mppt
    else:
        inputs = "Н/Д"
        
    arr = [module, inputs, mppt, p_max, i_max, width, height, depth, weight, v_mpp_min, v_mpp_max, 
           tp_nom, p_nom, tp_lim, p_lim, tp_lim_abs, p_lim_abs, phase, v_out, i_out_max, kpd_max,
           kpd_euro, v_abs_max, protect]
    print(arr)

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
            
        content_end = doc[num_page_end].get_text()
        content_begin = doc[num_page_begin].get_text()
        
        # print(content_begin.split('information')[1].split('Results')[0])
        content_end_result = content_end.split('Production')[1].split('Normalized')[0].strip("\n").replace('\n', ' ').split(' ')
        content_begin_result = content_begin.split('information')[1].split('Results')[0].strip("\n").replace('\n', ' ').split(' ')
        int_content_end_result = list(filter(lambda x: re.search('^[1-9]\d*(\.\d+)?$', x), content_end_result))
        int_content_begin_result = list(filter(lambda x: re.search('^[1-9]\d*(\.\d+)?$', x), content_begin_result))
        print(content_end_result)
        print(content_begin_result)
        print(int_content_end_result)
        print(int_content_begin_result)
        
        balances_and_main_result = content_end.split('ratio')[-1].split('Legends')[0].strip("\n").split('\n')
        print(balances_and_main_result)
        
        
search_in_txt()
search_in_pdf()