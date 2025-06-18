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

# Set up the font
font = pygame.font.Font(None, 20)

hitch_pos = 90
running = True

speedleft = 125
speedright = 125

################ MAIN LOOP ########################################
while(running):
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Check if the 'q' key is pressed
                running = False
            elif event.key == pygame.K_w:  # Check if the 'w' key is pressed
                speedleft = speedleft + 5
            elif event.key == pygame.K_s:  # Check if the 's' key is pressed
                speedleft =speedleft - 5
            elif event.key == pygame.K_e:  # Check if the 'e' key is pressed
                speedright = speedright + 5
            elif event.key == pygame.K_d:  # Check if the 'd' key is pressed
                speedright =speedright -5
    
    # Fill the screen with white
    screen.fill(WHITE)
 
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

# Quit Pygame
pygame.quit()
udp_socket.close()
sys.exit()