import socket
import time
import pygame

darkgrey = (40, 40, 40)
lightgrey = (150, 150, 150)

class ESPConnect:
    def __init__(self):
        print("ESP Connection Started")
        TCP_IP = '192.168.4.1'
        TCP_PORT = 10010
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((TCP_IP, TCP_PORT))
        self.counter = 0

    #The send data function is what outputs the data to the tractor
    def SendData(self,left_side,right_side,buttons):
        #Create a counter to help troubleshoot packets
        self.counter = self.counter +1
        if(self.counter >200):
            self.counter = 0       
        self.client.send((bytearray([self.counter,left_side,right_side,buttons, 0x68])))
        print(self.counter ,left_side,right_side,buttons)


class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)
 
    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, lightgrey)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10
 
pygame.init()
 
# Set the width and height of the screen [width,height]
size = [500, 980]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Joystick")
 
#Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print
textPrint = TextPrint()

#Create a connection to the ESP 
#connection = ESPConnect()
 
# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
            
 
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(darkgrey)
    textPrint.reset()
 
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
 
    textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
    textPrint.indent()

	#Hardcoding the joystick number here 
    i = 0

    joystick = pygame.joystick.Joystick(i)
    joystick.init()

    textPrint.print(screen, "Joystick {}".format(i) )
    textPrint.indent()

    # Get the name from the OS for the controller/joystick
    name = joystick.get_name()
    textPrint.print(screen, "Joystick name: {}".format(name) )
    
    # Usually axis run in pairs, up/down for one, and left/right for
    # the other.
    axes = joystick.get_numaxes()
    textPrint.print(screen, "Number of axes: {}".format(axes) )
    textPrint.indent()
    
    for i in range( axes ):
        axis = joystick.get_axis( i )
        textPrint.print(screen, "Axis {} value: {}".format(i, axis) )
    textPrint.unindent()
        
    buttons = joystick.get_numbuttons()
    textPrint.print(screen, "Number of buttons: {}".format(buttons) )
    textPrint.indent()

    for i in range( buttons ):
        button = joystick.get_button( i )
        textPrint.print(screen, "Button {:>2} value: {}".format(i,button) )
    textPrint.unindent()
        
    # Hat switch. All or nothing for direction, not like joysticks.
    # Value comes back in an array.
    hats = joystick.get_numhats()
    textPrint.print(screen, "Number of hats: {}".format(hats) )
    textPrint.indent()

    for i in range( hats ):
        hat = joystick.get_hat( i )
        textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)) )
    textPrint.unindent()
    
    textPrint.unindent()
 
	#Process the joysticks
    xval = joystick.get_axis(0)
    yval = -1*joystick.get_axis(1)
    

    left = 125
    right = 125

    #Execute the drive strategy
    if(yval < 0.01 and yval > -0.01): 
        left = 125
        right = 125
    else:
        left = yval*125+125
        right = yval*125+125

    if (xval > 0.01):
        right = right + xval*200 
        left = left - xval*200

    elif (xval < -0.01):
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

   # connection.SendData(int(left),int(right),0x00)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 20 frames per second
    clock.tick(20)
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
