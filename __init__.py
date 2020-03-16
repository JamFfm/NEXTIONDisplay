# !/usr/bin/env python
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
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# NextionDisplay Version 0.0.9.6
# Assembled by JamFfm
#
# sudo pip install pyserial         # install serial, unlikely you have to
#                                   # install it because usually it is already installed
# python -m serial.tools.list_ports # List all ports in command-box
# dmesg | grep tty                  # List serial Connections


from modules import cbpi, fermenter, app
import time
import serial
import socket                   # ip adr
import fcntl                    # ip adr
import struct                   # ip adr
from time import strftime       # Time display
from time import sleep
import threading

DEBUG = False                       # toggle writing of debug information in the app.log
TERMINATOR = bytearray([0xFF, 0xFF, 0xFF])
liste = []
listetarget = []
FERMLISTE = []
FERMLISTETARGET = []
global max_value_old
max_value_old = 0
global min_value_old
min_value_old = 0
global fmax_value_old
fmax_value_old = 0
global fmin_value_old
fmin_value_old = 0


def nx_setsys(ser, sysvar, value):  # Set system variables. sysvar as text. example: sysvar='dim'
    # Possible commands: 'bkcmd', 'dp', 'dim', 'dims', 'baud', 'bauds', 'ussp', 'thsp', 'thup', 'delay', 'sleep'
    # see instruction set of NEXTION device to see possible values for each system variable
    setdisplay = ('%s=%s' % (sysvar, str(value)))
    if DEBUG: cbpi.app.logger.info('NextionDisplay  - nx_setsys:%s' % setdisplay)
    ser.write(setdisplay)
    ser.write(TERMINATOR)


def writingDigittoNextion(ser, kettleID=1):
    unit = "°" + str(set_nextion_unit())
    ctemp = currenttemp_float(kettleID)
    #   Current Temperature in text field
    TextDigitTxt2 = ("%6.2f%s" % (ctemp, unit))  # UTF8° = U+00B0
    textCurrTemp2 = str(TextDigitTxt2)
    # if DEBUG: cbpi.app.logger.info('NextionDisplay  - digit CurrTempTxt.txt:%s' % (textCurrTemp2))
    NextionwriteString(ser, "CurrTempTxt", textCurrTemp2)

    #   Target Temp in Text Field    
    TextDigitTxt3 = ("%6.2f%s" % (float(TempTargTemp(kettleID)), unit))
    textCurrTemp3 = str(TextDigitTxt3)
    # if DEBUG: cbpi.app.logger.info('NextionDisplay  - TargTempTxt.txt:%s' % (textCurrTemp3))
    NextionwriteString(ser, "TargetTempTxt", textCurrTemp3)

    #   Current Kettlename in text field
    kname = kettlename(kettleID)
    textname = "Temperature of %s" % kname
    NextionwriteString(ser, "t3", textname)


def writing_multi_to_nextion(ser):
    unit = ("°" + str(set_nextion_unit()))
    NextionwriteString(ser, "unitMBrew", str(unit))
    stepnameMTxt = restname()
    NextionwriteString(ser, "StepnameMTxt", stepnameMTxt)

    for x in range(1, 5):
        try:
            kettle_name_field = "KettlenMTxt" + str(x)
            KettlenMTxt = kettlename(x)
            current_temp_field = "CurrMTemp" + str(x)
            CurrMTemp = ("%6.2f%s" % (currenttemp_float(x), "°"))
            target_temp_field = "TarTempMTxt" + str(x)
            TarTempMTxt = ("%6.2f%s" % (targettemp_float(x), "°"))
            heater_status_field = "heaterstatusM" + str(x)

            NextionwriteString(ser, kettle_name_field, KettlenMTxt)
            NextionwriteString(ser, current_temp_field, CurrMTemp)
            NextionwriteString(ser, target_temp_field, TarTempMTxt)

            if heater_status(x) == "on":
                if DEBUG: cbpi.app.logger.info("NextionDisplay  - writing_multi_to_nextion: heater status on")
                Nextionshowhideobject(ser, heater_status_field, "on")
            else:
                Nextionshowhideobject(ser, heater_status_field, "off")
        except:
            if DEBUG: cbpi.app.logger.info("NextionDisplay  - writing_multi_to_nextion: no Kettle %s found" % x)
            heater_status_field = "heaterstatusM" + str(x)
            Nextionshowhideobject(ser, heater_status_field, "off")
        pass
    pass

    time_remaining(ser)  # attention the name of the textfield is defined in the function  currently "remBrewTime")
    val = multiprogressbarvalue()
    Nextionprogressbar(ser, "RemainTimeMBar", val)


def Nextionshowhideobject(ser, objectname, onoff):
    if onoff == "on":
        onoff = 1
    elif onoff == "off":
        onoff = 0
    else:
        cbpi.app.logger.info("NextionDisplay  - Nextionshowhideobject onoff is not on or off:  %s" % onoff)

    if onoff == 1 or onoff == 0:
        command = ('vis %s,%s' % (objectname, onoff))
        ser.write(command)
        ser.write(TERMINATOR)
    pass


def multiprogressbarvalue():
    s = cbpi.cache.get("active_step")
    if DEBUG: cbpi.app.logger.info('NextionDisplay  - multiprogressbarvalue: %s' % s)
    try:
        if s.timer_end is not None:
            val = int(100 - (((s.timer_end - time.time()) * 100) / (s.timer*60)))
            if DEBUG: cbpi.app.logger.info('NextionDisplay  - multiprogressbarvalue: %s%s' % (val, "%"))
            return val
        else:
            if DEBUG: cbpi.app.logger.info('NextionDisplay  - multiprogressbarvalue: no timer running')
            return 0
        pass
    except:
        if DEBUG: cbpi.app.logger.info('NextionDisplay  - multiprogressbarvalue: no active step ')
        return 0
        pass
    pass


def Nextionprogressbar(ser, barname, val):
    try:
        command = ("%s.val=%s" % (barname, str(val)))
        if DEBUG: cbpi.app.logger.info('NextionDisplay  - Nextionprogressbar command Txt:%s' % command)
        ser.write(command)
        ser.write(TERMINATOR)
    except:
        cbpi.app.logger.info('NextionDisplay  - Nextionprogressbar can not convert val into string: %s' % command)
    pass


def NextionwriteString(ser, TextLableName, string):
    """
    :param ser: name of the serial connection
    :param TextLableName: name of the "textlable" on the Nextion
    :param string: the "string" to write in this lable
    use like NextionwriteString(ser, "TextLabelName", "string")
    """
    command = ('%s.txt="%s"' % (TextLableName, string))
    # if DEBUG: cbpi.app.logger.info('NextionDisplay  - command Txt:%s' % command)
    ser.write(command)
    ser.write(TERMINATOR)


def NextionwriteWave(ser, WaveID, Channnel, intValue):
    command = ('add %s,%s,%s' % (WaveID, Channnel, intValue))
    # if DEBUG: cbpi.app.logger.info('NextionDisplay  - command Wave:%s' % command)
    ser.write(command)
    ser.write(TERMINATOR)


def NextionwriteNumber(ser, NumberLableName, integer):
    command = ('%s.val=%s' % (NumberLableName, integer))
    # if DEBUG: cbpi.app.logger.info('NextionDisplay  - command Number:%s' % command)
    ser.write(command)
    ser.write(TERMINATOR)


def NextionwriteClear(ser, WaveID, channel):
    command = ('cle %s,%s' % (WaveID, channel))
    # if DEBUG: cbpi.app.logger.info('NextionDisplay  - command Number:%s' % command)
    ser.write(command)
    ser.write(TERMINATOR)


def Nextion_ref_wave(ser, stop_start):
    """
    :param ser:name of the serial connection
    :param stop_start: ether "ref_stop" or "ref_star"
    use as: ref_wave(ser, "ref_stop") or ref_wave(ser, "ref_star")
    this is like a substitude of addt Nextion function
    stops and starts refresh of wave graph
    """
    if stop_start == "ref_stop" or stop_start == "ref_star":
        command = stop_start
        ser.write(command)
        ser.write(TERMINATOR)
    else:
        cbpi.app.logger.info("NextionDisplay  - ref_wave error: stop_start not ref_stop or ref_star: %s" % stop_start)
    pass


def Nextion_refresh_wave(ser, waveid, channnel, amountofbytes, addtliste):
    """
    not used anymore because addt function is not reliable, use ref_stop or ref_star instead
    :param ser: serial object
    :param waveid: id of the wave item on the Nextion as integer
    :param channnel: channel of wave as integer
    :param amountofbytes: amount of byte equal to amount of values to send as integer
    :param addtliste: name of the list if values to send as a list
    """
    command = ('addt %s,%s,%s' % (waveid, channnel, amountofbytes))
    # if DEBUG: cbpi.app.logger.info('NextionDisplay  - command Wave:%s' % command)
    ser.write(command)
    ser.write(TERMINATOR)
    sleep(0.6)
    ser.write(addtliste)
    ser.write(TERMINATOR)


def writewave(ser, kettleID=1, erase=False, rewrite=False, dubbleline=True):
    currenttemp = currenttemp_float(kettleID)
    targettemp = targettemp_float(kettleID)
    unit = set_nextion_unit()
    #   Current Temperature in text field
    TextDigitTxt0 = ("%6.2f%s" % (currenttemp, ("°"+str(unit))))
    textCurrTemp0 = str(TextDigitTxt0)
    NextionwriteString(ser, "CurrTempBrwTxt", textCurrTemp0)
    #   Target Temp in Text Field    
    TextDigitTxt1 = ("%6.2f%s" % (targettemp, ("°"+str(unit))))
    textCurrTemp1 = str(TextDigitTxt1)
    NextionwriteString(ser, "TargTempBrwTxt", textCurrTemp1)
    #   Current Kettlename in text field    
    kettlen = kettlename(kettleID)
    NextionwriteString(ser, "KettleNameTxt", kettlen)
    #   rest name
    restn = restname()
    NextionwriteString(ser, "RestNameTxt", restn)
    #   remaining time of step
    time_remaining(ser)
    #   build liste of current temp values
    if erase is True:
        del liste[:]
    elif len(liste) < 406:  # the with of the wave object on Nextion if you change the wave-with this has to be adjusted
        liste.append(currenttemp)
    else:
        del liste[0]
        liste.append(currenttemp)
        # if DEBUG: cbpi.app.logger.info('NextionDisplay  - TempListe bigger 407:%s' % (len(liste)))
    if DEBUG: cbpi.app.logger.info('NextionDisplay  - TempListe len(liste):%s' % (len(liste)))
    # build liste of current targettemp values len(listetarget) can be different to len(liste)
    if erase is True:
        del listetarget[:]
    if len(listetarget) < 406:  # the with of the wave object on
        # Nextion if you change the wave-with this has to be adjusted
        listetarget.append(targettemp)
    else:
        del listetarget[0]
        listetarget.append(targettemp)
    # if DEBUG: cbpi.app.logger.info('NextionDisplay  - targetListe len(listetarget):%s' % (len(listetarget)))
    # min max labels for scale
    max_value = round((max(liste)+0.1), 1)
    min_value = round((min(liste)-0.1), 1)
    NextionwriteString(ser, "tmax", "%s%s" % (max_value, ("°"+str(unit))))
    NextionwriteString(ser, "tmin", "%s%s" % (min_value, ("°"+str(unit))))
    NextionwriteString(ser, "tavarage", "%s%s" % (round(((max_value+min_value)/2), 1), ("°"+str(unit))))
    # get the scaling-factor
    offset = (max_value - min_value)
    xpixel = 202  # the height of the wave object on Nextion if you change the wave-height this has to be adjusted
    factor = (xpixel / offset)
    global min_value_old
    global max_value_old
    if max_value != max_value_old or min_value != min_value_old or rewrite is True:
        if DEBUG: cbpi.app.logger.info('NextionDisplay  - rewrite')
        NextionwriteClear(ser, 1, 0)  # BrewTemp
        NextionwriteClear(ser, 1, 1)  # BrewTemp try to adjust thickness of line
        NextionwriteClear(ser, 1, 2)  # TargetTemp
        NextionwriteClear(ser, 1, 3)  # TargetTemp try to adjust thickness of line
        i = 0
        Nextion_ref_wave(ser, "ref_stop")
        while i < len(liste):
            if DEBUG: cbpi.app.logger.info('NextionDisplay  - liste:%s' % (liste[i]))
            digit = (round(float((liste[i] - min_value) * factor), 2))
            digit2 = digit + 1                          # try to adjust thickness of line
            string = (str(round(float(digit)))[:-2])
            string2 = (str(round(float(digit2)))[:-2])  # try to adjust thickness of line
            NextionwriteWave(ser, 1, 0, string)
            if dubbleline: NextionwriteWave(ser, 1, 1, string2)        # try to adjust thickness of line
            if DEBUG: cbpi.app.logger.info('NextionDisplay  - dubbleline rewrite: %s' % dubbleline)
            #  targettemp
            # if DEBUG: cbpi.app.logger.info('NextionDisplay  - listetarget:%s' % (listetarget[i]))
            target = (round(float((listetarget[i] - min_value) * factor), 2))
            target2 = target + 1
            tstring = (str(round(float(target)))[:-2])
            tstring2 = (str(round(float(target2)))[:-2])
            if 0 < target < xpixel:  # do not write target line if not in temp/screen range
                NextionwriteWave(ser, 1, 2, tstring)
                if dubbleline: NextionwriteWave(ser, 1, 3, tstring2)
                if DEBUG: cbpi.app.logger.info(
                    'NextionDisplay  - listetarget[i], target, tstring: %s, %s, %s' % (listetarget[i], target, tstring))
            pass
            if DEBUG: cbpi.app.logger.info('NextionDisplay  - liste(i), digit, string: %s, %s, %s' % (liste[i], digit, string))
            i += 1
        Nextion_ref_wave(ser, "ref_star")
    else:
        digit = (round(float((currenttemp - min_value) * factor), 2))
        digit2 = digit+1                              # try to adjust thickness of line
        string = (str(round(float(digit)))[:-2])
        string2 = (str(round(float(digit2)))[:-2])    # try to adjust thickness of line
        NextionwriteWave(ser, 1, 0, string)
        if dubbleline: NextionwriteWave(ser, 1, 1, string2)          # try to adjust thickness of line
        if DEBUG: cbpi.app.logger.info('NextionDisplay  - currenttemp, digit, string: %s, %s, %s' % (currenttemp, digit, string))
        # target Temp
        target = (round(float((targettemp - min_value) * factor), 2))
        target2 = target + 1
        tstring = (str(round(float(target)))[:-2])
        tstring2 = (str(round(float(target2)))[:-2])  # try to adjust thickness of line
        if 0 < target < xpixel:  # do not write target line if not in temp/ screen range
            NextionwriteWave(ser, 1, 2, tstring)
            if dubbleline: NextionwriteWave(ser, 1, 3, tstring2)     # try to adjust thickness of line
            if DEBUG: cbpi.app.logger.info(
                'NextionDisplay  - targettemp, target, tstring: %s, %s, %s' % (targettemp, target, tstring))
        else:
            pass
    pass
    # if DEBUG: cbpi.app.logger.info('NextionDisplay  - max and min value: %s, %s' % (max_value, min_value))

    global max_value_old
    max_value_old = max_value
    global min_value_old
    min_value_old = min_value
    return None


def writefermwave(ser, fermid=1, erase=False, frewrite=False, dubbleline=True):
    unit = set_nextion_unit()
    #   Current Temperature in text field
    cfermtemp = currentfermtemp(fermid)
    TextDigitTxt0 = ("%6.2f%s" % (cfermtemp, ("°"+str(unit))))
    textCurrTemp0 = str(TextDigitTxt0)
    NextionwriteString(ser, "CurFermTmpTxt", textCurrTemp0)
    #   Target Temp in Text Field
    tfermtemp = targetfermtemp(fermid)
    TextDigitTxt1 = ("%6.2f%s" % (tfermtemp, ("°"+str(unit))))
    textCurrTemp1 = str(TextDigitTxt1)
    NextionwriteString(ser, "targFermTmpTxt", textCurrTemp1)
    #   Current Kettlename and beername in text field
    fermn = ferm_name(fermid)
    fbeername = ferm_beername(fermid)
    displayfername = ("%s, %s" % (fermn, fbeername))
    NextionwriteString(ser, "FermNameTxt", displayfername)
    #   rest name
    fstepname = fermstepname(fermid)
    NextionwriteString(ser, "FermStepName", fstepname)
    #   remaining time of step
    fermtime_remaining(ser, fermid)
    #   build liste of current temp values
    if erase is True:
        del FERMLISTE[:]
    elif len(FERMLISTE) < 406:  # the with of the wave object on Nextion if you change the wave-with this has to be
        # adjusted
        FERMLISTE.append(cfermtemp)
    else:
        del FERMLISTE[0]
        FERMLISTE.append(cfermtemp)
    if DEBUG: cbpi.app.logger.info('NextionDisplay  - fermTempListe len(liste):%s' % (len(FERMLISTE)))
    # build liste of current targettemp values len(listetarget) can be different to len(liste)
    if erase is True:
        del FERMLISTETARGET[:]
    if len(FERMLISTETARGET) < 406:  # the with of the wave object on
        # Nextion if you change the wave with this has to be adjusted
        FERMLISTETARGET.append(tfermtemp)
    else:
        del FERMLISTETARGET[0]
        FERMLISTETARGET.append(tfermtemp)
    # if DEBUG: cbpi.app.logger.info('NextionDisplay  - targetListe len(FERMLISTETARGET):%s' % (len(FERMLISTETARGET)))
    # min max labels for scale
    fmax_value = round((max(FERMLISTE)+0.1), 1)
    fmin_value = round((min(FERMLISTE)-0.1), 1)
    NextionwriteString(ser, "tfermmax", "%s%s" % (fmax_value, ("°"+str(unit))))
    NextionwriteString(ser, "tfermmin", "%s%s" % (fmin_value, ("°"+str(unit))))
    NextionwriteString(ser, "tfermavarage", "%s%s" % (round(((fmax_value+fmin_value)/2), 1), ("°"+str(unit))))
    # get the scaling-factor
    offset = (fmax_value - fmin_value)
    xpixel = 202  # the height of the wave object on Nextion if you change the wave height this has to be adjusted
    ffactor = (xpixel / offset)
    global fmin_value_old
    global fmax_value_old
    if fmax_value != fmax_value_old or fmin_value != fmin_value_old or frewrite is True:
        if DEBUG: cbpi.app.logger.info('NextionDisplay  - fermenter rewrite')
        NextionwriteClear(ser, 5, 0)  # BrewTemp
        NextionwriteClear(ser, 5, 1)  # BrewTemp bold line
        NextionwriteClear(ser, 5, 2)  # TargetTemp
        NextionwriteClear(ser, 5, 3)  # TargetTemp bold line
        i = 0
        Nextion_ref_wave(ser, "ref_stop")
        while i < len(FERMLISTE):
            # if DEBUG: cbpi.app.logger.info('NextionDisplay  - FERMLISTE:%s' % (FERMLISTE[i]))
            digit = (round(float((FERMLISTE[i] - fmin_value) * ffactor), 2))
            digit2 = digit + 1
            string = (str(round(float(digit)))[:-2])
            string2 = (str(round(float(digit2)))[:-2])
            NextionwriteWave(ser, 5, 0, string)
            if dubbleline: NextionwriteWave(ser, 5, 1, string2)        # try to adjust thickness of line
            if DEBUG: cbpi.app.logger.info('NextionDisplay  - dubbleline fermenter rewrite: %s' % dubbleline)
            #  targettemp
            # if DEBUG: cbpi.app.logger.info('NextionDisplay  - FERMLISTETARGET:%s' % (FERMLISTETARGET[i]))
            target = (round(float((FERMLISTETARGET[i] - fmin_value) * ffactor), 2))
            targetbold = target + 1
            tstring = (str(round(float(target)))[:-2])
            tstringbold = (str(round(float(targetbold)))[:-2])
            if 0 < target < xpixel:  # do not write target line if not in temp/screen range
                NextionwriteWave(ser, 5, 2, tstring)
                if dubbleline: NextionwriteWave(ser, 5, 3, tstringbold)  # try to adjust thickness of line
                if DEBUG: cbpi.app.logger.info(
                    'NextionDisplay  - fermlistetarget[i], target, tstring: %s, %s, %s' % (FERMLISTETARGET[i], target, tstring))
            pass
            if DEBUG: cbpi.app.logger.info('NextionDisplay  - FERMLISTE(i), digit, string: %s, %s, %s' % (FERMLISTE[i], digit, string))
            i += 1
        Nextion_ref_wave(ser, "ref_star")
    else:
        digit = (round(float((cfermtemp - fmin_value) * ffactor), 2))
        digitbold = digit + 1
        if digit != 0:      # prevent digit from becoming zero
            string = (str(round(float(digit)))[:-2])
            stringbold = (str(round(float(digitbold)))[:-2])
            NextionwriteWave(ser, 5, 0, string)
            if dubbleline: NextionwriteWave(ser, 5, 1, stringbold)
        pass
        if DEBUG: cbpi.app.logger.info('NextionDisplay  - currentfermtemp, digit, string: %s, %s, %s' % (cfermtemp, digit, string))
        # target Temp
        target = (round(float((tfermtemp - fmin_value) * ffactor), 2))
        targetbold = target + 1
        tstring = (str(round(float(target)))[:-2])
        tstringbold = (str(round(float(targetbold)))[:-2])
        if 0 < target < xpixel:  # do not write target line if not in temp/ screen range
            NextionwriteWave(ser, 5, 2, tstring)
            if dubbleline: NextionwriteWave(ser, 5, 3, tstringbold)
            if DEBUG: cbpi.app.logger.info(
                'NextionDisplay  - targettemp, target, tstring: %s, %s, %s' % (tfermtemp, target, tstring))
        else:
            pass
    pass
    # if DEBUG: cbpi.app.logger.info('NextionDisplay  - max and min value: %s, %s' % (max_value, min_value))

    global fmax_value_old
    fmax_value_old = fmax_value
    global fmin_value_old
    fmin_value_old = fmin_value
    return None


def cbidecode(string):
    # if DEBUG: cbpi.app.logger.info('NextionDisplay  - string:%s' % string)
    udata=string.encode("utf-8")
    asciidata=udata.decode("utf-8", "ignore")
    # if DEBUG: cbpi.app.logger.info('NextionDisplay  - encoded_str:%s' % (asciidata))
    return asciidata.encode("utf-8")


def time_remaining(ser):
    s = cbpi.cache.get("active_step")
    try:
        if s.timer_end is not None:
            time_remain = time.strftime("%H:%M:%S", time.gmtime(s.timer_end - time.time()))
            if DEBUG: cbpi.app.logger.info('NextionDisplay  - time_remaining:%s %s %s' % (s.timer_end, time.time(), s.timer))
            NextionwriteString(ser, "remBrewTime", time_remain)
        else:
            NextionwriteString(ser, "remBrewTime", "")
        pass
    except:
        NextionwriteString(ser, "remBrewTime", "")
    pass


def time_remaining1(ser):
    while True:
        s = cbpi.cache.get("active_step")
        try:
            if s.timer_end is not None:
                time_remain = time.strftime("%H:%M:%S", time.gmtime(s.timer_end - time.time()))
                if DEBUG: cbpi.app.logger.info('NextionDisplay  - time_remaining:%s %s %s' % (s.timer_end, time.time(), s.timer))
                NextionwriteString(ser, "remBrewTime", time_remain)
            else:
                NextionwriteString(ser, "remBrewTime", "")
            pass
        except:
            NextionwriteString(ser, "remBrewTime", "")
        pass
    pass
# todo: seems not to be used

def fermtime_remaining(ser, fermid):
    try:
        if cbpi.cache.get("fermenter_task")[(int(fermid))].timer_start is not None:
            ftimeremain = (cbpi.cache.get("fermenter_task").get(fermid).timer_start - time.time())
            ftimeremain = interval(ftimeremain)
            # if DEBUG: cbpi.app.logger.info('NextionDisplay  - fermstepname:%s' % ftimeremain)
            NextionwriteString(ser, "remainfer", ftimeremain)
        else:
            NextionwriteString(ser, "remainfer", "")
        pass
    except:
        NextionwriteString(ser, "remainfer", "")


def set_nextion_unit():
    try:
        nx_unit = cbpi.get_config_parameter("unit", None)
        return nx_unit
    except:
        pass
    pass


def fermstepname(fermid):
    if is_fermenter_step_running() == "active":
        try:
            fstepname = cbpi.cache.get("fermenter_task")[(int(fermid))].name
            fstepname = cbidecode(fstepname)
            if DEBUG: cbpi.app.logger.info('NextionDisplay  - fermstepname:%s' % fstepname)
            return fstepname
        except:
            if DEBUG: cbpi.app.logger.info('NextionDisplay  - fermstepname not runnig?')
            return "error"
            pass
    else:
        return "no active ferm step"


def is_fermenter_step_running():
    for key, value2 in cbpi.cache["fermenter_task"].items():
        if value2.state == "A":
            return "active"
        else:
            pass


def currentfermtemp(fermid):
    # read the current temperature of fermenter with fermenter ID from parameters
    current_sensor_value_ferm = (cbpi.get_sensor_value(int(cbpi.cache.get("fermenter").get(fermid).sensor)))
    if DEBUG: cbpi.app.logger.info('NextionDisplay  - currentfermtemp.txt:%s' % current_sensor_value_ferm)
    return current_sensor_value_ferm


def targetfermtemp(fermid):
    # cbpi.app.logger.info("NEXTIONDisplay  - Target Temp detect")
    current_sensor_value_temptargid = cbpi.cache.get("fermenter")[(int(fermid))].target_temp
    # targfermTemp = ("%6.2f" % (float(current_sensor_value_temptargid)))
    if DEBUG: cbpi.app.logger.info("NEXTIONDisplay  - TargfermTemp: %s" % current_sensor_value_temptargid)
    return current_sensor_value_temptargid


def currenttemp_float(kettleID):
    temp = float(Temp(kettleID))
    return temp


def targettemp_float(kettleID):
    targettemp = float(TempTargTemp(kettleID))
    return targettemp


def heater_status(kettleid):
    heater_of_kettle = int(cbpi.cache.get("kettle").get(kettleid).heater)
    heater_status_of_kettle = int(cbpi.cache.get("actors").get(heater_of_kettle).state)
    if heater_status_of_kettle == 1:
        return "on"
    else:
        return "off"
    pass


def ferm_name(fermid):
    try:
        fname = ('%s' % cbpi.cache.get("fermenter").get(fermid).name)
        fname = cbidecode(fname)
        # if DEBUG: cbpi.app.logger.info('NextionDisplay  - ferm_name:%s' % fname)
        return fname
    except:
        return "not found"
    pass


def ferm_beername(fermid):
    try:
        beername = cbpi.cache.get("fermenter").get(fermid).brewname
        beername = cbidecode(beername)
        # if DEBUG: cbpi.app.logger.info('NextionDisplay  - ferm_beername:%s' % beername)
        return beername
    except:
        return "not found"
    pass


def kettlename(kettleID):
    brewkettlename = ('%s' % cbpi.cache.get("kettle").get(int(kettleID)).name)
    # if DEBUG: cbpi.app.logger.info('NextionDisplay  - KettleNameTxt.txt:%s' % (brewkettlename))
    brewkettlename = cbidecode(brewkettlename)
    # if DEBUG: cbpi.app.logger.info('NextionDisplay  - decodeKettleNameTxt.txt:%s' % (brewkettlename))
    return brewkettlename


def restname():
    s = cbpi.cache.get("active_step")
    if s is not None:
        try:
            brewrestname = s.name
            # if DEBUG: cbpi.app.logger.info('NextionDisplay  - brewrestname:%s' % (brewrestname))
            brewrestname = cbidecode(brewrestname)
            return brewrestname
        except:
            pass
            return "restart not detected"

    else:
        return "no active rest"
    pass


def Temp(kkid):
    # if DEBUG: cbpi.app.logger.info("NEXTIONDisplay  - Temp detect")
    current_sensor_value_id3 = (cbpi.get_sensor_value(int(cbpi.cache.get("kettle").get(int(kkid)).sensor)))
    curTemp = ("%6.2f" % (float(current_sensor_value_id3)))
    # if DEBUG: cbpi.app.logger.info("NEXTIONDisplay  - Temp: %s" % (curTemp))
    return curTemp


def TempTargTemp(temptargid):
    # if DEBUG: cbpi.app.logger.info("NEXTIONDisplay  - Target Temp detect")
    current_sensor_value_temptargid = cbpi.cache.get("kettle")[(int(temptargid))].target_temp
    targTemp = ("%6.2f" % (float(current_sensor_value_temptargid)))
    # if DEBUG: cbpi.app.logger.info("NEXTIONDisplay  - TargTemp: %s" % (targTemp))
    return targTemp


def get_ip(interface):
    ip_addr = "Not connected"
    so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        ip_addr = socket.inet_ntoa(fcntl.ioctl(so.fileno(), 0x8915, struct.pack('256s', interface[:15]))[20:24])
    finally:
        pass
    return ip_addr


def set_ip():
    if get_ip('wlan0') != 'Not connected':
        ip = get_ip('wlan0')
    elif get_ip('eth0') != 'Not connected':
        ip = get_ip('eth0')
    elif get_ip('enxb827eb488a6e') != 'Not connected':
        ip = get_ip('enxb827eb488a6e')
    else:
        ip = 'Not connected'
    pass
    return ip


def get_version_fo(path):
    version = ""
    try:
        if path is not "":
            fo = open(path, "r")
        else:
            fo = open("/home/pi/craftbeerpi3/config/version.yaml", "r")
        version = fo.read()
        fo.close()
    finally:
        return version


def interval(seconds):
    """
    gives back interval as tuple
    @return: (weeks, days, hours, minutes, seconds)
    formats string for fermtime_remaining
    returns the formatted string for text-field
    """
    WEEK = 60 * 60 * 24 * 7
    DAY = 60 * 60 * 24
    HOUR = 60 * 60
    MINUTE = 60

    weeks = seconds // WEEK
    seconds = seconds % WEEK
    days = seconds // DAY
    seconds = seconds % DAY
    hours = seconds // HOUR
    seconds = seconds % HOUR
    minutes = seconds // MINUTE
    seconds = seconds % MINUTE

    if weeks >= 1:
        remaining_time = ("Week:%d Days:%d Hours:%02d:%02d" % (int(weeks), int(days), int(hours), int(minutes)))
        return remaining_time
    elif weeks == 0 and days >= 1:
        remaining_time = ("Days:%d Hours:%02d:%02d:%02d" % (int(days), int(hours), int(minutes), int(seconds)))
        return remaining_time
    elif weeks == 0 and days == 0:
        remaining_time = ("Hours:%02d:%02d:%02d" % (int(hours), int(minutes), int(seconds)))
        return remaining_time
    else:
        pass
    pass


def set_parameter_kettleID():
    kettleid = cbpi.get_config_parameter("NEXTION_Kettle_ID", None)
    if kettleid is None:
        kettleid = 1
        cbpi.add_config_parameter("NEXTION_Kettle_ID", 1, "kettle", "Select kettle (Number), NO! CBPi reboot required")
        cbpi.app.logger.info("NEXTIONDisplay - KettleID added: %s" % kettleid)
    return kettleid


def set_parameter_fermID():
    fermid = cbpi.get_config_parameter("NEXTION_Fermenter_ID", None)
    if fermid is None:
        fermid = 1
        cbpi.add_config_parameter("NEXTION_Fermenter_ID", 1, "number", "Select Fermenter (Number), NO! CBPi reboot required")
        cbpi.app.logger.info("NEXTIONDisplay - FermenterID added: %s" % fermid)
    return fermid


def set_serial_port():
    port = cbpi.get_config_parameter("NEXTION_Serial_Port", None)
    if port is None:
        port = "/dev/ttyUSB0"
        cbpi.add_config_parameter("NEXTION_Serial_Port", "/dev/ttyUSB0", "string",
                                  "Select the Serial Port, Windows like COM1, Linux like dev/ttyS0,"
                                  " /dev/ttyAM0, /dev/ttyUSB0, etc.")
        cbpi.app.logger.info("TFTDisplay - NEXTION_Serial_Port added: %s" % port)
    return port


def set_parameter_dubbleline(ser):
    dubbleline = cbpi.get_config_parameter("NEXTION_bold_line", None)
    if dubbleline is None:
        dubbleline = "on"
        cbpi.add_config_parameter("NEXTION_bold_line", "on", "select", "Select if chart is drawn in bold line or not, "
                                                                       "CBPi reboot recommended", ["on", "off"])
        cbpi.app.logger.info("TFTDisplay - NEXTION_bold_line added: %s" % dubbleline)

    if dubbleline == "on":
        return True
    else:
        NextionwriteClear(ser, 1, 1)  # BrewTemp try to adjust thickness of line # brew
        NextionwriteClear(ser, 1, 3)  # BrewTemp try to adjust thickness of line # brew target

        NextionwriteClear(ser, 5, 1)  # BrewTemp try to adjust thickness of line # ferment
        NextionwriteClear(ser, 5, 3)  # BrewTemp try to adjust thickness of line # ferment target
        return False
    pass


def set_time(ser):
    look_time = 1  # in seconds
    while True:
        timestr = ((strftime("%Y-%m-%d %H:%M:%S", time.localtime())).ljust(20))
        NextionwriteString(ser, "t3start", timestr)
        # if DEBUG: cbpi.app.logger.info("NextionDisplay  - thread set_time " + timestr)
        sleep(look_time)  # showing time only every second <look_time>


def detect_touch(ser, kettleID, dubbleline):
    look_touch = 1  # in seconds
    while True:
        touch = ser.read_until(TERMINATOR)
        if len(touch) != 0:
            istouch = hex(ord(touch[0]))
            if istouch == "0x65":
                cbpi.app.logger.info("NextionDisplay  - touch: A button has been pushed %s" % istouch)
                pageID_touch = hex(ord(touch[1]))
                compID_touch = hex(ord(touch[2]))
                event_touch = hex(ord(touch[3]))
                cbpi.app.logger.info("NextionDisplay  - page:%s, component:%s, event:%s" % (pageID_touch, compID_touch, event_touch))
                # if pageID_touch == "0x1" and compID_touch == "0x10":
                if (pageID_touch == "0x1" or pageID_touch == "0x5") and compID_touch == "0x5":
                    cbpi.app.logger.info("NextionDisplay  - touch: Clearbutton of Brewpage pushed")
                    writewave(ser, kettleID, erase=True, dubbleline=dubbleline)
                elif pageID_touch == "0x0" and compID_touch == "0x3":
                    cbpi.app.logger.info("NextionDisplay  - touch: Brewpage button pushed")
                    if DEBUG: cbpi.app.logger.info("NextionDisplay  - touch: dubbleline = %s" % dubbleline)
                    writewave(ser, kettleID, erase=False, rewrite=True, dubbleline=dubbleline)
                elif (pageID_touch == "0x3" and compID_touch == "0x3") or (pageID_touch == "0x6" and compID_touch == "0x4"):
                    cbpi.app.logger.info("NextionDisplay  - touch: Clearbutton of Fermpage pushed")
                    writefermwave(ser, erase=True)
                elif pageID_touch == "0x0" and compID_touch == "0x5":
                    cbpi.app.logger.info("NextionDisplay  - touch: Fermpage button pushed")
                    writefermwave(ser, erase=False, frewrite=True)
                else:
                    pass
        sleep(look_touch)  # timeout the bigger the larger the chance of missing a push


@cbpi.initalizer(order=3150)
def initNextion(app):
    port = set_serial_port()
    time.sleep(3)
    ser = serial.Serial(
        port=port,
        baudrate=38400,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.1
    )
    ser.reset_output_buffer()

    try:
        cbpi.app.logger.info("NEXTIONDisplay - NEXTION_KetteID:         %s" % set_parameter_kettleID())
        cbpi.app.logger.info("NEXTIONDisplay - NEXTION_Serial Port:     %s" % port)
        cbpi.app.logger.info("NEXTIONDisplay - NEXTION_Fermenter_ID:    %s" % set_parameter_fermID())
        cbpi.app.logger.info("NEXTIONDisplay - NEXTION_bold_line:       %s" % set_parameter_dubbleline(ser))
    except:
        pass

    # nx_setsys(ser, 'bauds', 38400) # already set in display
    # nx_setsys(ser, 'bkcmd', 0)     # already set in display

    # Time as thread
    t_timethread = threading.Thread(target=set_time, name='Time Display', args=(ser,))
    t_timethread.start()

    cbpi.app.logger.info("NEXTIONDisplay - NEXTION init passed")
    # end of init

    @cbpi.backgroundtask(key="Nextionjob", interval=6)  # 4 = 27 min, 5 = 33.8 min, 6 = 40.6 min
    def Nextionjob(api):
        # This is the main job
        kettleID = int(set_parameter_kettleID())
        fermid = int(set_parameter_fermID())
        dubbleline = set_parameter_dubbleline(ser)
        ip = set_ip()
        cbpi_version = "CBPi %s" % (get_version_fo(""))

        # for any reason the first value will be dropped so this is just fake and does nothing
        NextionwriteString(ser, "t1startfake", cbpi_version)
        NextionwriteString(ser, "t1start", cbpi_version)

        iptext = "IP: %s" % ip
        NextionwriteString(ser, "t2start", iptext)

        writing_multi_to_nextion(ser)
        writewave(ser, kettleID, dubbleline=dubbleline)
        writingDigittoNextion(ser, kettleID)
        writefermwave(ser, fermid, dubbleline=dubbleline)

        # THREAD - DETECT push buttons
        threadnames = threading.enumerate()
        # if DEBUG: cbpi.app.logger.info("NextionDisplay  - names current thread %s" % threadnames)
        threadnames = str(threadnames)
        if "<Thread(read serial," in threadnames:
            # if DEBUG: cbpi.app.logger.info("NextionDisplay  - thread read serial detected")
            pass
        else:
            t_serialread = threading.Thread(target=detect_touch, name='read serial', args=(ser, kettleID, dubbleline))
            t_serialread.start()
            if DEBUG: cbpi.app.logger.info("NextionDisplay  - threads Thread started")
        pass
