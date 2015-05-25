import smbus
import time
import serial
import datetime
import json

print "Press CTRL+Z to exit"

class Zone(datetime.tzinfo):
    def __init__(self,offset,isdst,name):
        self.offset = offset
        self.isdst = isdst
        self.name = name
    def utcoffset(self, dt):
        return datetime.timedelta(hours=self.offset) + self.dst(dt)
    def dst(self, dt):
        return datetime.timedelta(hours=1) if self.isdst else datetime.timedelta(0)
    def tzname(self,dt):
        return self.name

GMT = Zone(0,False,'GMT')
# True if DST is on
# Fales if now DST
EST = Zone(-5,True,'EST')

#print datetime.datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S %Z')
print datetime.datetime.now(GMT).strftime('%m/%d/%Y %H:%M:%S %Z')
print datetime.datetime.now(EST).strftime('%m/%d/%Y %H:%M:%S %Z')


ser = serial.Serial('/dev/ttyACM0', 9600)
while True:
    try:
        #        localip = socket.gethostbyname(socket.gethostname())
        localip = commands.getoutput("/sbin/ifconfig").split("\n")[9].split()[1][5:]
    except:
        localip = "No ip addr"
    currentTime = datetime.datetime.now(EST).strftime('%m/%d/%Y %H:%M:%S %Z')
    readData = json.loads(ser.readline())
    print currentTime,
    print json.dumps(readData)
    print ""
#    readData['HTU21D-F Temperature']
#    readData['TSL2561 Luminosity']
#    readData['HTU21D-F Humidity']
    try:
        with open('/var/www/index.html', 'w') as f:
            tempInF = str(c_to_f(sensor2Data))
            x = {"Local ip": localip, 'Local Time' : currentTime , 'Temperature' :     readData['HTU21D-F Temperature'] , "Brightness" :     readData['TSL2561 Luminosity'], "Location": "Indoor Green House"}
            json.dump(x,f)
            print x
        f.closed
    except:
        print " cannot open file"
