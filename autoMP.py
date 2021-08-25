from PIL import Image
import os
import os.path
from pathlib import Path
import configparser
from PIL import ImageOps

config=configparser.ConfigParser(allow_no_value=True)
if os.path.isfile('.\config.txt')==False:
#default settings stored here. will generate a new config file with default settings if it does not exist
    config.add_section('settings')
    config.set('settings', '#change the palette_select value to change the colour palette. 0=default, 1=greyscale, 2= your first custom palette you\'ve created below, etc')
    config.set('settings', 'palette_select', '0')
    config.set('settings','#image scaling mode. use 0 for default(aspect ratio preserved), 1 for crop and 2 for stretch')  
    config.set('settings', 'scaling', '0')
    #config.set('settings','')  #config template pair, first is description comment
    #config.set('settings', '', '')
    config.add_section('greyscale')
    config.set('greyscale','colors','black,darkgrey,lightgrey,white')
    config.set('greyscale','#add your own custom palettes here using the same format as greyscale above') 
    config.set('greyscale','#available colours are: red, orange, yellow, lightgreen, darkgreen, lightblue, darkblue, claybrown, dirtbrown, whiteskin, magenta, black, darkgrey, lightgrey, white')
    config.set('greyscale','#make sure the colors are separated with only a comma, no spaces!') 
    with open(r".\config.txt", 'w') as configfile:
        config.write(configfile)
#future config file options:
#palette white skip
#stretch to fill canvas - img.resize((248,168))
#crop to fit canvas - img.fit(img, (248, 168))
#fill canvas with colored border - pad(img, (248,168))

#import settings from config.txt
config.read(".\config.txt")
settings=config['settings']
palette_select=int(settings['palette_select'])
scaling_select=int(settings['scaling'])
config_sections=config.sections()

#available colors
colors={
'red':[255,0,0],
'orange':[255,130,0],
'yellow':[255,251,0],
'lightgreen':[0,251,0],
'darkgreen':[0,130,66],
'lightblue':[0,251,255],
'darkblue':[0,0,255],
'claybrown':[198,65,33],
'dirtbrown':[132,97,0],
'whiteskin':[255,195,132],
'magenta':[198,0,198],
'black':[0,0,0],
'darkgrey':[132,130,132],
'lightgrey':[198,195,198],
'white':[255,251,255]}

#import custom palette settings
if palette_select>0:
    testp=config[config_sections[palette_select]]
    testp=testp['colors']
    testp=testp.split(',')
    custom={x: y for (x,y) in colors.items() if x in testp}
 
#palette prep
if palette_select>0:
    colors=custom
mp_palette=colors
mp_palette=[x for l in mp_palette.values() for x in l]
numcolors=int(len(mp_palette)/3)
padding=mp_palette[0:3]*(256-numcolors)
mp_palette=mp_palette+padding
#the palette needs to be padded with duplicate colors up to 256 to work correctly :)
#we use the first color to ensure no extra colors are added
#this whole section could be cleaned up a lot :/

# a palette image to use for quantization
pimage = Image.new("P", (1, 1), 0)
pimage.putpalette(mp_palette)

#prep specific palette for drawing routine
mpcolors=['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
x=list(colors)
mpfinal=zip(x,mpcolors)
mpfinal=list(mpfinal)
mpfinal=dict(mpfinal)
check=list(colors)
mpcolors=[mpfinal[x] for x in check]

#locating all relevant image files in the input folder
dir_path = os.path.dirname(os.path.realpath(__file__))
fin=dir_path+"\input"
fout=dir_path+"\output\\"
for file in Path(fin).iterdir():

    #converting image to correct resolution
    image = Image.open(file) 
    image=image.convert("RGB")
    if scaling_select==0:
        image.thumbnail((248,168))
    elif scaling_select==1:
        image=ImageOps.fit(image, (248, 168))
    elif scaling_select==2:
        image=image.resize((248,168))
    else:
        image.thumbnail((248,168))

    #applying correct palette
    image=image.quantize(colors=numcolors, palette=pimage)

    #saving image preview
    head, tail = os.path.split(file)
    root, ext=os.path.splitext(tail)
    image.save(fout+root+".bmp")

    pix = image.load()
    outstring = ""

    #generating output string
    for i in range(0,image.size[1]):
        for j in range(0,image.size[0]):
        
           outstring+= mpcolors[pix[j, i]]
           
    #generating a new lua file
    file=open('mariopaintFaster.lua','r')
    lines=file.readlines()
    lines[0]="local imagestring = \"%s\"\n" %(outstring)
    lines[1]="local imagewidth = %d\n" %(image.size[0])
    lines[2]="local imageheight = %d\n" %(image.size[1])

    file=open(fout+root+".lua",'w')
    file.writelines(lines)
    file.close()
