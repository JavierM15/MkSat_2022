import RPi.GPIO as GPIO
import _thread
import SDL_DS3231
import time

from time import sleep
from bmp280 import BMP280
from smbus import SMBus

from ina219 import INA219
from ina219 import DeviceRangeError

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
#Initialize INA219
SHUNT_OHMS = 0.1
ina = INA219(SHUNT_OHMS)
ina.configure()
#Initialize Servomotor
servoPin = 18
GPIO.setup(servoPin,GPIO.OUT)
pwm=GPIO.PWM(servoPin,50) #50 hz
pwm.start(0)

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
def BMP_280():
    while True:
        #BMP_280 only measures pressure
        #temperature = bmp280.get_temperature()
        #degree_sign = u"\N{DEGREE SIGN}"
        #format_temp = "{:.2f}".format(temperature)
        #print('Temperature =  ' + format_temp + degree_sign + 'C')
        pressure = bmp280.get_pressure()
        format_press = "{:.2f}".format(pressure)
        print('Pressure = ' + format_press + ' hPa')
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
#Voltage, led, buzzer, pressure, GPS, XBEE, servomotor,clock
#Falta XBEE, GPS
_thread.start_new_thread(LedControl,())
_thread.start_new_thread(Clock,())
_thread.start_new_thread(BMP_280,())
_thread.start_new_thread(Servo,())
#_thread.start_new_thread(BuzzerControl,())

#Loop, Voltage as primary
while(True):
    print("Bus Voltage: %0.2f V\n" % ina.voltage())
    sleep(2)
