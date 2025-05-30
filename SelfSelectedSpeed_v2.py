# import BertecRemoteControl
from time import sleep
import pygame
import keyboard

Sample_frequency = 20

stop_zone = True
stop_zone_width = 0.28

origin_location = 0.7
neutral_zone_width = 0.28
neutral_zone_location = 0.14

treadmill_width = 1.4

amount_front_divisions = 2
amount_back_divisions = 1

exponential_divisions = False
exponential_velocity_change = False

velocity_change_per_division = 0.1

front_zone = treadmill_width-origin_location-neutral_zone_width+neutral_zone_location

if stop_zone:
    back_zone = origin_location-neutral_zone_location-stop_zone_width
else:
    back_zone = origin_location-neutral_zone_location

import pygame



# Initializing Color
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Velocity')
font = pygame.font.Font(None, 36)
text = font.render(str(0.8), True, white, black)

textRect = text.get_rect()
textRect.center = (320, 240)

# Drawing Rectangle
while True:
    # completely fill the surface object
    # with white color
    screen.fill(white)

    # copying the text surface object
    # to the display surface object
    # at the center coordinate.
    screen.blit(text, textRect)

    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    text = font.render(str(0.8), True, white, black)
    pygame.draw.rect(screen, red, pygame.Rect(30, 30, 30 + 140, 30 + 280), 2)
    pygame.display.flip()
    for event in pygame.event.get():

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:

            # deactivates the pygame library
            pygame.quit()

            # quit the program.
            quit()

        # Draws the surface object to the screen.
    pygame.display.update()
    sleep(0.1)