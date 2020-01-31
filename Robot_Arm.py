
import board
import math 
import time
import digitalio
import analogio
from analogio import AnalogIn
import pulseio
from adafruit_motor import servo, Motor
#from adafruit_motor import Motor

import adafruit_bus_device

#import simpleio   
#pylint: disable-msg=import-error


# Shaft Servo
# Pitch Servo

#Dc Motor

#Photointerrupter

pwmShaftServo = pulseio.PWMOut(board.D9, duty_cycle=2 ** 15, frequency=50)
shaftServo = servo.Servo(pwmShaftServo)

shaftPot = AnalogIn(board.A1)



pwmPitchServo = pulseio.PWMOut(board.A3, duty_cycle=2 ** 15, frequency = 50)
pitchServo = servo.Servo(pwmPitchServo)

pitchServoPot = AnalogIn(board.A0)




pwmMotor = pulseio.PWMOut(board.A2, frequency=50)
my_Motor = servo.ContinuousServo(pwmMotor)

motorPot = AnalogIn(board.A5)



photoPin = digitalio.DigitalInOut(board.D8)
photoPin.direction = digitalio.Direction.INPUT
photoPin.pull = digitalio.Pull.UP

interrupts = -1         
lread = True
fread = True 


from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface #importing and prepping LCD library

from lcd.lcd import CursorMode

lcd = LCD(I2CPCF8574Interface(0x3f), num_rows=2, num_cols=16)

while True:
    
    mappedShaftPot = int(shaftPot.value/2**16*180) # simpleio.map_range(shaftPot,0,2^16,0,180)
    shaftServo.angle = int(mappedShaftPot)
    #print(int(mappedShaftPot))
 
    mappedPitchPot = int(pitchServoPot.value/2**16*180)
    pitchServo.angle = int(mappedPitchPot)

 

    MotorPotOut = motorPot.value
    #print(MotorPotOut)


    if photoPin.value:
        lread = True   #if interrupted, turn lread to true

    elif fread == lread: #if the photointerrupter is interrupted, then uniterrupted,
                                #count the interrupter and add 1 to the counter variable
        interrupts +=1   
        lread = not lread
    #print(interrupts)



    pwmMotor.duty_cycle = int(MotorPotOut)
    
    if(MotorPotOut < 2000):
        pwmMotor.duty_cycle = 0
    if(MotorPotOut > 60000):
        pwmMotor.duty_cycle = 2**16-1
    

    
    lcd.clear()
    lcd.set_cursor_pos(0,0)         #clears and resets LCD
    lcd.print("Presses: ") 

    time.sleep(.1)
    

   
