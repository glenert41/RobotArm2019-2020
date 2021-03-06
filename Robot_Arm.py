#This code makes a thing spin really fast and
# launch it in to the stratosphere
#Like a freaking explosion of fast upward momentum. 
#In theory its really cool, I promise
import gc
import board
import math
gc.collect()

import time
import digitalio
import analogio
gc.collect()

from analogio import AnalogIn
import pulseio
gc.collect()

from adafruit_motor import servo, Motor
#from adafruit_motor import Motor

import adafruit_bus_device

gc.collect()
import simpleio   
#pylint: disable-msg=import-error



#Shaft Servo Set Up
pwmShaftServo = pulseio.PWMOut(board.D9, duty_cycle=2 ** 15, frequency=50)
shaftServo = servo.Servo(pwmShaftServo)

shaftPot = AnalogIn(board.A1)


#Pitch Servo Set Up
pwmPitchServo = pulseio.PWMOut(board.A3, duty_cycle=2 ** 15, frequency = 50)
pitchServo = servo.Servo(pwmPitchServo)

pitchServoPot = AnalogIn(board.A0)



#Motor Set Up
pwmMotor = pulseio.PWMOut(board.A2, frequency=50)
my_Motor = servo.ContinuousServo(pwmMotor)

motorPot = AnalogIn(board.A5)


#PhotoInteruppter SetUp
photoPin = digitalio.DigitalInOut(board.D8)
photoPin.direction = digitalio.Direction.INPUT
photoPin.pull = digitalio.Pull.UP
interrupts = -1         
lread = True
fread = True 

#LCD Set Up
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface 
from lcd.lcd import CursorMode
lcd = LCD(I2CPCF8574Interface(0x3F), num_rows=2, num_cols=16)



initial = time.monotonic()

while True:

    now = time.monotonic() 
    
    mappedShaftPot = int(shaftPot.value/2**16*180)
    shaftServo.angle = int(mappedShaftPot)
    #print(str("Shaft Servo: ") + (str(shaftServo.angle)))

    mappedPitchPot = int(pitchServoPot.value/2**16*180)
    pitchServo.angle = int(mappedPitchPot)
    #print(str("Pitch Servo: ") + (str(pitchServo.angle)))

    MotorPotOut = motorPot.value

# ----------------------------------------------------    
   # Motor Potentiometer 

    if(MotorPotOut <= 5000):
        pwmMotor.duty_cycle = 0
    elif(MotorPotOut >= 60000):
        pwmMotor.duty_cycle = 2**16-1
    else:
        pwmMotor.duty_cycle = int(MotorPotOut)
    
    displayMotorPotOut = int(simpleio.map_range(MotorPotOut,0,2**16-1,0,100))
    
#-----------------------------------------------------

    #Just here becauses it is paired with the RPS printing Below
    if photoPin.value:
        lread = True   
    elif fread == lread:                             
        interrupts +=1   
        lread = not lread

#LCD 1 Second Updates

    if now - initial >= 1:
        lcd.clear()
        lcd.set_cursor_pos(0,0)         #clears and resets LCD
        
        

        if(MotorPotOut <= 5000):
            lcd.print(str("Speed: 0"))
        elif(MotorPotOut >= 60000):
            lcd.print("Speed: 100")
        else:
            lcd.print(("Speed: ") + (str(displayMotorPotOut)))

        #RPS Printing        
        lcd.set_cursor_pos(1,0)
        lcd.print(("RPS: ") + str(interrupts))
        interrupts = 0

        #End of the 1 Second Check
        initial = time.monotonic()
        
        

    time.sleep(.05)
    

   


