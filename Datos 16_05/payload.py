import RPi.GPIO as GPIO
import _thread
import SDL_DS3231
import time
import numpy

from time import sleep
from bmp280 import BMP280
from smbus import SMBus
from imusensor.MPU9250 import MPU9250

print("Display of the sensor measurements: ")

#Initialize the BMP280
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)
#Initialize Led Pin
ledPin = 26
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin,GPIO.OUT)
#Initialize Buzzer Pin
buzzPin = 19
GPIO.setup(buzzPin,GPIO.OUT)
#Initialize Clock DS3231
ds3231 = SDL_DS3231.SDL_DS3231(1, 0x68)
ds3231.write_now()
#Initialize IMU
address = 0x69
imu = MPU9250.MPU9250(bus, address)
imu.begin()
#Initiliaze Servomotor
servoPin = 18

def LedControl():
    while True:
        GPIO.output(ledPin,GPIO.HIGH)
        sleep(2)
        GPIO.output(ledPin,GPIO.LOW)
        sleep(2)
def BuzzerControl():
    while True:
	GPIO.output(buzzPin,GPIO.HIGH)
	sleep(2)
        GPIO.output(buzzPin,GPIO.LOW)
	sleep(2)

def Clock():
    while True:
        print ("Raspberry Pi=\t" + time.strftime("%Y/%m/%d, %H:%M:%S"))
        print ("Ds3231=\t\t%s" % ds3231.read_datetime())
        sleep(2)
def Servo():
    ang=0
    signal = 2+(ang/18)
    while True:
        if ang>=181:
            ang=0
            signal = 2+(ang/18)
            GPIO.output(18,True)
            pwm.ChangeDutyCycle(signal)
            sleep(1)
            GPIO.output(18,False)
            pwm.ChangeDutyCycle(0)
        else:
            signal = 2+(ang/18)
            GPIO.output(18,True)
            pwm.ChangeDutyCycle(signal)
            sleep(1)
            GPIO.output(18,False)
            pwm.ChangeDutyCycle(0)
            ang=ang+10

#Enable concurrent events
#Led, buzzer, pressure, temperature, imu, XBEE, servomotor, clock
#Falta XBEE
_thread.start_new_thread(LedControl,())
_thread.start_new_thread(Clock,())
_thread.start_new_thread(Servo,())
_thread.start_new_thread(BuzzerControl,())

#Loop, GY-91 as primary
while(True):
    imu.readSensor()
    imu.computeOrientation()
    print("Accel x: {0} ; Accel y : {1} ; Accel z : {2}".format(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2]))
    print("Gyro x: {0} ; Gyro y : {1} ; Gyro z : {2}".format(numpy.degrees(imu.GyroVals[0]), numpy.degrees(imu.GyroVals[1]), numpy.degrees(imu.GyroVals[2])))
    print("Mag x: {0} ; Mag y : {1} ; Mag z : {2}".format(imu.MagVals[0]/100, imu.MagVals[1]/100, imu.MagVals[2]/100))

    pressure_GY = bmp280.get_pressure()
    format_pressure_GY = "{:.2f}".format(pressure_GY)
    temp_GY = bmp280.get_temperature()
    format_temp_GY = "{:.2f}".format(temp_GY)
    degree_sign_GY = u"\N{DEGREE SIGN}"
    print('Temperature =  ' + format_temp_GY + degree_sign_GY + 'C')
    print('Pressure =  ' + format_pressure_GY + ' hPa \n')
    sleep(2)
