# NEXTIONDisplay

![](https://img.shields.io/badge/CBPi%203%20addin-under%20development-yellow.svg)  ![](https://img.shields.io/github/license/JamFfm/NEXTIONDisplay.svg?style=flat) ![](https://img.shields.io/github/last-commit/JamFfm/NEXTIONDisplay.svg?style=flat) ![](https://img.shields.io/github/release-pre/JamFfm/NEXTIONDisplay.svg?style=flat)

Use Nextion Display on a CraftbeerPi3 installation.

This is alpha and not for use in production installations!

Until now code is just in a very first version with known malfunktions! Display design in alpha version!


# Installation

1. Power off the display. Store the .tft file in this repository via a PC/Mac on a SD Card in a fat32 system (usually SD card max 32GB). There must be only 1 file on the card. Push the SD card in the display. Power on the display. Remove SD Card after installation. Again poweroff/poweron. 
Now you see the new startscreen.

2. Load the NEXTIONDisplay addin in the CraftbeerPi3 addin section (not jet available).

    Workaround1: 

    Copy the NEXTIONDisplay folder to /home/pi/craftbeerpi3/modules/plugins/

    or

    Workaround2:

    Key in on the command box of Raspi

    git clone https://github.com/JamFfm/NEXTIONDisplay.git -b master --single-branch /home/pi/craftbeerpi3/modules/plugins/NEXTIONDisplay

3. Reboot at least CBPi3


Maybe the Serial connection has to be turned off at the RASPI Settings. Reboot. Go again to the RASPI Settings. Turn on the Serial Port. Turn off the Serial console.
Maybe pyserial lib has to be installed if there is an error at import serial:

In commandbox type in: python -m pip install pyserial


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
In the Editor you can place pictures, fonts , buttons, text labels like in Visual Studio. Just way more simple. 
But powerful! From the Raspi side it is possible to place data to a special component placed on the page by the editor.
You just have to use the serial connection. To place a text in a text labels it is like t0.txt="your Text".
To close sending you have to terminate like three times x0ff.

There is the possibility to place some logic into the display. For example place a button on a page and program page 2 at release event. The page 2 will be displayed without the help of the Raspi.

The way to work with Nextion Displays is:

1. Design the pages in the Nextion editor.

2. Open the build folder (Menu-> files) and store the .tft file of your project on a SD card.

3. Put the SD Card in the Display, power on, the project will be loaded.

4. On Raspi side use the Serial Connection at your code to poste instructions to the display, and receive data from the display.
    It is touchscreen therefor it is quite helpful to use the inputs of the display in your code.

5. Be aware that all pictures and fonds have to be imported in the Editor and these have to be stored in the DISPLAY! like described in 3. You can not use pictures dynamically!! But you can change the pictures stored in the display.


You can download the Nextion Editor here:

https://nextion.itead.cc/resources/download/nextion-editor/

In this addon I use the following display:

https://www.itead.cc/nextion-nx4832t035.html

Features include: a 3.5" TFT 480x320 resistive touch screen display, 16M Flash, 3.5KByte RAM, 65k colors.


# Wireing the display

![Wireing](https://github.com/JamFfm/NEXTIONDisplay/blob/master/CBPi3Display/MMDVM-Nextion-wiring-for-programming.jpg "BrewNextionDisplay 3.5 Zoll")


# Usage

Push the buttons in the startscreen and choose the desired screen.
1. There is a screen with big digits with current temperature and the target temperature.

2. There is a graph which will show the temperature of the past 35 min and its corresponding target temperature. Attention: If target temperature is not in the displayed range of the current temperature the target temperature is not plotted. Name of active kettle and the name of the active rest is shown.

# Parameter

Have a look in the parameters section in CraftbeerPi Gui.
All parameter with the Nextion "flag" will have influence.

NEXTION_Kettle_ID: Choose kettle (Number), NO! CBPi reboot required, default is number 1.


# Known problems

The fermenting graphs are not build up to now. This will be implemented when brewgraph is stable.

While pushing clear-button the min and max values are not deleted.

Because of a lag of knowledge the rebuild of the graph in a new temperature scale is slow. Will fix it with higher baud rate of serial connection and the NEXTION addt function in the future.

Until now fahrenheit is not supported. But will be in further releases.

**Help is welcome**


# Fixed Problems

Fixed: Scale is fixed so you can't see much small temp changes. It is an overview to the past 17 min and shows from 0-100°C.
Next versions will have a variable scale which takes into consideration of the highest and lowest temp value.

Still struggling with the ASII and UTF8. Therefore Kettle and rest- names are not implemented.

# Support

Report issues either in this Git section or at Facebook at the [Craftbeerpi group](https://www.facebook.com/groups/craftbeerpi/)

