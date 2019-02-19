#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# NextionDisplay Version 0.0.0.2
# Assembled by JamFfm
#

# sudo pip install pyserial         # install serial unlikly you have to install it because usually it is already installed
# python -m serial.tools.list_ports # List all ports in command-box
# dmesg | grep tty                  # List serial Connections
#



from modules import cbpi, app

import os, re, thread
import modules
import time
import serial

#global textCurrTemp

def writingBrewCharttoNexion(kettleID):
    

    #   Current Temperature in text field
    TextDigitTxt0 = ("%6.2f%s" % (float(Temp(kettleID)), (chr(176)+"C")))
    #global textCurrTemp
    textCurrTemp0 = str(TextDigitTxt0)
    cbpi.app.logger.info('NextionDisplay  - CurrTempBrwTxt.txt:%s' % (textCurrTemp0))
    NextionwriteString("CurrTempBrwTxt", textCurrTemp0)

    #   Target Temp in Text Field    
    TextDigitTxt1 = ("%6.2f%s" % (float(TempTargTemp(kettleID)), (chr(176)+"C")))
    textCurrTemp1 = str(TextDigitTxt1)
    cbpi.app.logger.info('NextionDisplay  - TargTempBrwTxt.txt:%s' % (textCurrTemp1))
    NextionwriteString("TargTempBrwTxt", textCurrTemp1)
    
    #   Current Kettlename in text field    
    kettlename = ("Einkocher Test")
    #kettlename = (cbpi.cache.get("kettle")[int(kettleID)].name)
    #kettlename = str(decode(str(kettlename1)))
    cbpi.app.logger.info('NextionDisplay  - KettleNameTxt.txt:%s' % (kettlename))
    #kettlename = ('%s' % (cbpi.cache.get("kettle").get(int(kettleID)).name))
    #cbpi.app.logger.info('NextionDisplay  - KettleNameTxt.txt:%s' % (kettlename))
    NextionwriteString("KettleNameTxt", kettlename)





    #   Overall factor for graphs to change resulution

    factor = 2

    #   writing current Temp to wave    
    if float(Temp(kettleID)) < 100:
        TextDigit = ("%5.2f" % (float(Temp(kettleID))*((2.2*factor)-0)))
    else:
        TextDigit = ("%6.2f" % (float(Temp(kettleID))*((2.2*factor)-0)))

    string=(str(TextDigit)[:-3])
    cbpi.app.logger.info('NextionDisplay  - CurrTempWave: %s' % (string))
    #Wave ID 2, Channnel 0, Temp as string
    NextionwriteWave(2, 0, string)

    #   writing target Temp to wave
    if float(TempTargTemp(kettleID)) < 100:
        TextDigit = ("%5.2f" % (float(TempTargTemp(kettleID))*((2.2*factor)-0)))
    else:
        TextDigit = ("%6.2f" % (float(TempTargTemp(kettleID))*((2.2*factor)-0)))
    string1=(str(TextDigit)[:-3])
    cbpi.app.logger.info('NextionDisplay  - TargetTempWave: %s' % (string1))
    #Wave ID 2, Channnel 1, Temp as string
    NextionwriteWave(2, 1, string1)

def writingDigittoNextion(kettleID):
    
    #   Current Temperature in text field
    TextDigitTxt2 = ("%6.2f%s" % (float(Temp(kettleID)), (chr(176)+"C")))
    textCurrTemp2 = str(TextDigitTxt2)
    cbpi.app.logger.info('NextionDisplay  - CurrTempTxt.txt:%s' % (textCurrTemp2))
    NextionwriteString("CurrTempTxt", textCurrTemp2)

    #   Target Temp in Text Field    
    TextDigitTxt3 = ("%6.2f%s" % (float(TempTargTemp(kettleID)), (chr(176)+"C")))
    textCurrTemp3 = str(TextDigitTxt3)
    cbpi.app.logger.info('NextionDisplay  - TargTempTxt.txt:%s' % (textCurrTemp3))
    NextionwriteString("TargetTempTxt", textCurrTemp3)
    
    #   Current Kettlenumber in text field
    Digitnumber = int(kettleID)    
    cbpi.app.logger.info('NextionDisplay  - KettleNumb.val:%s' % (Digitnumber))
    NextionwriteNumber("KettleNumb", Digitnumber)



    
    
def NextionwriteString(TextLableName, string):
    command = ('%s.txt="%s"' %(TextLableName, string))
    cbpi.app.logger.info('NextionDisplay  - command Txt:%s' % (command))
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
        )

    ser.write(command)
    ser.write(chr(255))
    ser.write(chr(255))
    ser.write(chr(255))
    ser.close()

def NextionwriteWave(WaveID, Channnel, intValue):
    command = ('add %s,%s,%s' %(WaveID, Channnel, intValue))
    cbpi.app.logger.info('NextionDisplay  - command Wave:%s' % (command))
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
        )
    
    ser.write(command)
    ser.write(chr(255))
    ser.write(chr(255))
    ser.write(chr(255))
    ser.close()

def NextionwriteNumber(NumberLableName, integer):
    command = ('%s.val=%s' %(NumberLableName, integer))
    cbpi.app.logger.info('NextionDisplay  - command Number:%s' % (command))
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
        )

    ser.write(command)
    ser.write(chr(255))
    ser.write(chr(255))
    ser.write(chr(255))
    ser.close()

#   Decoding
def decode(string):
    #html = string
    #decoded_str = string.decode("windows-1252")
    #encoded_str = decoded_str.encode("utf8")
    encoded_str = string.encode('ascii', 'ignore')
    
    cbpi.app.logger.info('NextionDisplay  - encoded_str:%s' % (encoded_str))
    
    return encoded_str


    
#def CurrentFermTemp():
    #

#def TargetFernTemp():
    #

#def KettleName():
    #
#def RestName():
    #
#def FermenterName():
    #
#def Beername():
    #


def Temp(kkid):
    #cbpi.app.logger.info("TFTDisplay  - Temp ermitteln")
    current_sensor_value_id3 = (cbpi.get_sensor_value(int(cbpi.cache.get("kettle").get(int(kkid)).sensor)))
    curTemp = ("%6.2f" % (float(current_sensor_value_id3)))
    #cbpi.app.logger.info("NEXTIONDisplay  - Temp: %s" % (curTemp))
    return curTemp



def set_parameter_id3():  
    TFTid3 = cbpi.get_config_parameter("TFT_Kettle_ID", None)
    if TFTid3 is None:
        TFTid3 = 1
        cbpi.add_config_parameter ("TFT_Kettle_ID", 1, "number", "Choose kettle (Number), NO! CBPi reboot required")      
        cbpi.app.logger.info("NEXTIONDisplay  - TFTid added: %s" % (TFTid3))
    return TFTid3

def TempTargTemp(temptargid):
    #cbpi.app.logger.info("TFTDisplay  - Target Temp ermitteln")
    current_sensor_value_temptargid = (cbpi.cache.get("kettle")[(int(temptargid))].target_temp)
    targTemp = ("%6.2f" % (float(current_sensor_value_temptargid)))
    #cbpi.app.logger.info("TFTDisplay  - TargTemp: %s" % (targTemp))
    return targTemp

@cbpi.initalizer(order=3100)
def initNexion(app):


    #end of init    
    
    @cbpi.backgroundtask(key="Nexionjob", interval=2)
    def Nexionjob(api):
        ## This is the main job

        global id3
        id3 = set_parameter_id3()
        
        writingBrewCharttoNexion(id3)

        writingDigittoNextion(id3)
 
        

            
