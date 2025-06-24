import pygame
import pygame_gui

class BertecSelfSelectedSpeedGUI:
    white = 20
    def __init__(self):
        # Define colors
        self.red = (255, 0, 0)
        self.purple = (128, 0, 128)
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        # Initialize the screen and manager
        self.screen_width = 800
        self.screen_height = 800
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Bertec FIT 5 Self Selected Speed')
        self.manager = pygame_gui.UIManager((self.screen_width, self.screen_height))
        self.screen.fill(self.white)

        # Set Font Types
        self.font = pygame.font.Font(None, 20)
        self.large_font = pygame.font.Font(None, 36)

        current_velocity_text = self.large_font.render('Current Speed: ' + str(current_velocity) + ' m/s', True, self.black)
        self.screen.blit(current_velocity_text, (30, treadmill_display_top - 30))

        dead_zone_text = self.font.render('Dead Zone', True, self.black)
        self.screen.blit(dead_zone_text, (treadmill_display_right + 90, 50))  # 500
        stop_zone_text = self.font.render('Stop Zone', True, self.black)
        self.screen.blit(stop_zone_text, (treadmill_display_right + 90, 90))  # 500
        origin_location_text = self.font.render('Origin Location', True, self.black)
        self.screen.blit(origin_location_text, (treadmill_display_right + 85, 130))  # 495
        neutral_zone_location_text = self.font.render('Neutral Zone Location', True, self.black)
        self.screen.blit(neutral_zone_location_text, (treadmill_display_right + 50, 170))  # 460
        neutral_zone_height_text = self.font.render('Neutral Zone Height', True, self.black)
        self.screen.blit(neutral_zone_height_text, (treadmill_display_right + 60, 210))  # 470
        '''amount_fast_divisions_text = font.render('Amount of Fast Divisions', True, black)
        screen.blit(amount_fast_divisions_text, (treadmill_display_right+30, 250))  # 440
        amount_slow_divisions_text = font.render('Amount of Slow Divisions', True, black)
        screen.blit(amount_slow_divisions_text, (treadmill_display_right+30, 290))  # 440'''
        starting_velocity_text = self.font.render('Starting Velocity', True, self.black)
        self.screen.blit(starting_velocity_text, (treadmill_display_right + 70, 270))  # 440
        acceleration_text = self.font.render('Acceleration', True, self.black)
        self.screen.blit(acceleration_text, (treadmill_display_right + 70, 310))  # 440
        sample_frequency_text = self.font.render('Sample Frequency', True, self.black)
        self.screen.blit(sample_frequency_text, (treadmill_display_right + 70, 350))  # 440
        control_select_text = self.font.render('Select Control Type', True, self.black)
        self.screen.blit(control_select_text, (385, 380))  # 440
        slow_control_select_text = self.font.render('Slow Zone', True, self.black)
        self.screen.blit(slow_control_select_text, (345, 395))  # 440
        fast_control_select_text = self.font.render('Fast Zone', True, self.black)
        self.screen.blit(fast_control_select_text, (490, 395))  # 440
        slow_control_section_text = self.font.render('Slow:', True, self.black)
        self.screen.blit(slow_control_section_text, (treadmill_display_right + 10, 490))  # 440
        fast_control_section_text = self.font.render('Fast:', True, self.black)
        self.screen.blit(fast_control_section_text, (treadmill_display_right + 10, 580))  # 440

        # Check Boxes
        dead_zone_cb = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect(
            (treadmill_display_right + 170, 40), (30, 30)), text='', manager=self.manager)  # 580
        stop_zone_cb = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect(
            (treadmill_display_right + 170, 80), (30, 30)), text='', manager=self.manager)  # 580
        '''exponential_divisions_cb = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect(
            (treadmill_display_right+170, 560), (30, 30)), text='', manager=manager)  # 580
        exponential_speed_cb = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect(
            (treadmill_display_right+170, 600), (30, 30)), text='', manager=manager)  # 580'''

        # Text Boxes
        dead_zone_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (treadmill_display_right + 210, 40), (100, 30)), initial_text=str(dead_zone_height), manager=self.manager)  # 620
        stop_zone_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (treadmill_display_right + 210, 80), (100, 30)), initial_text=str(stop_zone_height), manager=self.manager)  # 620
        origin_location_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (treadmill_display_right + 210, 120), (100, 30)), initial_text=str(origin_location), manager=self.manager)  # 620
        neutral_zone_location_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (treadmill_display_right + 210, 160), (100, 30)), initial_text=str(neutral_zone_location),
            manager=self.manager)  # 620
        neutral_zone_height_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (treadmill_display_right + 210, 200), (100, 30)), initial_text=str(neutral_zone_height),
            manager=self.manager)  # 620
        '''fast_divisions_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (treadmill_display_right+210, 240), (100, 30)), initial_text=str(amount_fast_divisions), manager=manager)  # 620
        slow_divisions_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (treadmill_display_right+210, 280), (100, 30)), initial_text=str(amount_slow_divisions), manager=manager)  # 620'''
        starting_velocity_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (treadmill_display_right + 210, 260), (100, 30)), initial_text=str(starting_velocity),
            manager=self.manager)  # 620
        acceleration_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (treadmill_display_right + 210, 300), (100, 30)), initial_text=str(acceleration), manager=manager)  # 620
        sample_frequency_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (treadmill_display_right + 210, 340), (100, 30)), initial_text=str(sample_frequency),
            manager=self.manager)  # 620

        # buttons
        start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (treadmill_display_right + 100, screen_height - 75), (100, 50)),
            text='start', manager=self.manager, allow_double_clicks=False)
        stop_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (treadmill_display_right + 225, screen_height - 75), (100, 50)),
            text='stop', manager=self.manager, allow_double_clicks=False)
        end_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (treadmill_display_right + 350, screen_height - 75), (100, 50)),
            text='end', manager=self.manager, allow_double_clicks=False)

        # dropdown
        fast_control_select = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect(
            (469, 417), (100, 66)),
            item_list=['step', 'linear', 'equation'], default_selection='step', manager=self.manager)
        slow_control_select = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect(
            (328, 417), (100, 66)),
            item_list=['step', 'linear', 'equation'], default_selection='step', manager=self.manager)


    def draw_treadmill(self):
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
                                                    treadmill_display_bottom - treadmill_display_top), 2)

        # Draw origin line
        pygame.draw.line(screen, purple, (30, origin_display_location),
                         (30 + treadmill_display_width, origin_display_location), 2)

        # Draw fast division lines
        for division in range(0, amount_fast_divisions):
            if division != amount_fast_divisions:
                fast_division_line_display_location = neutral_zone_display_top - (division + 1) * (
                        fast_zone_display_height / amount_fast_divisions)
                pygame.draw.line(screen, black, (30, fast_division_line_display_location),
                                 (30 + treadmill_display_width, fast_division_line_display_location), 2)
        # Draw slow division lines
        for division in range(0, amount_slow_divisions):
            if division != 0:
                slow_division_line_display_location = slow_zone_display_top + division * (
                        slow_zone_display_height / amount_slow_divisions)
                pygame.draw.line(screen, black, (30, slow_division_line_display_location),
                                 (30 + treadmill_display_width, slow_division_line_display_location), 2)
        # Draw COP indicator

        # Draw cleaning box
        pygame.draw.rect(screen, white, pygame.Rect(treadmill_display_right - 1,
                                                    treadmill_display_top - 2,
                                                    5,
                                                    treadmill_display_bottom - treadmill_display_top + 4))

    def clear_slow_control_zone(self):
        pygame.draw.rect(self.screen, self.white, pygame.Rect(treadmill_display_right + 50,
                                                                485,
                                                                300,
                                                                577 - 490))
    def clear_fast_control_zone(self):
        pygame.draw.rect(self.screen, self.white, pygame.Rect(treadmill_display_right + 50,
                                                                485,
                                                                300,
                                                                577 - 490))