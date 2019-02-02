# NEXTIONDisplay
Use Nextion Display on a CraftbeerPi3 instalation.

This is Alpha and not for use in production installations!

Until now I wrote no code! Only Display design in alpha version!


# What for?
This addin is designed for Craftbeerpi 3.02 and will display mainly temperatures via serial connection to a Color Touch TFT. 

Does the same as the TFTDisplay addin. Have a look at the TFTDisplay addon which works via SPI connection in my pepository.

# Introduction to Nextion Displays

The Nextion displays are HMI displays which is not equal to HDMI!!
There is a Nextion editor which helps to design the Display. It is possible to build several display pages.
The amout of pages is only limited to the amount of memory.
In the Editor you can place pictures, fonts , buttons, text Lables like in Visual Studio. Just way morte simple. 
But powerful! From the Raspi side it is possible to place data to a spezial component placed on the page by the editor.
You just have to use the serial connection. To place a text in a textlabel it is like t0.txt="your Text".
To close sending you have to terminate like the times x0ff.

There is the possibility to place some logic into the display. For example place a button on a page and programm page 2 at release event. The page 2 will be displayed without the help of the Raspi.

The way to work with Nextion Displays is:

(1)-- Design the pages in the Nextion editor.

(2)-- Open the build folder (Mebnue files) and store the .tft file of your project on a SD card.

(3)-- Put the SD Card in the Display, power on, the project will be loaded.

(4)-- On Raspi Side use the Serial Connection in yout code to poste instructions to the display, and receive data from the display.
It is touchscreen therefor it is quite helpful to use the inputs of the display in your code.

(5)-- Be aware that all pictures and fonds have to be imported in the Editor and these have to be stored in the DISPLAY! like discribed in 3. You can not use pictures dynamically!!


You can download the Nextion Editor here:

https://nextion.itead.cc/resources/download/nextion-editor/

In this addon I use the following Display:

https://www.itead.cc/nextion-nx4832t035.html

Features include: a 3.5" TFT 480x320 resistive touch screen display, 16M Flash, 3.5KByte RAM, 65k colors.

# Wireing the display

![Wireing](https://github.com/JamFfm/NEXTIONDisplay/blob/master/CBPi3 Display/MMDVM-Nextion-wiring-for-programming.jpg "BrewNextionDisplay 3.5 Zoll")

# Installation

(1)-- Power off the display. Store the .tft file on a SD Card and push the SD card in the display. Power on the display. There must be only 1 file on the card. 
Remove SD Card after installation 
(2)-- load the NEXTIONDisplay addin in the Craftbeerpi addin section.

Maybe the Serical connection has to be turned on at the RASPI Settings.


# Usage

# Parameter

#Knows problems

**Help is welcome**

# Fixed Problems

# Support

Report issues either in this Git section or at Facebook at the [Craftbeerpi group](https://www.facebook.com/groups/craftbeerpi/)






