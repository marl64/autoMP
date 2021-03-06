import autoMP
import tkinter as tk
from tkinter import ttk
from pathlib import Path
# load config file/create it
config=autoMP.setup_checks()
config_sections=config.sections()

# setting config values for main script to use -- does not save to config file yet!!
def palette_check(self):
    config.set("settings","palette_select",palette_var.get())
def scaling_check():
    config.set("settings","scaling",scaling_var.get())
def dither_check():
    config.set("settings","dither",dither_var.get())
def contrast_check(self):
    config.set("settings","contrast_factor",contrast_var.get())
def brightness_check(self):
    config.set("settings","brightness_factor",brightness_var.get())
def saturation_check(self):
    config.set("settings","saturation_factor",saturation_var.get())
def preview_scale_check(self):
    config.set("settings","preview_scale",preview_scale_var.get())
def preview_border_check(self):
    config.set("settings","preview_border",preview_border_var.get())

path=Path.cwd()
window=tk.Tk()
window.iconphoto(False,tk.PhotoImage(file=autoMP.F_IN / 'autoMP.png'))
window.resizable(0,0)
window.title("autoMP")
main_frame=ttk.Frame()

dither_var=tk.StringVar(None,config['settings']['dither'])
scaling_var=tk.StringVar(None,config['settings']['scaling'])
palette_var=tk.StringVar(None,config['settings']['palette_select'])
contrast_var=tk.StringVar(None,config['settings']['contrast_factor'])
brightness_var=tk.StringVar(None,config['settings']['brightness_factor'])
saturation_var=tk.StringVar(None,config['settings']['saturation_factor'])
preview_scale_var=tk.StringVar(None,config['settings']['preview_scale'])
preview_border_var=tk.StringVar(None,config['settings']['preview_border'])

img_settings_frame=ttk.LabelFrame(main_frame,text="Image Settings")
preview_settings_frame=ttk.LabelFrame(main_frame,text="Preview Settings")

palette_frame=ttk.LabelFrame(img_settings_frame,text="Palette Select")
palette_list=["default"]+[x for x in config_sections[1:]]
palette_widget=ttk.Combobox(palette_frame,textvariable=palette_var,values=palette_list,state="readonly")
palette_widget.bind('<<ComboboxSelected>>',palette_check)

preview_scale_frame=ttk.LabelFrame(preview_settings_frame,text="Preview Scale")
preview_scale_list=[x for x in range(1,6)]
preview_scale_widget=ttk.Combobox(preview_scale_frame,textvariable=preview_scale_var,values=preview_scale_list,state="readonly",width=1)
preview_scale_widget.bind('<<ComboboxSelected>>',preview_scale_check)

scaling_frame=ttk.LabelFrame(img_settings_frame,text="Scaling")
scaling_widget0=ttk.Radiobutton(scaling_frame,text="Original",value="0",variable=scaling_var,command=scaling_check)
scaling_widget1=ttk.Radiobutton(scaling_frame,text="Zoom",value="1",variable=scaling_var,command=scaling_check)
scaling_widget2=ttk.Radiobutton(scaling_frame,text="Stretch",value="2",variable=scaling_var,command=scaling_check)
dither_widget=ttk.Checkbutton(
    img_settings_frame,
    text="Dithering",
    command=dither_check,
    variable=dither_var,
    onvalue=1,
    offvalue=0)

contrast_frame=ttk.LabelFrame(img_settings_frame,text="Contrast")
contrast_widget=ttk.Entry(contrast_frame,textvariable=contrast_var,width=3)
contrast_widget.bind('<FocusOut>',contrast_check)

brightness_frame=ttk.LabelFrame(img_settings_frame,text="Brightness")
brightness_widget=ttk.Entry(brightness_frame,textvariable=brightness_var,width=3)
brightness_widget.bind('<FocusOut>',brightness_check)

saturation_frame=ttk.LabelFrame(img_settings_frame,text="Saturation")
saturation_widget=ttk.Entry(saturation_frame,textvariable=saturation_var,width=3)
saturation_widget.bind('<FocusOut>',saturation_check)

preview_border_frame=ttk.LabelFrame(preview_settings_frame,text="Preview Border")
preview_border_widget=ttk.Entry(preview_border_frame,textvariable=preview_border_var,width=3)
preview_border_widget.bind('<FocusOut>',preview_border_check)

def settings_default():
    config.read_string(autoMP.DEFAULT_SETTINGS)
    with open(path / 'config.txt', 'w') as config_file:
            config.write(config_file)
    dither_var.set(config['settings']['dither'])
    scaling_var.set(config['settings']['scaling'])
    palette_var.set(config['settings']['palette_select'])
    contrast_var.set(config['settings']['contrast_factor'])
    brightness_var.set(config['settings']['brightness_factor'])
    saturation_var.set(config['settings']['saturation_factor'])
    preview_scale_var.set(config['settings']['preview_scale'])
    preview_border_var.set(config['settings']['preview_border'])

default_settings_widget=ttk.Button(text="Default Settings", command=settings_default)

def mainscript():
    with open(path / 'config.txt', 'w') as config_file:
            config.write(config_file)
    autoMP.palette_prep()
    for autoMP.file in Path(autoMP.F_IN).iterdir():
        autoMP.autoMP_func()

process_widget=ttk.Button(
    text="Process Images",
    
    command=mainscript,
   )
main_frame.pack(padx=20,pady=10)
img_settings_frame.pack(side=tk.LEFT)
palette_frame.pack()
palette_widget.pack()
scaling_frame.pack()
scaling_widget0.pack(side=tk.LEFT)
scaling_widget1.pack(side=tk.LEFT)
scaling_widget2.pack(side=tk.LEFT)
dither_widget.pack()
contrast_frame.pack()
contrast_widget.pack()
brightness_frame.pack()
brightness_widget.pack()
saturation_frame.pack()
saturation_widget.pack()
preview_settings_frame.pack(side=tk.LEFT)
preview_scale_frame.pack()
preview_scale_widget.pack()
preview_border_frame.pack()
preview_border_widget.pack()
default_settings_widget.pack(side=tk.RIGHT)
process_widget.pack()

window.mainloop()