import pygame
import sys

TARGET_JOYSTICK = "Nintendo Switch Pro Controller"

class NintendoJoystick:
    def __init__(self, joystick):
        self.joystick =  joystick
        self.name =      joystick.get_name()
        self.joyx =      0
        self.joyy =      0
        self.a_button =  False
        self.b_button =  False
        self.x_button =  False
        self.y_button =  False

    def update_states(self):
        self.joyx =      self.joystick.get_axis(0)
        self.joyy =      self.joystick.get_axis(1)
        self.a_button =  self.joystick.get_button(2)
        self.b_button =  self.joystick.get_button(1)
        self.x_button =  self.joystick.get_button(0)
        self.y_button =  self.joystick.get_button(3)

class JoystickManager:
    def __init__(self):
        # Initialize joysticks
        pygame.joystick.init()

        # Create a list to store Nintendo joysticks
        self.nintendo_joysticks = []

        #Determine how many joysticks are connected
        num_joysticks = pygame.joystick.get_count()

        if num_joysticks == 0:
            print("No joysticks found.")
        else:
            print("joysticks found.")

            #Check the name of each
            for i in range(num_joysticks):
                name = pygame.joystick.Joystick(i).get_name()
                
                #See if the joystick is a switch controller
                if (TARGET_JOYSTICK == name):
                    joystick = pygame.joystick.Joystick(i)
                    print("Found a switch controller at: " + str(i))
                    #Initilize the joystick
                    joystick.init()
                    #Create an instance of the joystick and then add to list
                    nintendo_joystick = NintendoJoystick(joystick)
                    self.nintendo_joysticks.append(nintendo_joystick)
                    print (nintendo_joystick)
                    print ("Joystick Created")

    def run(self):
            # Update states for each Nintendo joystick
            for i in self.nintendo_joysticks:
                i.update_states()






