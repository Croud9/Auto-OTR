from queue import Empty
import fitz
import re

def search_in_txt():
    with open(r"Data/Modules/Sungrow/Sungrow_SG110CX_Pvsyst668.OND", 'r') as fp:
        for l_no, line in enumerate(fp):
            # search string
            if 'Model=' in line:
                model = line.split('=')[1].replace('\n', '') #Модель 
            if 'Manufacturer=' in line:
                title = line.split('=')[1].replace('\n', '') #Фирма 
            if 'NbInputs=' in line:
                inputs_x_2 = int(line.split('=')[1].replace('\n', '')) #Кол-во входов до деления 
            if 'NbMPPT=' in line:  
                mppt = int(line.split('=')[1].replace('\n', '')) #Кол-во мппт 
            if 'PMaxOUT=' in line:  
                p_max = float(line.split('=')[1].replace('\n', '')) #Максимальная мощность
            if 'IMaxAC=' in line:  
                i_max = float(line.split('=')[1].replace('\n', '')) #Максимальный ток
            if 'Width=' in line:  
                width = float(line.split('=')[1].replace('\n', '')) * 1000 #ширина
            if 'Height=' in line:  
                height = float(line.split('=')[1].replace('\n', '')) * 1000 #высота
            if 'Depth=' in line:  
                depth = float(line.split('=')[1].replace('\n', '')) * 1000 #глубина
            if 'Weight=' in line:  
                weight = float(line.split('=')[1].replace('\n', '')) #вес
            if 'VMppMin=' in line:  
                v_mpp_min = int(line.split('=')[1].replace('\n', '')) #напряжение минимальное
            if 'VMPPMax=' in line:  
                v_mpp_max = int(line.split('=')[1].replace('\n', '')) #напряжение максимальное

        
    module = " ".join([title, model])  
    inputs = inputs_x_2 // mppt
   
    arr = [module, inputs, mppt, p_max, i_max, width, height, depth, weight, v_mpp_min, v_mpp_max]
    print(arr)

def search_in_pdf():
    with fitz.open("Data/Report/PVsyst_отчет.pdf") as doc:
        for page in doc:
            text = page.search_for("January")
            if len(text) != 0:
                num_page = page.number
                break
            
        text = doc[num_page].get_text()
        
        # print(text.split('Production')[1].split('Normalized')[0])
        main_result = text.split('Production')[1].split('Normalized')[0].strip("\n").replace('\n', ' ').split(' ')
        int_main_result = list(filter(lambda x: re.search('^[1-9]\d*(\.\d+)?$', x), main_result))
        print(int_main_result)
        
        balances_and_main_result = text.split('ratio')[-1].split('Legends')[0].strip("\n").split('\n')
        print(balances_and_main_result)
        
        
search_in_txt()
# search_in_pdf()