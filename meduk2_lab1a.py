##################################################
# Name:         Michael Edukonis
# UIN:          677141300
# email:        meduk2@illinois.edu
# class:        CS437
# assignment:   Lab1a
# date:         1/23/2023
##################################################
#meduk2_lab1a.py

import picar_4wd as fc
import random
import sys
import time
import os

#Required integer input for any movement
speed = 1

#Servo has a 180 degree range.  This is split among 4 stops for each sweep: 9, ~11, 12, ~1, and 3 o'clock
scan_angles = [90, 60, 45, 20, 0, -20, -45, -60, -90]     

#list holds the scan results of the ultrasonic sensor.
scan_result = [0,0,0,0,0,0,0,0,0]                        

#Minimum allowable distance (cm) before a turn is necessary
min_distance = 30

##################################################
# Function: scan()
# Inputs:   none
# Outputs:  none
# notes:    calls the set_angle() method from servo
#           object.  Stores the results to the
#           scan_result[] list and prints result
#           to standard output for debug.
##################################################
def scan():
    for x in range(len(scan_angles)):
        fc.servo.set_angle(scan_angles[x])
        time.sleep(0.3)                                     #decreased from 0.5 to 0.3
        scan_result[x] = fc.us.get_distance()
    print(scan_result)

##################################################
# Function: move_forward()
# Inputs:   integer
# Outputs:  none
# notes:    takes an integer for power setting and
#           applies to the 4 wheel motors.  Sleep
#           instruction allows car travel time and
#           then stops all motors.
##################################################
def move_forward(speed):
    fc.forward(speed)
    print("moving forward") #debug
    time.sleep(0.5)
    stop()

##################################################
# Function: turn_right()
# Inputs:   integer
# Outputs:  none
# Notes:    takes an integer for power setting and
#           applies to the 2 left wheel motors
#           forward and 2 right wheels backward
#           effecting a turn right motion on the
#           car. Sleep instruction gives enough
#           time for 90 degree turn and then stops
#           all motors.
###################################################
def turn_right(radius, speed):
    fc.turn_right(speed)
    print("turning right") #debug
    if radius < 90:
        time.sleep(0.5)             #Will give a 45 degree turn
    else:
        time.sleep(1.2)             #else 90 degree turn.
    stop()
 
###################################################
# Function: turn_left()
# Inputs:   integer
# Outputs:  none
# Notes:    takes an integer for power setting and
#           applies to the 2 right wheel motors
#           forward and 2 left wheels backward
#           effecting a turn left motion on the
#           car. Sleep time gives enough time for
#           90 degree turn and then stops all motors.
###################################################
def turn_left(radius, speed):
    fc.turn_left(speed)
    print("turning left") #debug
    if radius < 90:
        time.sleep(0.5)             #Will give a 45 degree turn
    else:                           #Else 90 degree turn
        time.sleep(1.2)
    stop()
 
###################################################
# Function: back_up()
# Inputs:   integer
# Outputs:  none
# Notes:    takes an integer for power setting and
#           applies to the 4 wheel motors in
#           reverse.  Sleep instruction allows for
#           travel time and then stop all motors.
###################################################
def back_up(speed):
    fc.backward(speed)
    print("backing up") #debug
    time.sleep(0.5)
    stop()

###################################################
# Function: stop()
# Inputs:   none
# Outputs:  none
# Notes:    calls the picar object stop method which
#           issues the command to stop all motors.
###################################################
def stop():
    print("all stop") #debug
    fc.stop()

###################################################
# Function: check_distance()
# Inputs:   integer
# Outputs:  integer
# Notes:    returns a 0 for all clear or 1 for
#           obstacle detected.  If an object is
#           closer than the minimum distance,
#           function returns a
#           1 signaling that an object is nearby
#           -2 is sometimes returned from the
#           sensor if nothing is detected so this
#           would also return 0 signal, all clear.
###################################################
def check_distance(measurement):
    if measurement > min_distance:
        return 0
    if measurement == -2:
        return 0
    if measurement >= 0 and measurement <= min_distance:
        return 1

if __name__ == '__main__':                          #will only run code below if run directly.  Not if imported into another python script.
    while True:
        try:
            scan()                                  #[90, 60, 45, 20, 0, -20, -45, -60, 90]
            for x in range(len(scan_result)):
                scan_result[x] = check_distance(scan_result[x]) #convert scan result list to map of surroundings 1=object near 0=clear
            print(scan_result)                      #debug
            if any(scan_result[:3]) == 1:           #[1,1,1,0,0,0,0,0,0]  object to the left side
                turn_right(90, speed)
            elif any(scan_result[6:]) == 1:         #[0,0,0,0,0,0,1,1,1]  object to the front and/or right side
                turn_left(90, speed)
            elif any(scan_result[3:-3]) == 1:       #[0,0,0,1,1,1,0,0,0]  object dead ahead backup then turn
                back_up(speed)
                print("random turn - ")             #debug
                random.choice([turn_left, turn_right])(90, speed)  #random choice turn left or right
            else:
                move_forward(speed)

        except KeyboardInterrupt:  
            try:
                stop()
                sys.exit(0)
            except SystemExit:
                stop()
                os._exit(0)        
        finally:
            stop()
            