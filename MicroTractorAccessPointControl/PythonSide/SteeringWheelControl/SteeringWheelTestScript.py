import pygame
import socket
import time
import select
import math

# Initialize pygame
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

# Initialize the joystick module
pygame.joystick.init()

# Get the number of joysticks connected
joystick_count = pygame.joystick.get_count()

print(f"Number of joysticks connected: {joystick_count}")

# Search for the joystick named "Controller (Wired Wheel)"
target_joystick_name = "Controller (Wired Wheel)"
target_joystick = None

for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joystick_name = joystick.get_name()
    print(f"Joystick {i}: {joystick_name}")
    if joystick_name == target_joystick_name:
        target_joystick = joystick
        print(f"Found target joystick: {target_joystick_name}")
        print("Number of axes:", target_joystick.get_numaxes())
        print("Number of buttons:", target_joystick.get_numbuttons())
        print(target_joystick.get_numaxes)
        break

if target_joystick is None:
    print(f"Joystick '{target_joystick_name}' not found.")

# Set up the font
font = pygame.font.Font(None, 20)

hitch_pos = 90
running = True



while(True):
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # Fill the screen with white
    screen.fill(WHITE)
 
    #Read in the inputs
    steering_angle = target_joystick.get_axis(0)
    left_pedal     = target_joystick.get_axis(4)
    right_pedal    = target_joystick.get_axis(5)
 
    #Process some drive strategy
    # 250 is full speed forward, 0 is full speed reverse
    speedleft = 62.5*left_pedal + 187.5
    speedright = 62.5*left_pedal + 187.5

    #Add in some steering
    speedleft += steering_angle * 125
    speedright -= steering_angle *125

    #Add saturation blocks
    if(speedleft > 250):
        speedleft = 250
    if(speedleft < 0):
        speedleft = 0
        
    if(speedright > 250):
        speedright = 250
    if(speedright < 0):
        speedright = 0

    # Send outputs
    datatoSend = bytes([0x4D, int(speedleft), int(speedright), int(hitch_pos), 0x01, 0x00])
    udp_socket.sendto(datatoSend, ('192.168.4.1', 5000))
    
    # Get the current FPS
    fps = int(clock.get_fps())

    counter = counter + 1
    # Render the FPS value to the screen
    fps_text = font.render(f"FPS: {counter}", True, BLACK)
    screen.blit(fps_text, (10, 10))
    
    fps_text = font.render(f"Speed Left: {round(speedleft, 1)}", True, BLACK)
    screen.blit(fps_text, (10, 70))
    
    fps_text = font.render(f"Speed Right: {round(speedright, 1)}", True, BLACK)
    screen.blit(fps_text, (10, 90))
    
    fps_text = font.render(f"Hitch Position: {hitch_pos}", True, BLACK)
    screen.blit(fps_text, (10, 110))
    
    # Frame rate control
    clock.tick(20)
    
    # Update the display
    pygame.display.flip()




# Quit pygame
pygame.quit()