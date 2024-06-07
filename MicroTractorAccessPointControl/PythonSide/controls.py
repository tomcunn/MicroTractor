####################################
#
#  Controls.py
# 
#  Turn the user inputs into control 
#  outputs 
#
####################################
import pygame

DEADBAND = 0.20

def HitchControl(current_position,x_button,b_button):
    if(x_button):
        if(current_position < 180):
            current_position = 180
    elif(b_button):
        if(current_position > 0):
            current_position = 0
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

