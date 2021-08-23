import PIL
from PIL import Image
import sys
import os
import os.path
from pathlib import Path

mp_palette= [255,0,0,255,130,0,255,251,0,0,251,0,0,130,66,0,251,255,0,0,255,198,65,33,132,9,70,255,195,132,198,0,198,0,0,0,132,130,132,198,195,198,255,251,255,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
] #the palette needs to be buffered with duplicate colours to work correctly :)

# a palette image to use for quantization
pimage = Image.new("P", (1, 1), 0)
pimage.putpalette(mp_palette)

mpcolors={}
mpcolors[0]='1' #red
mpcolors[1]='2'  #orange
mpcolors[2]='3'  #yellow
mpcolors[3]='4'  #light green
mpcolors[4]='5'  #dark green
mpcolors[5]='6'  #light blue
mpcolors[6]='7'  #dark blue
mpcolors[7]='8'  #maroon
mpcolors[8]='9'  #brown
mpcolors[9]='A'  #flesh
mpcolors[10]='B'  #purple?
mpcolors[11]='C'  #black
mpcolors[12]='D'  #dark grey
mpcolors[13]='E'  #light grey
mpcolors[14]='F'  #white

dir_path = os.path.dirname(os.path.realpath(__file__))
fin=dir_path+"\input"
fout=dir_path+"\output\\"
for file in Path(fin).iterdir():
    
    image = Image.open(file) #copy image filename here!!!
    image=image.convert("RGB")
    image.thumbnail((245,165))

    image=image.quantize(colors=15, palette=pimage)
    head, tail = os.path.split(file)
    root, ext=os.path.splitext(tail)
    image.save(fout+root+".bmp")

    pix = image.load()

    outstring = ""

    for i in range(0,image.size[1]-1):
        for j in range(0,image.size[0]-1):
        
           outstring+= mpcolors[pix[j, i]]
           
    #generating a new lua file
    file=open('mariopaintFaster.lua','r')
    lines=file.readlines()
    lines[0]="local imagestring = \"%s\"\n" %(outstring)
    lines[1]="local imagewidth = %d - 1\n" %(image.size[0])
    lines[2]="local imageheight = %d - 1\n" %(image.size[1])

    file=open(fout+root+".lua",'w')
    file.writelines(lines)
    file.close()
