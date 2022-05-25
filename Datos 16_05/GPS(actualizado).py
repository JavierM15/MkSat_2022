import serial
import datetime

def dec2deg(value):
   dec = value/100.00
   deg = int(dec)
   min = (dec - int(dec))/0.6
   position = deg + min
   position = "%.7f" %(position)
   return position

mapscale = 18
while True:
    port="/dev/ttyAMA0"
    ser=serial.Serial(port, baudrate=9600, timeout=0.5)
    gpsdata=ser.readline()
    gpsdata = gpsdata.decode("utf8",errors='replace')
    gpsdata = gpsdata.split(',')
    if "GNRMC" in gpsdata[0]:
        hrs, mi, sec = gpsdata[1][0:2], gpsdata[1][2:4], gpsdata[1][4:6]
        day, month, year = gpsdata[9][0:2], gpsdata[9][2:4], gpsdata[9][4:6]
        status= gpsdata[2]
        latitude= dec2deg(float(gpsdata[3]))
        oLat=gpsdata[4]
        longitude = dec2deg(float(gpsdata[5]))
        oLon=gpsdata[6]
        datetimeutc = "{}:{}:{} {}/{}/{}".format(hrs, mi, sec, day, month, year)
        datetimeutc = datetime.datetime.strptime(datetimeutc, '%H:%M:%S %d/%m/%y')
        mess0= "Estado {}".format(status)
        mess1 = "Datetime = {}".format(datetimeutc)
        print(mess1)
        mess2= "Latitud {} {}, Longitud {} {}".format(latitude, oLat, longitude, oLon)
        print(mess2)
    """
    if "GNGGA" in gpsdata[0]:
        lat = dec2deg(float(gpsdata[2]))
        lon = dec2deg(float(gpsdata[4]))
        alt = gpsdata[9]
        satcount = gpsdata[7]
        message1 = "Altitude={}, Satellites={}\n".format(alt, satcount)
        print(message1)
        """








        