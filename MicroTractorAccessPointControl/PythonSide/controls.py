####################################
#
#  Controls.py
# 
#  Turn the user inputs into control 
#  outputs 
#
####################################
import pygame

DEADBAND = 0.05
desired_position = 90

def HitchControl(current_position,x_button,b_button):

    global desired_position
    print(current_position)
    #Define the ramp rate of the hitch here
    ramp_rate = 7.0
        #Use the buttons to set the desired position
    if(b_button):
        desired_position = 90
    elif(x_button):
        desired_position = 0
    
    #Implement a rate limiter 
    if(current_position < (desired_position - ramp_rate)):
        current_position = current_position + ramp_rate
        
    elif(current_position > (desired_position + ramp_rate)):
        current_position = current_position - ramp_rate
   
    else:
        current_position = desired_position
   
    print(current_position)
    #Return the current_position
    return current_position



#Given an x,y joystick, convert this into left and track values
def SpeedControlJoystick(xval,yval):        
        
    #Execute the drive strategy
    if(yval < DEADBAND and yval > -DEADBAND): 
        left = 125
        right = 125
    else:
        left  = 1*yval*125+125
        right = 1*yval*125+125 

    if (xval > DEADBAND):
        right = right + xval*200 
        left = left - xval*200 
    elif (xval < -DEADBAND):
        left  = left  - xval*200
        right = right + xval*200 
 
    #Saturation
    if(left > 250):
        left = 250
    elif(left< 0):
        left = 0
    if(right > 250):
        right = 250
    elif(right <0):
        right = 0
    return (left, right)

def SpeedControlKeyboard(keystroke):

    # checking if key "W" was pressed
    if (keystroke == pygame.K_w):
        SpeedControlKeyboard.left = 0xFA
        SpeedControlKeyboard.right = 0xFA
       
    # checking if key "S" was pressed
    if (keystroke == pygame.K_s):
        SpeedControlKeyboard.left = 0x7D
        SpeedControlKeyboard.right = 0x7D

    # checking if key "X" was pressed
    if (keystroke == pygame.K_x):
        SpeedControlKeyboard.left = 0x00
        SpeedControlKeyboard.right = 0x00

    # checking if key "a" was pressed
    if (keystroke == pygame.K_d):
        SpeedControlKeyboard.left = 0x00
        SpeedControlKeyboard.right = 0xFA

    # checking if key "d" was pressed
    if (keystroke == pygame.K_a):
        SpeedControlKeyboard.left = 0xFA
        SpeedControlKeyboard.right = 0x00

    return(SpeedControlKeyboard.left,SpeedControlKeyboard.right)

SpeedControlKeyboard.left = 0x7D
SpeedControlKeyboard.right = 0x7D

