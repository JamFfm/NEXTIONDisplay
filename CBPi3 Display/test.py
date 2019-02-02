#!/usr/bin/env python

#I found out at  JeeLabs.org that if i want as user pi want to use the serial port, that the user pi needs to have rights to it.

#sudo usermod -a -G tty pi
#will do the trick. Now logout and log back in to make this changes have effect.
#I like to reboot as the Pi is fast enough

#sudo reboot


import serial

port=serial.Serial(port="/dev/ttyAMA0", baudrate=9600, timeout=1.0)
print "schreiben"
port.write("n0.val=5")
port.write(chr(255))
port.write(255)
port.write(255)
print "ende"
