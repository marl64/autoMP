from PIL import Image, ImageOps, ImageEnhance
from pathlib import Path
import configparser

CANVAS_SIZE = (248, 168)
#SNES_WINDOW_SIZE = (256, 224)
CANVAS_OFFSET = (4, 27)

# available colors
COLORS_RGB = {
    'red': (255, 0, 0),
    'orange': (255, 132, 0),
    'yellow': (255, 255, 0),
    'lime': (0, 255, 0),
    'green': (0, 132, 66),
    'cyan': (0, 255, 255),
    'blue': (0, 0, 255),
    'rust': (198, 66, 33),
    'brown': (132, 99, 0),
    'tan': (255, 198, 132),
    'magenta': (198, 0, 198),
    'black': (0, 0, 0),
    'grey': (132, 132, 132),
    'silver': (198, 198, 198),
    'white': (255, 255, 255)
}

# valid color-representing characters for the Lua script
CHARACTER_LIST = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'
    ]

F_IN = ".\input"
F_OUT = ".\output\\"

DEFAULT_SETTINGS = """
[settings] = 
to restore all settings to default, move or delete config.txt and run automp.py
palette_select = default
----- default, greyscale, custom palette names etc.
scaling = 0
----- 0 - original, 1 - zoom, 2 - stretch
dither = 1
----- 0 - off, 1 - on
contrast_factor = 1
----- <1 - decrease contrast, 1 - default, >1 - increase contrast
brightness_factor = 1
----- <1 - decrease brightness, 1 - default, >1 - increase brightness
saturation_factor = 1
----- <1 - decrease color balance, 1 - default, >1 - increase color balance
preview_border = 1
----- 0 - off, 1 - paint screen, 2 - stamp screen, 3 - automp border, 4 and onward - custom preview borders
preview_scale = 2
----- 1 - original resolution, 2 to 5 - scaling multiplier
---------------# palettes #---------------
available colors:
----- red,orange,yellow,lime,green,cyan,blue,rust,brown,tan,magenta,black,grey,silver,white
----- separate colors with commas but no spaces
[greyscale]
colors = black,grey,silver,white
"""
CUSTOM_PALETTE_TEMPLATE = """
[example1]
colors =
[example2]
colors =
[example3]
colors =
"""
def setup_checks():
    """Check for I/O directories and config file, create them if necessary"""
    # check for input/output folders; create them if they do not exist
    Path('.\\input').mkdir(exist_ok=True)
    Path('.\\output').mkdir(exist_ok=True)

    # default settings stored here. will generate a new config file with
    # default settings if it does not already exist
    global config
    config = configparser.ConfigParser(allow_no_value=True)
    if not Path('.\\config.txt').exists():
        
        config.read_string(DEFAULT_SETTINGS+CUSTOM_PALETTE_TEMPLATE)
        with open(r".\config.txt", 'w') as config_file:
            config.write(config_file)
        

    config.read(".\\config.txt")
    return config

def palette_prep():
# import settings from config.txt, if being called as a module
    config.read(".\\config.txt")

    global config_sections
    config_sections = config.sections()
    palette_select = config['settings'].get('palette_select')

    mp_palette = COLORS_RGB
    # import custom palette settings; create new dictionary with custom colors
    if palette_select != 'default':
        pal_str = config[palette_select]['colors'].split(',')
        mp_palette = {color_str: rgb_val for (color_str, rgb_val) in COLORS_RGB.items() if color_str in pal_str}

    # palette prep
    pal_colors = list(mp_palette) 
    mp_palette = [x for y in mp_palette.values() for x in y]
    global num_colors
    num_colors = int(len(mp_palette) / 3)
    mp_palette = mp_palette + mp_palette[0:3] * (256 - num_colors)
    
    # the palette needs to be padded with duplicate colors up to 256, maybe
    # we use the first color to ensure no extra colors are added
    # this whole section could be cleaned up a lot :/

    # a palette image to use for quantization
    global pimage
    pimage = Image.new("P", (1, 1), 0)
    pimage.putpalette(mp_palette)
    # prep specific palette for drawing routine
    mpfinal = dict(zip(list(COLORS_RGB), CHARACTER_LIST))
    global final_character_list
    final_character_list = [mpfinal[x] for x in pal_colors]

def autoMP_func():

    scaling_select = config['settings'].getint('scaling')
    dither_select = config['settings'].getint('dither')
    preview_border = config['settings'].getint('preview_border')
    preview_scale = config['settings'].getint('preview_scale')
    contrast_factor = config['settings'].getfloat('contrast_factor')
    brightness_factor = config['settings'].getfloat('brightness_factor')
    saturation_factor = config['settings'].getfloat('saturation_factor')

    # convert image to correct resolution
    image = Image.open(file)
    image = image.convert("RGB")
    if scaling_select == 0:
        image.thumbnail(CANVAS_SIZE)
    elif scaling_select == 1:
        image = ImageOps.fit(image, CANVAS_SIZE)
    elif scaling_select == 2:
        image = image.resize(CANVAS_SIZE)
    else:
        image.thumbnail(CANVAS_SIZE)

    # apply image enhancements
    enhancer = ImageEnhance.Contrast(image)
    if contrast_factor != 1:
        image = enhancer.enhance(contrast_factor)
    enhancer = ImageEnhance.Brightness(image)
    if brightness_factor != 1:
        image = enhancer.enhance(brightness_factor)
    enhancer = ImageEnhance.Color(image)
    if saturation_factor != 1:
        image = enhancer.enhance(saturation_factor)
    
    # apply correct palette
    image = image.quantize(colors=num_colors,
                        palette=pimage,
                        dither=dither_select)

    preview_size = image.size
    pixel_colors = image.load()

    # save image preview
    root=file.stem
    
    # apply preview border
    if preview_border > 0:
        background = Image.open('resources\\mpborder' + str(preview_border) + '.png')
        paste_corners = [0, 0]
        for i in range(2):
            paste_corners[i] = int(
                round((CANVAS_SIZE[i] - preview_size[i]) / 2)) + CANVAS_OFFSET[i]
        background.paste(image, paste_corners)
        image = background
    else:
        pass

    # apply preview scaling
    if 1 < preview_scale < 6:
        image = image.resize(
            (image.size[0] * preview_scale, image.size[1] * preview_scale),
            resample=Image.NEAREST)
    image = image.convert("RGB") # to ensure image saves correctly
    image.save(F_OUT + root + ".png")

    # generate output string
    outstring = ""
    for i in range(0, preview_size[1]):
        for j in range(0, preview_size[0]):

            outstring += final_character_list[pixel_colors[j, i]]

    # generate a new Lua file
    lua_template = open('resources\\mariopaintFaster.lua', 'r')
    lines = lua_template.readlines()
    lines[0] = "local imagestring = \"%s\"\n" % (outstring)
    lines[1] = "local imagewidth = %d\n" % (preview_size[0])
    lines[2] = "local imageheight = %d\n" % (preview_size[1])

    lua_output = open(F_OUT + root + ".lua", 'w')
    lua_output.writelines(lines)
    lua_output.close()


if __name__=="__main__":

    setup_checks()
    palette_prep()
     # locate all relevant image files in the input folder
    for file in Path(F_IN).iterdir():
        autoMP_func()
