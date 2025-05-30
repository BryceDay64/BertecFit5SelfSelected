import BertecRemoteControl
from time import sleep
import pygame
import keyboard

white = (255, 255, 255)
black = (0, 0, 0)

remote = BertecRemoteControl.RemoteControl()
res = remote.start_connection()
print(res)




initialize_velocity = input("Set the initial velocity")

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Velocity')
font = pygame.font.Font(None, 36)
text = font.render(initialize_velocity,True, white, black)

# params = remote.get_run_treadmill_user_input()
res = remote.run_treadmill(initialize_velocity, 1, 1, initialize_velocity, 1, 1)

velocity = initialize_velocity

textRect = text.get_rect()
textRect.center = (320, 240)
sleep(5)

try:
    while True:

        screen.fill(white)
        screen.blit(text, textRect)

        res = remote.get_force_data()

        copy = res['copy']
        fz = res['fz']
        if fz>500:
            if copy >= 1.12:
                velocity = str(round(float(velocity)+0.05, 2))
                res = remote.run_treadmill(velocity, 1, 1, velocity, 1, 1)
            elif copy >= 0.84:
                velocity = str(round(float(velocity)+0.01, 2))
                res = remote.run_treadmill(velocity, 1, 1, velocity, 1, 1)
            elif copy <= 0.56:
                velocity = str(round(float(velocity)-0.01, 1))
                res = remote.run_treadmill(velocity, 1, 1, velocity, 1, 1)
            elif copy <= 0.28:
                velocity = str(0)
                res = remote.run_treadmill(velocity, 1, 1, velocity, 1, 1)

        text = font.render(str(velocity), True, white, black)
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
        if keyboard.is_pressed('q'):
            quit()

        sleep(0.05)

finally:
    res = remote.run_treadmill(0, 1, 1, 0, 1, 1)
    pygame.quit()
