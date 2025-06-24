# import BertecRemoteControl
from time import sleep
import pygame
import pygame_gui

from BertecSelfSelectedSpeedGUI import BertecSelfSelectedSpeedGUI as Bertec

# TODO:
#  Add treadmill Control
#  Add COP marker
#  setting speed change in each division
#  add speed control methods
#  Future work: Add symbolic library for equation control
#  add start and stop functionality
#  add equal spacing to step

# Defaults
# Default Booleans:
dead_zone = False
stop_zone = False
exponential_divisions = False
exponential_velocity_change = False
start = False

# Default Values
dead_zone_height = 0.1
stop_zone_height = 0.28
neutral_zone_height = 0.28
origin_location = 0.7
neutral_zone_location = 0.14

# Default Divisions
amount_fast_divisions = 2
amount_slow_divisions = 2

sample_frequency = 20
starting_velocity = 0

velocity_change_first_fast_division = 0.01
velocity_change_first_slow_division = 0.01

treadmill_width = 0.7   # meters
treadmill_length = 1.4  # meters

fast_zone_height = (treadmill_length-neutral_zone_height)/2
slow_zone_height = (treadmill_length-neutral_zone_height)/2

# Initializing Color
red = (255, 0, 0)
purple = (128, 0, 128)
green = (0, 255, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

screen_width = 800
screen_height = 800

treadmill_display_mult = 350
treadmill_display_length = treadmill_length*treadmill_display_mult
treadmill_display_width = treadmill_width * treadmill_display_mult
treadmill_display_top = 0.5*(screen_height-treadmill_display_length)
treadmill_display_bottom = treadmill_display_top+treadmill_display_length

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Bertec FIT 5 Self Selected Speed')
font = pygame.font.Font(None, 20)
large_font = pygame.font.Font(None, 36)
text = font.render(str(0.8), True, white, black)

manager = pygame_gui.UIManager((screen_width, screen_height))

# completely fill the surface object
# with white color
screen.fill(white)

current_velocity = 0
acceleration = 1
velocity_change = 0
copx = 0
copy = 0

treadmill_display_right = 30+treadmill_display_width

# Text
current_velocity_text = large_font.render('Current Speed: ' + str(current_velocity) + ' m/s', True, black)
screen.blit(current_velocity_text, (30, treadmill_display_top-30))


dead_zone_text = font.render('Dead Zone', True, black)
screen.blit(dead_zone_text, (treadmill_display_right+90, 50))  # 500
stop_zone_text = font.render('Stop Zone', True, black)
screen.blit(stop_zone_text, (treadmill_display_right+90, 90))  # 500
origin_location_text = font.render('Origin Location', True, black)
screen.blit(origin_location_text, (treadmill_display_right+85, 130))  # 495
neutral_zone_location_text = font.render('Neutral Zone Location', True, black)
screen.blit(neutral_zone_location_text, (treadmill_display_right+50, 170))  # 460
neutral_zone_height_text = font.render('Neutral Zone Height', True, black)
screen.blit(neutral_zone_height_text, (treadmill_display_right+60, 210))  # 470
'''amount_fast_divisions_text = font.render('Amount of Fast Divisions', True, black)
screen.blit(amount_fast_divisions_text, (treadmill_display_right+30, 250))  # 440
amount_slow_divisions_text = font.render('Amount of Slow Divisions', True, black)
screen.blit(amount_slow_divisions_text, (treadmill_display_right+30, 290))  # 440'''
starting_velocity_text = font.render('Starting Velocity', True, black)
screen.blit(starting_velocity_text, (treadmill_display_right+70, 270))  # 440
acceleration_text = font.render('Acceleration', True, black)
screen.blit(acceleration_text, (treadmill_display_right+70, 310))  # 440
sample_frequency_text = font.render('Sample Frequency', True, black)
screen.blit(sample_frequency_text, (treadmill_display_right+70, 350))  # 440
control_select_text = font.render('Select Control Type', True, black)
screen.blit(control_select_text, (385, 380))  # 440
slow_control_select_text = font.render('Slow Zone', True, black)
screen.blit(slow_control_select_text, (345, 395))  # 440
fast_control_select_text = font.render('Fast Zone', True, black)
screen.blit(fast_control_select_text, (490, 395))  # 440
slow_control_section_text = font.render('Slow:', True, black)
screen.blit(slow_control_section_text, (treadmill_display_right+10, 490))  # 440
fast_control_section_text = font.render('Fast:', True, black)
screen.blit(fast_control_section_text, (treadmill_display_right+10, 580))  # 440


# Check Boxes
dead_zone_cb = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect(
    (treadmill_display_right+170, 40), (30, 30)), text='', manager=manager)  # 580
stop_zone_cb = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect(
    (treadmill_display_right+170, 80), (30, 30)), text='', manager=manager)  # 580
'''exponential_divisions_cb = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect(
    (treadmill_display_right+170, 560), (30, 30)), text='', manager=manager)  # 580
exponential_speed_cb = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect(
    (treadmill_display_right+170, 600), (30, 30)), text='', manager=manager)  # 580'''

# Text Boxes
dead_zone_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
    (treadmill_display_right+210, 40), (100, 30)), initial_text=str(dead_zone_height), manager=manager)  # 620
stop_zone_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
    (treadmill_display_right+210, 80), (100, 30)), initial_text=str(stop_zone_height), manager=manager)  # 620
origin_location_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
    (treadmill_display_right+210, 120), (100, 30)), initial_text=str(origin_location), manager=manager)  # 620
neutral_zone_location_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
    (treadmill_display_right+210, 160), (100, 30)), initial_text=str(neutral_zone_location), manager=manager)  # 620
neutral_zone_height_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
    (treadmill_display_right+210, 200), (100, 30)), initial_text=str(neutral_zone_height), manager=manager)  # 620
'''fast_divisions_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
    (treadmill_display_right+210, 240), (100, 30)), initial_text=str(amount_fast_divisions), manager=manager)  # 620
slow_divisions_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
    (treadmill_display_right+210, 280), (100, 30)), initial_text=str(amount_slow_divisions), manager=manager)  # 620'''
starting_velocity_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
    (treadmill_display_right+210, 260), (100, 30)), initial_text=str(starting_velocity), manager=manager)  # 620
acceleration_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
    (treadmill_display_right+210, 300), (100, 30)), initial_text=str(acceleration), manager=manager)  # 620
sample_frequency_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
    (treadmill_display_right+210, 340), (100, 30)), initial_text=str(sample_frequency), manager=manager)  # 620

# buttons
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
    (treadmill_display_right+100, screen_height-75), (100, 50)),
    text='start', manager=manager, allow_double_clicks=False)
stop_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
    (treadmill_display_right+225, screen_height-75), (100, 50)),
    text='stop', manager=manager, allow_double_clicks=False)
end_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
    (treadmill_display_right+350, screen_height-75), (100, 50)),
    text='end', manager=manager, allow_double_clicks=False)

# dropdown
fast_control_select = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect(
    (469, 417), (100, 66)),
    item_list=['step', 'linear', 'equation'], default_selection='step', manager=manager)
slow_control_select = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect(
    (328, 417), (100, 66)),
    item_list=['step', 'linear', 'equation'], default_selection='step', manager=manager)

clock = pygame.time.Clock()


# Drawing Rectangle
while True:
    time_delta = clock.tick(60) / 1000.0

    # Actual zone calculations
    if dead_zone:
        fast_zone_height = treadmill_length-origin_location-neutral_zone_height+neutral_zone_location-dead_zone_height
    else:
        fast_zone_height = treadmill_length - origin_location - neutral_zone_height + neutral_zone_location

    if stop_zone:
        slow_zone_height = origin_location - neutral_zone_location - stop_zone_height
    else:
        slow_zone_height = origin_location - neutral_zone_location

    pygame.draw.rect(screen, white, pygame.Rect(30,
                                                treadmill_display_bottom+2,
                                                treadmill_display_width+50,
                                                screen_height-treadmill_display_bottom))
    pygame.draw.rect(screen, white, pygame.Rect(0,
                                                0,
                                                treadmill_display_width+50,
                                                treadmill_display_top - 5))

    current_velocity_text = large_font.render('Current Speed: ' + str(round(current_velocity, 3)) + ' m/s', True, black)
    screen.blit(current_velocity_text, (30, treadmill_display_top - 30))
    current_velocity_change_text = large_font.render('Speed Change: ' + str(round(velocity_change, 3)) + ' m/s',
                                                     True, black)
    screen.blit(current_velocity_change_text, (30, treadmill_display_top - 70))
    fast_zone_height_text = large_font.render('COP location: (' + str(round(copx, 3))+', ' + str(round(copy, 3))+')',
                                              True, black)
    screen.blit(fast_zone_height_text, (30, 680))  # 440
    fast_zone_height_text = large_font.render('Fast Zone Height: ' + str(round(fast_zone_height, 3)), True, black)
    screen.blit(fast_zone_height_text, (30, 720))  # 440
    slow_zone_height_text = large_font.render('Slow Zone Height: ' + str(round(slow_zone_height, 3)), True, black)
    screen.blit(slow_zone_height_text, (30, 760))  # 440

    # Display Calculations
    # Stop Zone
    stop_zone_display_top = treadmill_display_bottom-stop_zone_height*treadmill_display_mult
    stop_zone_display_height = treadmill_display_bottom-stop_zone_display_top

    # Neutral Zone
    neutral_zone_display_top = treadmill_display_bottom - treadmill_display_mult * (
            origin_location + (neutral_zone_height - neutral_zone_location))
    neutral_zone_display_height = neutral_zone_height * treadmill_display_mult

    # Slow Zone
    slow_zone_display_top = neutral_zone_display_top+neutral_zone_display_height
    if stop_zone:
        slow_zone_display_height = stop_zone_display_top-slow_zone_display_top
    else:
        slow_zone_display_height = treadmill_display_bottom-slow_zone_display_top

    # Dead Zone
    dead_zone_display_top = treadmill_display_top
    dead_zone_display_height = dead_zone_height*treadmill_display_mult

    # Fast Zone
    if dead_zone:
        fast_zone_display_top = dead_zone_display_top+dead_zone_display_height
        fast_zone_display_height = neutral_zone_display_top - dead_zone_display_top-dead_zone_display_height
    else:
        fast_zone_display_top = treadmill_display_top
        fast_zone_display_height = neutral_zone_display_top - treadmill_display_top

    # Origin Line
    origin_display_location = treadmill_display_bottom-origin_location*treadmill_display_mult

    # Draw Display Treadmill
    # Draw Stop Zone
    if stop_zone:
        pygame.draw.rect(
            screen, red, pygame.Rect(30,
                                     stop_zone_display_top,
                                     treadmill_display_width,
                                     stop_zone_display_height))
        pygame.draw.rect(
            screen, black, pygame.Rect(30,
                                       stop_zone_display_top,
                                       treadmill_display_width,
                                       stop_zone_display_height), 2)

    # Draw Slow Down Zone
    pygame.draw.rect(
        screen, yellow, pygame.Rect(30,
                                    slow_zone_display_top,
                                    treadmill_display_width,
                                    slow_zone_display_height))

    # Draw Speed Up Zone
    pygame.draw.rect(
        screen, green, pygame.Rect(30,
                                   fast_zone_display_top,
                                   treadmill_display_width,
                                   fast_zone_display_height))

    # Draw Dead Zone
    if dead_zone:
        pygame.draw.rect(
            screen, black, pygame.Rect(30,
                                       dead_zone_display_top,
                                       treadmill_display_width,
                                       dead_zone_display_height))

    # Draw Neutral Zone
    pygame.draw.rect(
        screen, white, pygame.Rect(30,
                                   neutral_zone_display_top,
                                   treadmill_display_width,
                                   neutral_zone_display_height))

    pygame.draw.rect(
        screen, black, pygame.Rect(30,
                                   neutral_zone_display_top,
                                   treadmill_display_width,
                                   neutral_zone_display_height), 2)

    # Draw Treadmill
    pygame.draw.rect(screen, black, pygame.Rect(30,
                                                treadmill_display_top,
                                                treadmill_display_width,
                                                treadmill_display_bottom-treadmill_display_top), 2)

    # Draw origin line
    pygame.draw.line(screen, purple, (30, origin_display_location),
                     (30+treadmill_display_width, origin_display_location), 2)

    # Draw fast division lines
    for division in range(0, amount_fast_divisions):
        if division != amount_fast_divisions:
            fast_division_line_display_location = neutral_zone_display_top-(division+1)*(
                    fast_zone_display_height/amount_fast_divisions)
            pygame.draw.line(screen, black, (30, fast_division_line_display_location),
                             (30 + treadmill_display_width, fast_division_line_display_location), 2)
    # Draw slow division lines
    for division in range(0, amount_slow_divisions):
        if division != 0:
            slow_division_line_display_location = slow_zone_display_top+division*(
                    slow_zone_display_height/amount_slow_divisions)
            pygame.draw.line(screen, black, (30, slow_division_line_display_location),
                             (30 + treadmill_display_width, slow_division_line_display_location), 2)
    # Draw COP indicator

    # Draw cleaning box
    pygame.draw.rect(screen, white, pygame.Rect(treadmill_display_right-1,
                                                treadmill_display_top-2,
                                                5,
                                                treadmill_display_bottom - treadmill_display_top+4))

    pygame.display.flip()
    for event in pygame.event.get():

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        manager.process_events(event)

        if event.type == pygame_gui.UI_CHECK_BOX_CHECKED:
            if event.ui_element == dead_zone_cb:
                dead_zone = True
            if event.ui_element == stop_zone_cb:
                stop_zone = True

        if event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
            if event.ui_element == dead_zone_cb:
                dead_zone = False
            if event.ui_element == stop_zone_cb:
                stop_zone = False

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == dead_zone_tb:
                dead_zone_height = float(event.text)
            if event.ui_element == stop_zone_tb:
                stop_zone_height = float(event.text)
            if event.ui_element == origin_location_tb:
                origin_location = float(event.text)
            if event.ui_element == neutral_zone_location_tb:
                neutral_zone_location = float(event.text)
            if event.ui_element == neutral_zone_height_tb:
                neutral_zone_height = float(event.text)
            if event.ui_element == fast_divisions_tb:
                amount_fast_divisions = int(event.text)
            if event.ui_element == slow_divisions_tb:
                amount_slow_divisions = int(event.text)
            if event.ui_element == sample_frequency_tb:
                sample_frequency = int(event.text)
            if event.ui_element == starting_velocity_tb:
                starting_velocity = float(event.text)
            if event.ui_element == acceleration_tb:
                acceleration = int(event.text)

        if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            if event.ui_element == slow_control_select:
                if event.text == 'step':
                    # clear white box
                    pygame.draw.rect(screen, white, pygame.Rect(treadmill_display_right + 50,
                                                                485,
                                                                300,
                                                                577 - 490))

                    # textbox
                    slow_divisions_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
                        (treadmill_display_right + 225, 488), (25, 20)), initial_text='2',
                        manager=manager)  # 620

                    # checkbox
                    slow_equally_spaced_cb = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect(
                        (treadmill_display_right + 160, 510), (15, 15)), text='', manager=manager)  # 580

                    # text
                    amount_slow_divisions_text = font.render('Amount of Divisions (1-5):', True, black)
                    screen.blit(amount_slow_divisions_text, (treadmill_display_right+50, 490))
                    slow_equally_spaced_text = font.render('Equally Spaced?', True, black)
                    screen.blit(slow_equally_spaced_text, (treadmill_display_right + 50, 510))
                    slow_division_location_text = font.render('Location of Divisions from Neutral:', True, black)
                    screen.blit(slow_division_location_text, (treadmill_display_right + 50, 530))

                if event.text == 'linear':
                    # clear white box
                    pygame.draw.rect(screen, white, pygame.Rect(treadmill_display_right+50,
                                                                 485,
                                                                 300,
                                                                 577-490))
                    slow_divisions_tb.hide()
                    slow_equally_spaced_cb.hide()

                if event.text == 'equation':
                    print('equation')

            if event.ui_element == fast_control_select:
                if event.text == 'step':
                    # clear white box

                    # textbox
                    slow_divisions_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
                        (treadmill_display_right + 225, 578), (25, 20)), initial_text='2',
                        manager=manager)  # 488

                    # checkbox
                    slow_equally_spaced_cb = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect(
                        (treadmill_display_right + 160, 600), (15, 15)), text='', manager=manager)  # 510

                    # text
                    amount_slow_divisions_text = font.render('Amount of Divisions (1-5):', True, black)
                    screen.blit(amount_slow_divisions_text, (treadmill_display_right + 50, 580))  # 490
                    slow_equally_spaced_text = font.render('Equally Spaced?', True, black)
                    screen.blit(slow_equally_spaced_text, (treadmill_display_right + 50, 600))  # 510
                    slow_division_location_text = font.render('Location of Divisions from Neutral:', True, black)
                    screen.blit(slow_division_location_text, (treadmill_display_right + 50, 620))  #530

                if event.text == 'linear':
                    print('linear')
                if event.text == 'equation':
                    print('equation')

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                start = True
            if event.ui_element == stop_button:
                # Set treadmill to speed to 0
                start = False
            if event.ui_element == end_button:
                quit()

        # Draws the surface object to the screen.

    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.update()
    sleep(1/sample_frequency)
