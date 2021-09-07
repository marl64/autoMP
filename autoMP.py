from PIL import Image, ImageOps, ImageEnhance
from pathlib import Path
import configparser

CANVAS_SIZE = (248, 168)
SNES_WINDOW_SIZE = (256, 224)
CANVAS_OFFSET = (4, 27)

# available colors
COLORS_RGB = {
    'red': [255, 0, 0],
    'orange': [255, 132, 0],
    'yellow': [255, 255, 0],
    'lime': [0, 255, 0],
    'green': [0, 132, 66],
    'cyan': [0, 255, 255],
    'blue': [0, 0, 255],
    'rust': [198, 66, 33],
    'brown': [132, 99, 0],
    'tan': [255, 198, 132],
    'magenta': [198, 0, 198],
    'black': [0, 0, 0],
    'grey': [132, 132, 132],
    'silver': [198, 198, 198],
    'white': [255, 255, 255]
}
# check for input/output folders; create them if they do not exist
Path('.\\input').mkdir(exist_ok=True)
Path('.\\output').mkdir(exist_ok=True)

# default settings stored here. will generate a new config file with
# default settings if it does not already exist
config = configparser.ConfigParser(allow_no_value=True)
if not Path('.\\config.txt').exists():
    
    default_config = """
    [settings]
    to restore all settings to default, move or delete config.txt and run automp.py
    palette_select = 0
    ----- 0 - default, 1 - greyscale, 2 and up - custom palettes
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
    [1. greyscale]
    colors = black,grey,silver,white
    [2. ]
    colors =
    [3. ]
    colors =
    [4. ]
    colors =
    """
    config.read_string(default_config)
    with open(r".\config.txt", 'w') as config_file:
        config.write(config_file)

# import settings from config.txt
config.read(".\\config.txt")
config_sections = config.sections()
settings = config['settings']
palette_select = int(settings['palette_select'])
scaling_select = int(settings['scaling'])
dither_select = int(settings['dither'])
preview_border = int(settings['preview_border'])
preview_scale = int(settings['preview_scale'])
contrast_factor = float(settings['contrast_factor'])
brightness_factor = float(settings['brightness_factor'])
saturation_factor = float(settings['saturation_factor'])

mp_palette = COLORS_RGB
# import custom palette settings
if palette_select > 0:
    testp = config[config_sections[palette_select]]
    testp = testp['colors'].split(',')
    mp_palette = {color_str: rgb_value for (color_str, rgb_value) in COLORS_RGB.items() if color_str in testp}

# palette prep
characters = list(mp_palette)
mp_palette = [x for y in mp_palette.values() for x in y]

num_colors = int(len(mp_palette) / 3)
mp_palette = mp_palette + mp_palette[0:3] * (256 - num_colors)

# the palette needs to be padded with duplicate colors up to 256
# we use the first color to ensure no extra colors are added
# this whole section could be cleaned up a lot :/

# a palette image to use for quantization
pimage = Image.new("P", (1, 1), 0)
pimage.putpalette(mp_palette)

# prep specific palette for drawing routine
character_list = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'
]
mpfinal = dict(zip(list(COLORS_RGB), character_list))
character_list = [mpfinal[x] for x in characters]

# locating all relevant image files in the input folder
dir_path = str(Path.cwd())
f_in = ".\input"
f_out = ".\output\\"
for file in Path(f_in).iterdir():

    # converting image to correct resolution
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

    enhancer = ImageEnhance.Contrast(image)
    if contrast_factor != 1:
        image = enhancer.enhance(contrast_factor)
    enhancer = ImageEnhance.Brightness(image)
    if brightness_factor != 1:
        image = enhancer.enhance(brightness_factor)
    enhancer = ImageEnhance.Color(image)
    if saturation_factor != 1:
        image = enhancer.enhance(saturation_factor)
    
    # applying correct palette
    image = image.quantize(colors=num_colors,
                           palette=pimage,
                           dither=dither_select)

    preview_size = image.size
    pixel_colors = image.load()

    # saving image preview
    root=file.stem
    
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

    if 1 < preview_scale < 6:
        image = image.resize(
            (image.size[0] * preview_scale, image.size[1] * preview_scale),
            resample=Image.NEAREST)
    image = image.convert("RGB")
    image.save(f_out + root + ".png")

    # generating output string

    outstring = ""
    for i in range(0, preview_size[1]):
        for j in range(0, preview_size[0]):

            outstring += character_list[pixel_colors[j, i]]

    # generating a new lua file
    lua_template = open('resources\\mariopaintFaster.lua', 'r')
    lines = lua_template.readlines()
    lines[0] = "local imagestring = \"%s\"\n" % (outstring)
    lines[1] = "local imagewidth = %d\n" % (preview_size[0])
    lines[2] = "local imageheight = %d\n" % (preview_size[1])

    lua_output = open(f_out + root + ".lua", 'w')
    lua_output.writelines(lines)
    lua_output.close()
