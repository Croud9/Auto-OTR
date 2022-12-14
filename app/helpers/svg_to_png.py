import os, subprocess
from os.path import isfile, join

ink_path = 'Data/System/Inkscape/inkscape.exe'
path_svg = 'Data/Schemes/Structural/structural_for_pptx_ru.svg'
path_svg_en = 'Data/Schemes/Structural/structural_for_pptx_en.svg'
path_png = 'Data/System/Images/PPTX/'

def convert(count_invertor, wifi, widths):
    triple = count_invertor // 3
    double = count_invertor % 3 // 2
    single = count_invertor % 3 // 1 if double == 0 else 0

    height_on_slides = [0]
    height = 260

    for i in range(triple):
        if wifi == True and i == 0:
            h3 = 270 * 3
        else:
            h3 = height * 3
        height_on_slides.append(h3 + height_on_slides[-1])

    for i in range(double):
        if wifi == True and i == 0:
            h2 = 275 * 2
        else:
            h2 = height * 2
        height_on_slides.append(h2 + height_on_slides[-1])

    for i in range(single):
        if wifi == True and i == 0:
            h = 290
        else:
            h = height
        height_on_slides.append(h + height_on_slides[-1])

    files_in_general = [f for f in os.listdir(path_png) if isfile(join(path_png, f))]
    if len(files_in_general) != 0:
        for file in files_in_general:
            os.remove(path_png + f"/{file}") 

    max_widths = max(widths)
    for i in range(len(height_on_slides) - 1):
        if max_widths == 750 or max_widths == 670:
            if widths[i] == 670 or widths[i] == 750:
                start_width = 0
                width = widths[i]
            else:
                start_width = 120
                width = widths[i] + start_width
        else:
            start_width = 0
            width = widths[i]

        cmd = f'"{ink_path}" "{path_svg}" -w "{5000}" --export-area={start_width}:{height_on_slides[i]}:{width}:{height_on_slides[i + 1]} --export-background="#fff" --export-filename "{path_png}img{i}.png"' #--export-background="#fff"
        subprocess.call(cmd, shell = True)
