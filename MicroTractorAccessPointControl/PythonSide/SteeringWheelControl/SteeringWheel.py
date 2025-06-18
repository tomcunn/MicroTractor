import pygame

# Initialize pygame
pygame.init()

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
    
while(True):
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    print(target_joystick.get_axis(0), 
          target_joystick.get_axis(1), 
          target_joystick.get_axis(2), 
          target_joystick.get_axis(3),
          target_joystick.get_axis(4),
          target_joystick.get_axis(5))



# Quit pygame
pygame.quit()