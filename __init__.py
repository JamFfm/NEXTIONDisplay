# !/usr/bin/env python
# *-* coding: iso-8859-1 *-*
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
# NextionDisplay Version 0.0.0.9
# Assembled by JamFfm
#
# sudo pip install pyserial         # install serial unlikely you have to
#                                   # install it because usually it is already installed
# python -m serial.tools.list_ports # List all ports in command-box
# dmesg | grep tty                  # List serial Connections


from modules import cbpi, app
import time
import serial
import socket  # ip adr
import fcntl   # ip adr
import struct  # ip adr
# from time import gmtime, strftime  # Time display
from time import strftime  # Time display

liste = []
listetarget =[]
global max_value_old
max_value_old = 0
global min_value_old
min_value_old = 0


def writingDigittoNextion(kettleID):
    ctemp = currenttemp_float(kettleID)
    #   Current Temperature in text field
    TextDigitTxt2 = ("%6.2f%s" % (ctemp, (chr(176)+"C")))
    textCurrTemp2 = str(TextDigitTxt2)
    # cbpi.app.logger.info('NextionDisplay  - digit CurrTempTxt.txt:%s' % (textCurrTemp2))
    NextionwriteString("CurrTempTxt", textCurrTemp2)

    #   Target Temp in Text Field    
    TextDigitTxt3 = ("%6.2f%s" % (float(TempTargTemp(kettleID)), (chr(176)+"C")))
    textCurrTemp3 = str(TextDigitTxt3)
    # cbpi.app.logger.info('NextionDisplay  - TargTempTxt.txt:%s' % (textCurrTemp3))
    NextionwriteString("TargetTempTxt", textCurrTemp3)

    #   Current Kettlenumber in text field
    Digitnumber = int(kettleID)
    # cbpi.app.logger.info('NextionDisplay  - KettleNumb.val:%s' % (Digitnumber))
    NextionwriteNumber("KettleNumb", Digitnumber)


def NextionwriteString(TextLableName, string):
    """
    :param TextLableName: name of the textlable on the Nextion
    :param string: the string to write in this lable
    """
    command = ('%s.txt="%s"' %(TextLableName, string))
    cbpi.app.logger.info('NextionDisplay  - command Txt:%s' % command)
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=9600,
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
    command = ('add %s,%s,%s' % (WaveID, Channnel, intValue))
    # cbpi.app.logger.info('NextionDisplay  - command Wave:%s' % command)
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=9600,
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
    # cbpi.app.logger.info('NextionDisplay  - command Number:%s' % command)
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=9600,
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


def NextionwriteClear(WaveID, channel):
    command = ('cle %s,%s' %(WaveID, channel))
    # cbpi.app.logger.info('NextionDisplay  - command Number:%s' % command)
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=9600,
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


def cbidecode(string):

    # cbpi.app.logger.info('NextionDisplay  - string:%s' % string)
    udata=string.encode("iso-8859-1")
    asciidata=udata.decode("ascii", "ignore")

    # cbpi.app.logger.info('NextionDisplay  - encoded_str:%s' % (asciidata))
    return asciidata.encode("iso-8859-1")


def writewave(kettleID):
    temp0 = currenttemp_float(kettleID)
    targettemp = targettemp_float(kettleID)
    #   Current Temperature in text field
    TextDigitTxt0 = ("%6.2f%s" % (temp0, (chr(176)+"C")))
    textCurrTemp0 = str(TextDigitTxt0)
    # cbpi.app.logger.info('NextionDisplay  - CurrTempBrwTxt.txt:%s' % (textCurrTemp0))
    NextionwriteString("CurrTempBrwTxt", textCurrTemp0)
    #   Target Temp in Text Field    
    TextDigitTxt1 = ("%6.2f%s" % (targettemp, (chr(176)+"C")))
    textCurrTemp1 = str(TextDigitTxt1)
    # cbpi.app.logger.info('NextionDisplay  - TargTempBrwTxt.txt:%s' % (textCurrTemp1))
    NextionwriteString("TargTempBrwTxt", textCurrTemp1)
    #   Current Kettlename in text field    
    kettlen = kettlename()
    NextionwriteString("KettleNameTxt", kettlen)
    #   rest name
    restn = restname()
    NextionwriteString("RestNameTxt", restn)
    #   build liste
    if len(liste) < 406:
        liste.append(temp0)
    else:
        del liste[0]
        liste.append(temp0)
        cbpi.app.logger.info('NextionDisplay  - TempListe bigger 407:%s' % (len(liste)))
    # cbpi.app.logger.info('NextionDisplay  - TempListe:%s' % (liste))
    cbpi.app.logger.info('NextionDisplay  - TempListe len(liste):%s' % (len(liste)))
    # build liste targettemp
    if len(listetarget) < 406:
        listetarget.append(targettemp)
    else:
        del listetarget[0]
        listetarget.append(targettemp)
    cbpi.app.logger.info('NextionDisplay  - targetListe len(listetarget):%s' % (len(listetarget)))
    # min max labels at scale
    max_value = (max(liste)+0.2)
    min_value = (min(liste)-0.2)
    NextionwriteString("tmax", "%s%s" % (max_value, (chr(176)+"C")))
    NextionwriteString("tmin", "%s%s" % (min_value, (chr(176)+"C")))
    NextionwriteString("tavarage", "%s%s" % (round(((max_value+min_value)/2), 2), (chr(176)+"C")))
    # get the factor
    offset = (max_value - min_value)
    xpixel = 202  # the height of the wave on Nextion
    cbpi.app.logger.info('NextionDisplay  -         check 1: offset: %s' % offset)
    factor2 = (xpixel / offset)
    cbpi.app.logger.info('NextionDisplay  -         check 2: factor2: %s' % factor2)
    global min_value_old
    global max_value_old
    if max_value != max_value_old or min_value != min_value_old:
        cbpi.app.logger.info('NextionDisplay  - rewrite check 3')
        NextionwriteClear(1, 0)  # BrewTemp
        NextionwriteClear(1, 2)  # TargetTemp
        i = 0
        while i < len(liste):
            cbpi.app.logger.info('NextionDisplay  - liste:%s' % (liste[i]))
            digit = (round(float((liste[i] - min_value) * factor2), 2))
            string = (str(round(float(digit)))[:-2])
            NextionwriteWave(1, 0, string)
            #  targettemp
            target = (round(float((listetarget[i] - min_value) * factor2), 2))
            tstring = (str(round(float(target)))[:-2])
            if target < xpixel:  #do not write target line if not in temp range
                NextionwriteWave(1, 2, tstring)
            else:
                pass
            i += 1
            cbpi.app.logger.info('NextionDisplay  - digit, string: %s, %s' % (digit, string))
    else:
        digit = (round(float((temp0 - min_value) * factor2), 2))
        string = (str(round(float(digit)))[:-2])
        NextionwriteWave(1, 0, string)
        cbpi.app.logger.info('NextionDisplay  - digit, string: %s, %s' % (digit, string))
        # target Temp
        target = (round(float((targettemp - min_value) * factor2), 2))
        tstring = (str(round(float(target)))[:-2])
        if target < xpixel:  # do not write target line if not in temp range
            NextionwriteWave(1, 2, tstring)
        else:
            pass
    pass
    cbpi.app.logger.info('NextionDisplay  - max and min value: %s, %s' % (max_value, min_value))

    global max_value_old
    max_value_old = max_value
    global min_value_old
    min_value_old = min_value


def currentfermtemp():
    pass


def targetfermtemp():
    pass


def currenttemp_float(kettleID):
    temp = float(Temp(kettleID))
    return temp


def targettemp_float(kettleID):
    targettemp = float(TempTargTemp(kettleID))
    return targettemp


def kettlename():
    kettlename = ""
    kettlename = ('%s' % (cbpi.cache.get("kettle").get(int(kettleID)).name))
    # cbpi.app.logger.info('NextionDisplay  - KettleNameTxt.txt:%s' % (kettlename))
    kettlename = cbidecode(kettlename)
    # cbpi.app.logger.info('NextionDisplay  - decodeKettleNameTxt.txt:%s' % (kettlename))
    return kettlename


def restname():
    restname = ""
    s = cbpi.cache.get("active_step")
    if s is not None:
        restname = s.name
        # cbpi.app.logger.info('NextionDisplay  - restname:%s' % (restname))
        restname = cbidecode(restname)
        return restname
    else:
        return "no active rest"

def FermenterName():
    pass


def Beername():
    # beername = modules.fermenter.Fermenter.brewname
    # return beername
    pass


def Temp(kkid):
    # cbpi.app.logger.info("NEXTIONDisplay  - Temp detect")
    current_sensor_value_id3 = (cbpi.get_sensor_value(int(cbpi.cache.get("kettle").get(int(kkid)).sensor)))
    curTemp = ("%6.2f" % (float(current_sensor_value_id3)))
    # cbpi.app.logger.info("NEXTIONDisplay  - Temp: %s" % (curTemp))
    return curTemp


def set_parameter_kettleID():
    kettleid = cbpi.get_config_parameter("NEXTION_Kettle_ID", None)
    if kettleid is None:
        kettleid = 1
        cbpi.add_config_parameter ("NEXTION_Kettle_ID", 1, "number", "Choose kettle (Number), NO! CBPi reboot required")
        cbpi.app.logger.info("NEXTIONDisplay  - KettleID added: %s" % kettleid)
    return kettleid


def TempTargTemp(temptargid):
    # cbpi.app.logger.info("TFTDisplay  - Target Temp detect")
    current_sensor_value_temptargid = cbpi.cache.get("kettle")[(int(temptargid))].target_temp
    targTemp = ("%6.2f" % (float(current_sensor_value_temptargid)))
    # cbpi.app.logger.info("TFTDisplay  - TargTemp: %s" % (targTemp))
    return targTemp


def get_ip(interface):
    ip_addr = "Not connected"
    so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        ip_addr = socket.inet_ntoa(fcntl.ioctl(so.fileno(), 0x8915, struct.pack('256s', interface[:15]))[20:24])
    finally:
        pass
    return ip_addr


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


@cbpi.initalizer(order=3100)
def initNextion(app):

    # end of init

    @cbpi.backgroundtask(key="Nexionjob", interval=4)

    def Nextionjob(api):
        # This is the main job
        if get_ip('wlan0') != 'Not connected':
            ip = get_ip('wlan0')
        elif get_ip('eth0') != 'Not connected':
            ip = get_ip('eth0')
        elif get_ip('enxb827eb488a6e') != 'Not connected':
            ip = get_ip('enxb827eb488a6e')
        else:
            ip = 'Not connected'
        pass
        cbpi_version = "CBPi %s" % (get_version_fo(""))
        # for any reason the first value will be dropped so this is just fake and does nothing
        NextionwriteString("t1startfake", cbpi_version)
        #
        NextionwriteString("t1start", cbpi_version)

        timestr = ((strftime("%Y-%m-%d %H:%M:%S", time.localtime())).ljust(20))
        NextionwriteString("t3start", timestr)

        iptext = ""
        iptext = "IP: %s" % ip
        NextionwriteString("t2start", iptext)

        global kettleID
        kettleID = set_parameter_kettleID()

        writingDigittoNextion(kettleID)
        writewave(kettleID)

        # writingFermCharttoNexion(kettleID)

