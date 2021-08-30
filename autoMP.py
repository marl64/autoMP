from PIL import Image
import os
import os.path
from pathlib import Path
import configparser
from PIL import ImageOps

if os.path.isdir('.\input')==False:
    os.makedirs('.\input')
if os.path.isdir('.\output')==False:
    os.makedirs('.\output')
config=configparser.ConfigParser(allow_no_value=True)
if os.path.isfile('.\config.txt')==False:
#default settings stored here. will generate a new config file with default settings if it does not exist
    config.add_section('settings')
    config.set('settings','to restore all settings to default, move or delete config.txt and run autoMP.py')
    config.set('settings', 'palette_select', '0')
    config.set('settings','# 0 - default, 1 - greyscale, 2 and up - custom palettes')  
    config.set('settings', 'scaling', '0')
    config.set('settings','# 0 - original, 1 - zoom, 2 - stretch')  
    config.set('settings', 'dither', '1')
    config.set('settings','# 0 - off, 1 - on') 
    config.set('settings', 'preview_border', '1') 
    config.set('settings','# 0 - off, 1 - paint screen, 2 - stamp screen' ) 
    config.set('settings', 'preview_size', '2') 
    config.set('settings','# 1 - original resolution, 2 to 5 - scaling multiplier' ) 
    #config.set('settings','')  #config template pair, first is description comment
    #config.set('settings', '', '')
    config.add_section('1. greyscale')
    config.set('1. greyscale','colors','black,grey,silver,white')
    config.set('1. greyscale','---------------#custom palettes#---------------') 
    config.set('1. greyscale','available colors:')
    config.set('1. greyscale','# red, orange, yellow, lime, green, cyan, blue, rust, brown, tan, magenta, black, grey, silver, white')
    config.set('1. greyscale','separate colors with commas but no spaces')
    config.add_section('2. ')
    config.set('2. ','colors =')
    config.add_section('3. ')
    config.set('3. ','colors =')
    config.add_section('4. ')
    config.set('4. ','colors =')
    with open(r".\config.txt", 'w') as configfile:
        config.write(configfile)
#future config file options:
#palette white skip
#fill canvas with colored border - pad(img, (248,168))

#import settings from config.txt
config.read(".\config.txt")
settings=config['settings']
palette_select=int(settings['palette_select'])
scaling_select=int(settings['scaling'])
config_sections=config.sections()
dither_select=int(settings['dither'])
preview_border=int(settings['preview_border'])
preview_size=int(settings['preview_size'])
#available colors
colors={
'red':[255,0,0],
'orange':[255,132,0],
'yellow':[255,255,0],
'lime':[0,255,0],
'green':[0,132,66],
'cyan':[0,255,255],
'blue':[0,0,255],
'rust':[198,66,33],
'brown':[132,99,0],
'tan':[255,198,132],
'magenta':[198,0,198],
'black':[0,0,0],
'grey':[132,132,132],
'silver':[198,198,198],
'white':[255,255,255]}

#import custom palette settings
if palette_select>0:
    testp=config[config_sections[palette_select]]
    testp=testp['colors']
    testp=testp.split(',')
    custom={x: y for (x,y) in colors.items() if x in testp}

mp_palette=colors
#palette prep
if palette_select>0:
    mp_palette=custom
characters=mp_palette
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
check=list(characters)
mpfinal=dict(zip(list(colors),mpcolors))
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
    image=image.quantize(colors=numcolors, palette=pimage, dither=dither_select)
    sizex=image.size[0]
    sizey=image.size[1]
    pix = image.load()
    #saving image preview
    head, tail = os.path.split(file)
    root, ext=os.path.splitext(tail)

    if preview_border==1:
        background=Image.open('resources\mptemplate.png')
        cornerx=int(round((248-sizex)/2))+4
        cornery=int(round((168-sizey)/2))+27
        background.paste(image, (cornerx,cornery))
        image=background
    elif preview_border==2:
        background=Image.open('resources\mptemplate2.png')
        cornerx=int(round((248-sizex)/2))+4
        cornery=int(round((168-sizey)/2))+27
        background.paste(image, (cornerx,cornery))
        image=background
    else:
        pass
    if 1<preview_size<6:
        image=image.resize((image.size[0]*preview_size,image.size[1]*preview_size), resample=Image.NEAREST)
    image=image.convert("RGB")
    image.save(fout+root+".png")
        
    outstring = ""

    #generating output string
    for i in range(0,sizey):
        for j in range(0,sizex):
        
            outstring+= mpcolors[pix[j, i]]
        
    #generating a new lua file
    file=open('resources\mariopaintFaster.lua','r')
    lines=file.readlines()
    lines[0]="local imagestring = \"%s\"\n" %(outstring)
    lines[1]="local imagewidth = %d\n" %(sizex)
    lines[2]="local imageheight = %d\n" %(sizey)

    file=open(fout+root+".lua",'w')
    file.writelines(lines)
    file.close()
