import svgutils.transform as sg
import sys
import re
import shutil

with open('Data/Schemes/frame.svg', encoding='utf-8') as file:
    shutil.copyfileobj(file, sys.stdout)
    
background = sg.fromfile('Data/Schemes/frame.svg')
logo = sg.fromfile('Data/Schemes/connect_system.svg')

def convert_to_pixels(measurement):
    value = float(re.search(r'[0-9\.]+', measurement).group())
    if measurement.endswith("px"):
        return value
    elif measurement.endswith("mm"):
        return value * 3.7795275591
    else:
        # unit not supported
        return value

width = convert_to_pixels(background.get_size()[0])
height = convert_to_pixels(background.get_size()[1])
logo_width = convert_to_pixels(logo.get_size()[0])
logo_height = convert_to_pixels(logo.get_size()[1])

root = logo.getroot()

# Top Left
root.moveto(1, 1)

# Top Right
#root.moveto(width - logo_width - 1, 1)

# Bottom Left
#root.moveto(1, height - logo_height - 1)

# Bottom Right
#root.moveto(width - logo_width - 1, height - logo_height - 1)

background.append([root])

background.save('output.svg')