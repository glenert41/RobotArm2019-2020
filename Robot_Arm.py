# CircuitPython IO demo #1 - General Purpose I/O
import board
import time
import digitalio
import analogio
from analogio import AnalogIn
import pulseio
from adafruit_motor import servo
from adafruit_motor import Motor

import adafruit_bus_device

import simpleio   
#pylint: disable-msg=import-error


# Shaft Servo
# Pitch Servo

#Dc Motor

#Photointerrupter

pwmShaftServo = pulseio.PWMOut(board.A4, duty_cycle=2 ** 15, frequency=50)
shaftServo = servo.Servo(pwmShaftServo)

shaftPot = AnalogIn(board.A1)



pwmPitchServo = pulseio.PWMOut(board.A3, duty_cycle=2 ** 15, frequency = 50)
pitchServo = servo.Servo(pwmPitchServo)

pitchServoPot = AnalogIn(board.A0)




pwmMotor = pulseio.PWMOut(board.A2, frequency=50)
my_Motor = servo.ContinuousServo(pwmMotor)

motorPot = AnalogIn(board.A5)




while True:
 
    mappedShaftPot = shaftPot.value/2**16*180 # simpleio.map_range(shaftPot,0,2^16,0,180)
    shaftServo.angle = int(mappedShaftPot)
    #print(int(mappedShaftPot))
 
    mappedPitchPot = pitchServoPot.value/2**16*180
    pitchServo.angle = int(mappedPitchPot)

    #mappedMotorPot = simpleio.map_range(int(motorPot.value),200,1600,0,2**16-1)
    #pwmMotor.duty_cycle = int(mappedMotorPot)
    #pwmMotor.duty_cycle = 60000
    #print(int(mappedMotorPot))
    #print(motorPot.value)

    

    MotorPotOut = motorPot.value
    print(MotorPotOut)


    #print(secureMotorPot)
    




    pwmMotor.duty_cycle = int(MotorPotOut)
    
    if(MotorPotOut < 2000):
        pwmMotor.duty_cycle = 0
    if(MotorPotOut > 60000):
        pwmMotor.duty_cycle = 2**16-1
    


    time.sleep(.1)
    

   
