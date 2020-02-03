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

lcd = LCD(I2CPCF8574Interface(0x3F), num_rows=2, num_cols=16)

initial = time.monotonic()

while True:
    lcd.clear()

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
    

    now = time.monotonic() 
    if now - initial == 2:
        lcd.set_cursor_pos(0,0)         #clears and resets LCD
        lcd.print(str(motorPot.value)) 
        print("working")
        initial = time.monotonic()
    


    '''
    lcd.set_cursor_pos(1,0)
    lcd.print("CAH! VROOM VROOM")
    print("Pressing")
    '''
    time.sleep(.05)
    

   
