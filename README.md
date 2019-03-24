# NEXTIONDisplay

![](https://img.shields.io/badge/CBPi%203%20addin-under%20development-yellow.svg)  ![](https://img.shields.io/github/license/JamFfm/NEXTIONDisplay.svg?style=flat) ![](https://img.shields.io/github/last-commit/JamFfm/NEXTIONDisplay.svg?style=flat) ![](https://img.shields.io/github/release-pre/JamFfm/NEXTIONDisplay.svg?style=flat)

Use Nextion Display on a CraftbeerPi3 instalation.

This is Alpha and not for use in production installations!

Until now code is just in a very first version with known malfunktions! Display design in alpha version!


# What for?
This addin is designed for Craftbeerpi 3.02 and will display mainly temperatures via serial connection to a Color Touch TFT. 

Does the same as the TFTDisplay addin. Have a look at the TFTDisplay addon which works via SPI connection in my repository.

![Screens](https://github.com/JamFfm/NEXTIONDisplay/blob/master/CBPi3Display/Startscreen1.jpg "Example Startscreen")

![Screens](https://github.com/JamFfm/NEXTIONDisplay/blob/master/CBPi3Display/digitmode.jpg "Example Digitscreen")

![Screens](https://github.com/JamFfm/NEXTIONDisplay/blob/master/CBPi3Display/BrewGraph.jpg "Example Waveform")

# Introduction to Nextion Displays

The Nextion displays are HMI displays which is not equal to HDMI!!
There is a Nextion editor which helps to design the Display. It is possible to build several display pages.
The amout of pages is only limited to the amount of memory.
In the Editor you can place pictures, fonts , buttons, text Lables like in Visual Studio. Just way morte simple. 
But powerful! From the Raspi side it is possible to place data to a spezial component placed on the page by the editor.
You just have to use the serial connection. To place a text in a textlabel it is like t0.txt="your Text".
To close sending you have to terminate like three times x0ff.

There is the possibility to place some logic into the display. For example place a button on a page and programm page 2 at release event. The page 2 will be displayed without the help of the Raspi.

The way to work with Nextion Displays is:

(1)-- Design the pages in the Nextion editor.

(2)-- Open the build folder (Mebnue files) and store the .tft file of your project on a SD card.

(3)-- Put the SD Card in the Display, power on, the project will be loaded.

(4)-- On Raspi side use the Serial Connection at your code to poste instructions to the display, and receive data from the display.
It is touchscreen therefor it is quite helpful to use the inputs of the display in your code.

(5)-- Be aware that all pictures and fonds have to be imported in the Editor and these have to be stored in the DISPLAY! like described in 3. You can not use pictures dynamically!! But you can change the pictures stored in the display.


You can download the Nextion Editor here:

https://nextion.itead.cc/resources/download/nextion-editor/

In this addon I use the following Display:

https://www.itead.cc/nextion-nx4832t035.html

Features include: a 3.5" TFT 480x320 resistive touch screen display, 16M Flash, 3.5KByte RAM, 65k colors.

# Wireing the display

![Wireing](https://github.com/JamFfm/NEXTIONDisplay/blob/master/CBPi3Display/MMDVM-Nextion-wiring-for-programming.jpg "BrewNextionDisplay 3.5 Zoll")

# Installation

(1)-- Power off the display. Store the .tft file via a PC/Mac on a SD Card in a fat32 system. Push the SD card in the display. Power on the display. There must be only 1 file on the card. Remove SD Card after installation.

(2)-- load the NEXTIONDisplay addin in the CraftbeerPi3 addin section (not jet available).

Workaround: Copy the NEXTIONDisplay folder to /home/pi/craftbeerpi3/modules/plugins/

(3)-- reboot at least CBPi3


Maybe the Serial connection has to be turned off at the RASPI Settings. Reboot. Go again to the RASPI Settings. Turn on the Serial Port. Turn off the Serial console.
Maybe pyserial lib has to be installed if there is an error at import serial:

In commandbox type in: python -m pip install pyserial

# Usage

# Parameter

# Knows problems

Scale is fixed so you can't see much small temp changes. Ist is an overview to the past 17 min and shows from 0-100°C.
Next versions will have a variable scale which takes into consideration of the highest and lowest temp value.
Until now Farenheit is not supported. But will be in further releases.

**Help is welcome**

# Fixed Problems

# Support

Report issues either in this Git section or at Facebook at the [Craftbeerpi group](https://www.facebook.com/groups/craftbeerpi/)






