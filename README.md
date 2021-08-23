# autoMP
Tool for converting images into a Lua script for rendering in Mario Paint

autoMP by marl

based on Automatic Mario Paint by alden

mariopaintFaster by alden

Logo artwork and readme by G-Zone (I'm helping!)

Special thanks to greysondn


What you need:

Python
The interpreter for the Python programming language, which autoMP is built with.
-> For Windows 10, open Command Prompt and type "python3", then press enter and install.

Pillow
A set of libraries for Python, required to run autoMP.
-> Open Command Prompt and type "python3 -m pip install --upgrade pip" and press enter. Then, type "python3 -m pip install --upgrade Pillow" and press enter.

SNES9x with Lua support:
This is a version of the SNES9x emulator which lets you run game-altering scripts.
-> https://github.com/TASVideos/snes9x-rr/releases/tag/snes9x-151-v7.1

Mario Paint (JU) [h1] (Joystick):
This is a modified Mario Paint ROM which uses the control pad for input rather than the SNES mouse.
-> You're on your own here! A quick web search should prove fruitful.


Setup:

Ensure that autoMP.py and mariopaintFaster.lua are in the same folder.

If they don't already exist, create 2 new folders, "input" and "output" in that folder as well.

Place the image(s) you want to use into the input folder. Pretty much any image file should work. If one isn't accepted, try saving it as a common filetype, like .jpg or .png.

Double-click autoMP.py. This should fill the output folder with preview images, as well as lua scripts for each image in your input folder.

Place the provided snes9x.cfg file in your SNES9x folder, and make sure there are 2 sub-folders named "Roms" and "Saves". Place the ROM you downloaded in the Roms folder and place the provided savestate, MarioPaintJUh1Joystick.000, in the Saves folder. Make sure both the ROM and the savestate have the same filename, minus the extentions.

Open SNES9x and load the ROM (File > Open ROM...), then load the supplied savestate (File > Load Game > Slot #0). You should now be on a blank canvas with the stamps page open at the top, with each stamp set to a single colored pixel.

Open your chosen Lua script in SNES9x (File > Lua Scripting > New Lua Scripting Window..., then browse to your output folder and select the script you want to use and click Run) and watch the image draw! Do not close the scripting window or the drawing will stop. The drawing is complete once the game returns to normal speed. 


Voila! Your automatic work of art is finished!


From here, you can create a new savestate to keep your artwork (File > Save Game), but I don't recommend saving over Slot #0. You can also perform a hard save by clicking the robot head in the bottom center and pressing save. Remember, this modified ROM uses a controller instead of the mouse for inputs. By default, the arrow keys move your cursor and the D key selects, and you can hold the A or S keys to move your cursor faster. Once the robot is done saving your file (you can speed this up by holding Tab), it will create a .srm file in your Saves folder. This .srm is compatible with unmodified Mario Paint ROMs, and you can even load it onto a flash cart, or onto an original Mario Paint  cartridge by using a Retrode, a RetroBlaster, or similar such devices. 

We hope you enjoy making lots of Mario Paint masterpieces!


Q&A

Q: Why do I have to load that savestate?

A: The stamps! Mario Paint's smallest brush size is 2x2. In order to work around this and paint with a single pixel brush, we need a custom stamp for each color in the palette which is, you guessed it, only a single pixel. To save you (and the bot) from having to make the stamps every time you want to print, you can simply load the savestate with all the stamps set up and the cursor in position, ready to draw. Plus, it saves you the trouble of catching Mario on the title screen!

Q: What is the included snes9x.cfg file for?

A: The .cfg or configuration file saves the emulator's settings. You can skip this step if you want, but I've disabled some obtrusive on-screen text and changed the default image size to 1x, which is easily resizable if you'd like. The inclusion of this .cfg is mostly for the convenience of the layman who may not be familiar with emulators. 
