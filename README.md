# autoMP
Tool for converting images into a Lua script for rendering in Mario Paint

autoMP by marl

based on Automatic Mario Paint by alden

mariopaintFaster by alden

Logo artwork and readme by G-Zone (I'm helping!)

Special thanks to greysondn

*This guide was written with accesibility in mind. My hope is that anyone will be able to use autoMP, even if you, like myself, are unfamiliar with things like Python and related software. It is written assuming you're using Windows 10.*


## What you need

###### autoMP
Our image converting and script writing utility. Be sure to download the latest version!\
-> https://github.com/marl64/autoMP/releases

###### Python
The interpreter for the Python programming language, which autoMP is built with.\
* In the installer, be sure that "Add Python to PATH" is checked on the first page, then click Customize installation.
* For Optional Features, leave everything checked.
* For Advanced Options, be sure to check "Decompile standard library".
-> https://www.python.org/downloads/

###### Pillow
A set of libraries for Python, required to run autoMP.\
* After installing Python as instructed above, open Command Prompt (Press the Windows key, then type cmd), then right-click and press "Run as administrator".
* Type "pip install --upgrade Pillow" and press enter.

###### SNES9x with Lua support
This is a version of the SNES9x emulator which lets you run game-altering scripts.\
-> https://github.com/TASVideos/snes9x-rr/releases/tag/snes9x-151-v7.1

###### Lunar IPS
This is a very simple utility for patching ROM files.\
-> https://fusoya.eludevisibility.org/lips/

###### Mario Paint ROM file
Mario Paint is a 1992 art program for the Super Nintendo Entertainment System/Super Famicom that came bundled with the SNES Mouse.\
-> We can't provide a source for this file. You'll have to either dump an official cartridge yourself, or obtain it some other way. A quick web search should prove fruitful.


## Setup

1. Download and extract the autoMP source code.

2. If they don't already exist, create 2 new folders, "input" and "output" in the autoMP folder.

3. Place the image(s) you want to use into the input folder. Pretty much any image file should work. If one isn't accepted, try saving it as a common filetype, like .jpg or .png.

4. Double-click autoMP.py. This should fill the output folder with preview images, as well as lua scripts for each image in your input folder.

5. Open Lunar IPS. Click "Apply IPS Patch" and browse for the patch we provided, MarioPaintJUh1Joystick.ips, then for the Mario Paint ROM you want to patch it to. This modifies your ROM to accept the gamepad rather than the mouse for inputs, which is imperative for autoMP to function properly.

6. Extract the SNES9x emulator into a seperate folder from autoMP. Place the provided snes9x.cfg file into your SNES9x folder (if there already is one, overwrite it), and make sure there are 2 sub-folders named "Roms" and "Saves". Place your patched ROM in the Roms folder and place the provided savestate, MarioPaint.000, in the Saves folder. **Make sure both your patched ROM and the savestate have the same filename. If they don't, rename one or both of them so that they match.**

7. Open SNES9x and load the ROM (File > Open ROM...), then load the supplied savestate (Press the F1 key, or go to File > Load Game > Slot #0). You should now be on a blank canvas with the stamps page open at the top, with each stamp set to a single colored pixel.

8. Load your chosen Lua script into SNES9x (Press spacebar twice, or go to File > Lua Scripting > New Lua Scripting Window..., then choose your file from the output folder), then press Run and watch the image draw! *(Note: you can press the M key to toggle the sound.)* Do not close the scripting window or the drawing will stop. The drawing is complete once the game returns to normal speed. 


Voila! Your automatic work of art is finished!


From here, you can take screenshots (press the F12 key; screenshots are saved in the SNES9x Screenshots folder by default) or create a new savestate to keep your artwork (File > Save Game), but I don't recommend saving over Slot #0. You can also perform a hard save by clicking the robot head in the bottom center and pressing save. Remember, this modified ROM uses a controller instead of the mouse for inputs. By default, the arrow keys move your cursor and the D key selects, and you can hold the A or S keys to move your cursor faster. Once the robot is done saving your file (you can speed this up by holding Tab), it will create a .srm file in your Saves folder. This .srm is compatible with unmodified Mario Paint ROMs, and you can even load it onto a flash cart, or onto an original Mario Paint cartridge by using a Retrode, a RetroBlaster, or similar such devices. 

We hope you enjoy making lots of Mario Paint masterpieces!


## Q&A

Q: Why do I have to load that savestate?

A: The stamps! Mario Paint's smallest brush size is 2x2. In order to work around this and paint with a single pixel brush, we need a custom stamp for each color in the palette which is, you guessed it, only a single pixel. To save you (and the bot) from having to make the stamps every time you want to print, you can simply load the savestate with all the stamps set up and the cursor in position, ready to draw. Plus, it saves you the trouble of catching Mario on the title screen!

Q: What is the included snes9x.cfg file for?

A: The .cfg or configuration file saves the emulator's settings. You can skip this step if you want, but I've disabled some obtrusive on-screen text, mapped the spacebar to open the Lua Script Window and the M key to toggle sound, and changed the default image size to 1x, which is easily resizable if you'd like. The inclusion of this .cfg is mostly for the convenience of the layman who may not be familiar with emulators. 

Q: I don't like how my image turned out. Can I prepare an image externally and have that turned into a Lua script?

A: Yes! You just have to make sure your image is no larger than 248x168px and that it adheres to Mario Paint's color palette. Once you have it how you like, simply put it in the input folder and run autoMP as normal. Check your preview image in the output folder, and if done correctly, it should be identical to your input image.
