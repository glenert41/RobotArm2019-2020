# CircuitPython IO demo #1 - General Purpose I/O
import board
import neopixel
import math
import time
import digitalio
import analogio
from analogio import AnalogIn
import pulseio
from adafruit_motor import servo
import touchio
import adafruit_bus_device
#import simpleio  #pylint: disable-msg=import-error


# Shaft Servo
# Pitch Servo

#Dc Motor

#Photointerrupter

pwmShaftServo = pulseio.PWMOut(board.A4, duty_cycle=2 ** 15, frequency=50)
shaftServo = servo.Servo(pwmShaftServo)

shaftPot = AnalogIn(board.A1)



while True:
 
    mappedShaftPot = shaftPot.value/2**16*180; # simpleio.map_range(shaftPot,0,2^16,0,180)
    shaftServo.angle = int(mappedShaftPot)
    print(int(mappedShaftPot))


    '''
    for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
        shaftServo.angle = 1
        print(shaftPot.value)
        time.sleep(0.05)
    for angle in range(180, 0, -5): # 180 - 0 degrees, 5 degrees at a time.
        shaftServo.angle = 90
        print(shaftPot.value)
        time.sleep(0.05)
    '''


    time.sleep(.1)
    

   


