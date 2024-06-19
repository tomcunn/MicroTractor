import pygame
import socket
import time
import select
import JoystickControl2 as joy
import controls
import math


print("starting program")

counter = 0

# Set colors
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (120,120,120)

##################### INIT ########################################
# Set the IP address and port to bind the UDP socket
host = "192.168.4.2"  # Listen on all available interfaces
port = 5000

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_socket.setblocking(False)
udp_socket.settimeout(0.001)

# Bind the socket to the specified address and port
udp_socket.bind((host, port))

print(f"Listening for UDP packets on {host}:{port}")


pygame.init()
pygame.display.set_caption("Tractor Control")
# Set up the clock
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 500))
pygame.display.update()

# Create an instance of NintendoJoystickManager and run the main loop
joystick_manager = joy.JoystickManager()

number_of_controllers = len(joystick_manager.nintendo_joysticks)

print("This many controllers were found:" + str(number_of_controllers))

#This just shortens the name of the controller to make it easier to keep track of
if(number_of_controllers == 1):
    controller1 = joystick_manager.nintendo_joysticks[0]
elif(number_of_controllers == 2):
    controller1 = joystick_manager.nintendo_joysticks[0]
    controller2 = joystick_manager.nintendo_joysticks[1]

# Set up the font
font = pygame.font.Font(None, 20)


hitch_pos = 90
running = True


################ MAIN LOOP ########################################
while(running):
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Check if the 'q' key is pressed
                running = False
    
    # Fill the screen with white
    screen.fill(WHITE)
   
    #Process Operator Inputs
    joystick_manager.run()

    #Process Hitch Controls
    hitch_pos = controls.HitchControl(hitch_pos,controller1.x_button,controller1.b_button)

    #print(hitch_pos)
    #Process Controls
    speedleft,speedright = controls.SpeedControlJoystick( controller1.joyx ,  controller1.joyy)

    #Send outputs
    datatoSend = bytes([0x4D,int(speedleft),int(speedright),int(hitch_pos),int(controller1.a_button),int(controller1.y_button)])
    udp_socket.sendto(datatoSend, ('192.168.4.1' , 5000))
    
    # Get the current FPS
    fps = int(clock.get_fps())

    counter = counter + 1
    # Render the FPS value to the screen
    fps_text = font.render(f"FPS: {counter}", True, BLACK)
    screen.blit(fps_text, (10, 10))
    
    fps_text = font.render(f"X-Axis: {round(controller1.joyx,2)}", True, BLACK)
    screen.blit(fps_text, (10, 30))
    
    fps_text = font.render(f"Y_Axis: {round(controller1.joyy,2)}", True, BLACK)
    screen.blit(fps_text, (10, 50))
    
    fps_text = font.render(f"Speed Left: {round(speedleft,1)}", True, BLACK)
    screen.blit(fps_text, (10, 70))
    
    fps_text = font.render(f"Speed Right: {round(speedright,1)}", True, BLACK)
    screen.blit(fps_text, (10, 90))
    
    # Frame rate control
    clock.tick(20)
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
    
