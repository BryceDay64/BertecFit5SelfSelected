import pygame
import pygame_gui


class BertecSelfSelectedSpeedGUI:
    treadmill_length = 1.6  # meters

    def __init__(self, values):

        self.values = values

        # Define colors
        self.red = (255, 0, 0)
        self.purple = (128, 0, 128)
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        # Control method booleans
        self.slow_step = True
        self.fast_step = True
        self.slow_linear = False
        self.fast_linear = False
        self.slow_equation = False
        self.fast_equation = False

        self.previous_amount_slow = 2
        self.previous_amount_fast = 2

        # Initialize the screen and manager
        self.screen_width = 800
        self.screen_height = 800
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Bertec FIT 5 Self Selected Speed')
        self.manager = pygame_gui.UIManager((self.screen_width, self.screen_height))
        self.screen.fill(self.white)

        # Set dimensions of treadmill
        self.treadmill_display_mult = 300
        self.treadmill_display_length = 1.6 * self.treadmill_display_mult
        self.treadmill_display_width = 0.7 * self.treadmill_display_mult
        self.treadmill_display_top = 0.5 * (self.screen_height - self.treadmill_display_length)
        self.treadmill_display_bottom = self.treadmill_display_top + self.treadmill_display_length
        self.treadmill_display_right = 30 + self.treadmill_display_width

        # Set Font Types
        self.font = pygame.font.Font(None, 20)
        self.large_font = pygame.font.Font(None, 36)

        self.current_velocity_text = self.large_font.render(
            'Current Speed: ' + str(self.values['current_velocity']) + ' m/s', True, self.black)
        self.screen.blit(self.current_velocity_text, (30, self.treadmill_display_top - 30))

        self.dead_zone_text = self.font.render('Dead Zone', True, self.black)
        self.screen.blit(self.dead_zone_text, (self.treadmill_display_right + 90, 50))  # 500
        self.stop_zone_text = self.font.render('Stop Zone', True, self.black)
        self.screen.blit(self.stop_zone_text, (self.treadmill_display_right + 90, 90))  # 500
        self.origin_location_text = self.font.render('Origin Location', True, self.black)
        self.screen.blit(self.origin_location_text, (self.treadmill_display_right + 85, 130))  # 495
        self.neutral_zone_location_text = self.font.render('Neutral Zone Location', True, self.black)
        self.screen.blit(self.neutral_zone_location_text, (self.treadmill_display_right + 50, 170))  # 460
        self.neutral_zone_height_text = self.font.render('Neutral Zone Height', True, self.black)
        self.screen.blit(self.neutral_zone_height_text, (self.treadmill_display_right + 60, 210))  # 470
        self.starting_velocity_text = self.font.render('Starting Velocity', True, self.black)
        self.screen.blit(self.starting_velocity_text, (self.treadmill_display_right + 70, 270))  # 440
        self.acceleration_text = self.font.render('Acceleration', True, self.black)
        self.screen.blit(self.acceleration_text, (self.treadmill_display_right + 70, 310))  # 440
        self.sample_frequency_text = self.font.render('Sample Frequency', True, self.black)
        self.screen.blit(self.sample_frequency_text, (self.treadmill_display_right + 70, 350))  # 440
        self.control_select_text = self.font.render('Select Control Type', True, self.black)
        self.screen.blit(self.control_select_text, (385, 380))  # 440
        self.slow_control_select_text = self.font.render('Slow Zone', True, self.black)
        self.screen.blit(self.slow_control_select_text, (345, 395))  # 440
        self.fast_control_select_text = self.font.render('Fast Zone', True, self.black)
        self.screen.blit(self.fast_control_select_text, (490, 395))  # 440
        self.slow_control_section_text = self.font.render('Slow:', True, self.black)
        self.screen.blit(self.slow_control_section_text, (self.treadmill_display_right + 10, 490))  # 440
        self.fast_control_section_text = self.font.render('Fast:', True, self.black)
        self.screen.blit(self.fast_control_section_text, (self.treadmill_display_right + 10, 580))  # 440
        self.enter_text = self.font.render('To commit values press "Enter"', True, self.black)
        self.screen.blit(self.enter_text, (self.treadmill_display_right + 90, 15))

        # Check Boxes
        self.dead_zone_cb = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect(
            (self.treadmill_display_right + 170, 40), (30, 30)), text='', manager=self.manager)  # 580
        self.stop_zone_cb = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect(
            (self.treadmill_display_right + 170, 80), (30, 30)), text='', manager=self.manager)  # 580

        # Text Boxes
        self.dead_zone_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (self.treadmill_display_right + 210, 40), (100, 30)),
            initial_text=str(self.values['dead_zone_height']), manager=self.manager)  # 620
        self.stop_zone_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (self.treadmill_display_right + 210, 80), (100, 30)),
            initial_text=str(self.values['stop_zone_height']), manager=self.manager)  # 620
        self.origin_location_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (self.treadmill_display_right + 210, 120), (100, 30)),
            initial_text=str(self.values['origin_location']), manager=self.manager)  # 620
        self.neutral_zone_location_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (self.treadmill_display_right + 210, 160), (100, 30)),
            initial_text=str(self.values['neutral_zone_location']), manager=self.manager)  # 620
        self.neutral_zone_height_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (self.treadmill_display_right + 210, 200), (100, 30)),
            initial_text=str(self.values['neutral_zone_height']), manager=self.manager)  # 620
        self.starting_velocity_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (self.treadmill_display_right + 210, 260), (100, 30)), initial_text=str(values['starting_velocity']),
            manager=self.manager)  # 620
        self.acceleration_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (self.treadmill_display_right + 210, 300), (100, 30)),
            initial_text=str(self.values['acceleration']), manager=self.manager)  # 620
        self.sample_frequency_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (self.treadmill_display_right + 210, 340), (100, 30)),
            initial_text=str(self.values['sample_frequency']), manager=self.manager)  # 620

        # buttons
        self.start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (self.treadmill_display_right + 100, self.screen_height - 75), (100, 50)),
            text='start', manager=self.manager, allow_double_clicks=False)
        self.stop_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (self.treadmill_display_right + 225, self.screen_height - 75), (100, 50)),
            text='stop', manager=self.manager, allow_double_clicks=False)
        self.end_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (self.treadmill_display_right + 350, self.screen_height - 75), (100, 50)),
            text='end', manager=self.manager, allow_double_clicks=False)
        self.weight_calibration_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            (self.treadmill_display_right + 210, self.screen_height - 133), (130, 50)), text='weight calibration',
            manager=self.manager, allow_double_clicks=False)

        # dropdown
        self.fast_control_select = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect(
            (469, 417), (100, 66)),
            item_list=['step', 'linear', 'equation'], default_selection='step', manager=self.manager)
        self.slow_control_select = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect(
            (328, 417), (100, 66)),
            item_list=['step', 'linear', 'equation'], default_selection='step', manager=self.manager)

        self.step_control_layout('slow')
        self.step_control_layout('fast')

    def draw_treadmill(self):
        # Display Calculations
        # Stop Zone
        stop_zone_display_top = self.treadmill_display_bottom - self.values['stop_zone_height'] * self.treadmill_display_mult
        stop_zone_display_height = self.treadmill_display_bottom - stop_zone_display_top

        # Neutral Zone
        neutral_zone_display_top = self.treadmill_display_bottom - self.treadmill_display_mult * (
                self.values['origin_location'] + (self.values['neutral_zone_height'] - self.values['neutral_zone_location']))
        neutral_zone_display_height = self.values['neutral_zone_height'] * self.treadmill_display_mult

        # Slow Zone
        slow_zone_display_top = neutral_zone_display_top + neutral_zone_display_height
        if self.values['stop_zone']:
            slow_zone_display_height = stop_zone_display_top - slow_zone_display_top
        else:
            slow_zone_display_height = self.treadmill_display_bottom - slow_zone_display_top

        # Dead Zone
        dead_zone_display_top = self.treadmill_display_top
        dead_zone_display_height = self.values['dead_zone_height'] * self.treadmill_display_mult

        # Fast Zone
        if self.values['dead_zone']:
            fast_zone_display_top = dead_zone_display_top + dead_zone_display_height
            fast_zone_display_height = neutral_zone_display_top - dead_zone_display_top - dead_zone_display_height
        else:
            fast_zone_display_top = self.treadmill_display_top
            fast_zone_display_height = neutral_zone_display_top - self.treadmill_display_top

        # Origin Line
        origin_display_location = self.treadmill_display_bottom-self.values['origin_location']*self.treadmill_display_mult

        # Draw Display Treadmill
        # Draw Stop Zone
        if self.values["stop_zone"]:
            pygame.draw.rect(
                self.screen, self.red, pygame.Rect(30,
                                                   stop_zone_display_top,
                                                   self.treadmill_display_width,
                                                   stop_zone_display_height))
            pygame.draw.rect(
                self.screen, self.black, pygame.Rect(30,
                                                     stop_zone_display_top,
                                                     self.treadmill_display_width,
                                                     stop_zone_display_height), 2)

        # Draw Slow Down Zone
        pygame.draw.rect(
            self.screen, self.yellow, pygame.Rect(30,
                                                  slow_zone_display_top,
                                                  self.treadmill_display_width,
                                                  slow_zone_display_height))

        # Draw Speed Up Zone
        pygame.draw.rect(
            self.screen, self.green, pygame.Rect(30,
                                                 fast_zone_display_top,
                                                 self.treadmill_display_width,
                                                 fast_zone_display_height))

        # Draw Dead Zone
        if self.values['dead_zone']:
            pygame.draw.rect(
                self.screen, self.black, pygame.Rect(30,
                                                     dead_zone_display_top,
                                                     self.treadmill_display_width,
                                                     dead_zone_display_height))

        # Draw Neutral Zone
        pygame.draw.rect(
            self.screen, self.white, pygame.Rect(30,
                                                 neutral_zone_display_top,
                                                 self.treadmill_display_width,
                                                 neutral_zone_display_height))

        pygame.draw.rect(
            self.screen, self.black, pygame.Rect(30,
                                                 neutral_zone_display_top,
                                                 self.treadmill_display_width,
                                                 neutral_zone_display_height), 2)

        # Draw Treadmill
        pygame.draw.rect(self.screen, self.black, pygame.Rect(30,
                                                              self.treadmill_display_top,
                                                              self.treadmill_display_width,
                                                              self.treadmill_display_bottom
                                                              - self.treadmill_display_top), 2)

        # Draw origin line
        pygame.draw.line(self.screen, self.purple, (30, origin_display_location),
                         (30 + self.treadmill_display_width, origin_display_location), 2)

        if self.values['fast_control_type'] == 'step':
                # Draw fast division lines
                for division in range(0, self.values['amount_fast_divisions']):
                    if self.values['fast_eq_sp']:
                        if division != self.values['amount_fast_divisions']:
                            fast_division_line_display_location = neutral_zone_display_top - (division + 1) * (
                                    fast_zone_display_height / self.values['amount_fast_divisions'])
                            pygame.draw.line(self.screen, self.black, (30, fast_division_line_display_location),
                                             (30 + self.treadmill_display_width, fast_division_line_display_location),
                                             2)
                    else:
                        if division != 0:
                            fast_division_line_display_location = (neutral_zone_display_top
                                                                   - self.values['fast_division_locations'][division-1]*self.treadmill_display_mult)
                            pygame.draw.line(self.screen, self.black, (30, fast_division_line_display_location),
                                             (30 + self.treadmill_display_width, fast_division_line_display_location), 2)

        if self.values['slow_control_type'] == 'step':
                # Draw slow division lines
                for division in range(0, self.values['amount_slow_divisions']):
                    if division != 0:
                        if self.values['slow_eq_sp']:
                            slow_division_line_display_location = slow_zone_display_top + division * (
                                    slow_zone_display_height / self.values['amount_slow_divisions'])
                        else:
                            slow_division_line_display_location = (
                                    slow_zone_display_top + self.values['slow_division_locations'][division-1]
                                    * self.treadmill_display_mult)
                        pygame.draw.line(self.screen, self.black, (30, slow_division_line_display_location),
                                         (30 + self.treadmill_display_width, slow_division_line_display_location), 2)

        # Draw COP indicator
        pygame.draw.ellipse(self.screen, self.black, pygame.Rect(
            30+(self.treadmill_display_width/2)-5,  # +int(round(self.values['copx']*self.treadmill_display_mult, 0))
            self.treadmill_display_bottom-5-int(round(self.values['copy']*self.treadmill_display_mult,0)),
            10,
            10))
        # Draw cleaning box
        pygame.draw.rect(self.screen, self.white, pygame.Rect(self.treadmill_display_right - 1,
                                                              self.treadmill_display_top - 2,
                                                              5,
                                                              self.treadmill_display_bottom
                                                              - self.treadmill_display_top + 4))
        pygame.draw.rect(self.screen, self.white, pygame.Rect(30,
                                                              self.treadmill_display_top - 5,
                                                              self.treadmill_display_width,
                                                              5))
        pygame.draw.rect(self.screen, self.white, pygame.Rect(30,
                                                              self.treadmill_display_bottom,
                                                              self.treadmill_display_width,
                                                              20))


    def update_text(self):
        # Draw boxes to erase previous text
        pygame.draw.rect(self.screen, self.white, pygame.Rect(30,
                                                              self.treadmill_display_bottom + 20,
                                                              self.treadmill_display_width+100,
                                                              self.screen_height - self.treadmill_display_bottom))
        pygame.draw.rect(self.screen, self.white, pygame.Rect(0,
                                                              0,
                                                              self.treadmill_display_width + 115,
                                                              self.treadmill_display_top - 5))
        pygame.draw.rect(self.screen, self.white, pygame.Rect(599,
                                                              29,
                                                              201,
                                                              300))
        pygame.draw.rect(self.screen, self.white, pygame.Rect(29,
                                                              self.treadmill_display_bottom + 30,
                                                              350,
                                                              50))
        # Add new text
        current_velocity_text = self.large_font.render(
            'Current Speed: ' + str(round(self.values['current_velocity'], 3))+' m/s', True, self.black)
        self.screen.blit(current_velocity_text, (30, self.treadmill_display_top - 30))

        current_velocity_change_text = self.large_font.render(
            'Speed Change: ' + str(round(self.values['velocity_change'], 3)) + ' m/s', True, self.black)
        self.screen.blit(current_velocity_change_text, (30, self.treadmill_display_top - 70))

        cop_location_text = self.large_font.render(
            'COP location: (' + str(round(self.values['copx'], 3)) + ', ' + str(round(self.values['copy'], 3)) + ')',
            True, self.black)
        self.screen.blit(cop_location_text, (30, 680))  # 440

        fast_zone_height_text = self.large_font.render(
            'Fast Zone Height: ' + str(round(self.values['fast_zone_height'], 3)), True, self.black)
        self.screen.blit(fast_zone_height_text, (30, 720))  # 440

        slow_zone_height_text = self.large_font.render(
            'Slow Zone Height: ' + str(round(self.values['slow_zone_height'], 3)), True, self.black)
        self.screen.blit(slow_zone_height_text, (30, 760))  # 440

        if self.values['weight_stop']:
            weight_stop_text = self.large_font.render('Weight Stop!', True, self.red)
            self.screen.blit(weight_stop_text, (600,30))

        if self.values['wrap']:
            wrap_text = self.large_font.render('Velocity Wrap!', True, self.red)
            self.screen.blit(wrap_text, (600, 80))

    def clear_slow_control_zone(self):
        pygame.draw.rect(self.screen, self.white, pygame.Rect(self.treadmill_display_right + 50,
                                                              485,
                                                              750-self.treadmill_display_right,
                                                              577 - 490))
        if self.slow_step:
            self.slow_divisions_tb.hide()
            self.slow_equally_spaced_cb.hide()
            slow_current_delete = self.values['amount_slow_divisions']
            self.values['slow_eq_sp'] = False
            self.slow_velocity_change_tb_1.hide()
            self.slow_step_location_tb_2.hide()
            while slow_current_delete > 0:
                match slow_current_delete:
                    case 5:
                        self.slow_step_location_tb_5.hide()
                        self.slow_velocity_change_tb_5.hide()
                    case 4:
                        self.slow_step_location_tb_4.hide()
                        self.slow_velocity_change_tb_4.hide()
                    case 3:
                        self.slow_step_location_tb_3.hide()
                        self.slow_velocity_change_tb_3.hide()
                    case 2:
                        self.slow_velocity_change_tb_2.hide()
                slow_current_delete -= 1
        if self.slow_linear:
            self.slow_linear_slope_tb.hide()
            self.slow_linear_yintercept_tb.hide()
        if self.slow_equation:
            self.slow_equation_tb.hide()

    def clear_fast_control_zone(self):
        pygame.draw.rect(self.screen, self.white, pygame.Rect(self.treadmill_display_right + 50,
                                                              577,
                                                              750-self.treadmill_display_right,
                                                              577 - 490))
        if self.fast_step:
            self.fast_divisions_tb.hide()
            self.fast_equally_spaced_cb.hide()
            fast_current_delete = self.values['amount_fast_divisions']
            self.values['fast_eq_sp'] = False
            self.fast_velocity_change_tb_1.hide()
            self.fast_step_location_tb_2.hide()
            while fast_current_delete > 0:
                match fast_current_delete:
                    case 5:
                        self.fast_step_location_tb_5.hide()
                        self.fast_velocity_change_tb_5.hide()
                    case 4:
                        self.fast_step_location_tb_4.hide()
                        self.fast_velocity_change_tb_4.hide()
                    case 3:
                        self.fast_step_location_tb_3.hide()
                        self.fast_velocity_change_tb_3.hide()
                    case 2:
                        self.fast_velocity_change_tb_2.hide()
                fast_current_delete -= 1
        if self.fast_linear:
            self.fast_linear_slope_tb.hide()
            self.fast_linear_yintercept_tb.hide()
        if self.fast_equation:
            self.fast_equation_tb.hide()

    def step_control_layout(self, zone):
        if zone == 'slow':
            # textbox
            self.slow_divisions_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
                (self.treadmill_display_right + 225, 488), (25, 20)), initial_text=str(self.values['amount_slow_divisions']),
                manager=self.manager)  # 620
            self.create_step_text_box('slow', 'velocity_change', 1)
            slow_current_add = self.values['amount_slow_divisions']
            while slow_current_add > 0:
                match slow_current_add:
                    case 5:
                        self.create_step_text_box('slow', 'velocity_change', 5)
                        self.create_step_text_box('slow', 'division_location', 5)
                    case 4:
                        self.create_step_text_box('slow', 'velocity_change', 4)
                        self.create_step_text_box('slow', 'division_location', 4)
                    case 3:
                        self.create_step_text_box('slow', 'velocity_change', 3)
                        self.create_step_text_box('slow', 'division_location', 3)
                    case 2:
                        self.create_step_text_box('slow', 'velocity_change', 2)
                        self.create_step_text_box('slow', 'division_location', 2)
                slow_current_add -= 1


            # checkbox
            self.slow_equally_spaced_cb = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect(
                (self.treadmill_display_right + 160, 510), (15, 15)), text='', manager=self.manager)  # 580

            # text
            amount_slow_divisions_text = self.font.render('Amount of Divisions (1-5):', True, self.black)
            self.screen.blit(amount_slow_divisions_text, (self.treadmill_display_right + 50, 490))
            slow_equally_spaced_text = self.font.render('Equally Spaced?', True, self.black)
            self.screen.blit(slow_equally_spaced_text, (self.treadmill_display_right + 50, 510))
            slow_velocity_change_text = self.font.render('Velocity change of each step:', True, self.black)
            self.screen.blit(slow_velocity_change_text, (self.treadmill_display_right + 50, 530))
            slow_division_location_text = self.font.render('Location of Divisions from Neutral:', True, self.black)
            self.screen.blit(slow_division_location_text, (self.treadmill_display_right + 50, 550))

            self.values['slow_control_type'] = 'step'
        elif zone == 'fast':
            # textbox
            self.fast_divisions_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
                (self.treadmill_display_right + 225, 578), (25, 20)), initial_text=str(self.values['amount_fast_divisions']),
                manager=self.manager)  # 488
            self.create_step_text_box('fast', 'velocity_change', 1)
            fast_current_add = self.values['amount_fast_divisions']
            while fast_current_add > 0:
                match fast_current_add:
                    case 5:
                        self.create_step_text_box('fast', 'velocity_change', 5)
                        self.create_step_text_box('fast', 'division_location', 5)
                    case 4:
                        self.create_step_text_box('fast', 'velocity_change', 4)
                        self.create_step_text_box('fast', 'division_location', 4)

                    case 3:
                        self.create_step_text_box('fast', 'velocity_change', 3)
                        self.create_step_text_box('fast', 'division_location', 3)
                    case 2:
                        self.create_step_text_box('fast', 'velocity_change', 2)
                        self.create_step_text_box('fast', 'division_location', 2)
                fast_current_add -= 1

            # checkbox
            self.fast_equally_spaced_cb = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect(
                (self.treadmill_display_right + 160, 600), (15, 15)), text='', manager=self.manager)  # 510

            # text
            amount_fast_divisions_text = self.font.render(
                'Amount of Divisions (1-5):', True, self.black)
            self.screen.blit(amount_fast_divisions_text, (self.treadmill_display_right + 50, 580))  # 490
            fast_equally_spaced_text = self.font.render(
                'Equally Spaced?', True, self.black)
            self.screen.blit(fast_equally_spaced_text, (self.treadmill_display_right + 50, 600))  # 510
            fast_velocity_change_text = self.font.render('Velocity change of each step:', True, self.black)
            self.screen.blit(fast_velocity_change_text, (self.treadmill_display_right + 50, 620))
            fast_division_location_text = self.font.render(
                'Location of Divisions from Neutral:', True, self.black)
            self.screen.blit(fast_division_location_text, (self.treadmill_display_right + 50, 640))  # 530

            self.values['fast_control_type'] = 'step'

    def linear_control_layout(self, zone):
        if zone == 'slow':
            # textbox
            self.slow_linear_slope_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
                (self.treadmill_display_right + 105, 507), (50, 20)), initial_text='0.001',
                manager=self.manager)  # 620
            self.slow_linear_yintercept_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
                (self.treadmill_display_right + 185, 507), (50, 20)), initial_text='0',
                manager=self.manager)  # 620

            # text
            slow_linear_text = self.font.render('Enter your linear Equation', True, self.black)
            self.screen.blit(slow_linear_text, (self.treadmill_display_right + 50, 490))
            slow_linear_equation_text = self.font.render('Δv(x) = -               x - ', True, self.black)
            self.screen.blit(slow_linear_equation_text, (self.treadmill_display_right + 50, 510))

            self.values['slow_control_type'] = 'linear'

        elif zone == 'fast':
            # textbox
            self.fast_linear_slope_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
                (self.treadmill_display_right + 105, 598), (50, 20)), initial_text='0.001',
                manager=self.manager)  # 488
            self.fast_linear_yintercept_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
                (self.treadmill_display_right + 185, 598), (50, 20)), initial_text='0',
                manager=self.manager)  # 488

            # text
            fast_linear_text = self.font.render(
                'Enter your linear Equation', True, self.black)
            self.screen.blit(fast_linear_text, (self.treadmill_display_right + 50, 580))  # 490
            fast_linear_equation_text = self.font.render(
                'Δv(x) =                 x + ', True, self.black)
            self.screen.blit(fast_linear_equation_text, (self.treadmill_display_right + 50, 600))  # 510

            self.values['fast_control_type'] = 'linear'

    def equation_control_layout(self, zone):
        if zone == 'slow':
            # textbox
            self.slow_equation_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
                (self.treadmill_display_right + 95, 507), (200, 20)), initial_text='0.001x',
                manager=self.manager)  # 620

            # text
            slow_wip_text = self.font.render('lol Nerd (WIP)', True, self.black)
            self.screen.blit(slow_wip_text, (self.treadmill_display_right + 50, 490))
            slow_equation_text = self.font.render('Δv(x) = ', True, self.black)
            self.screen.blit(slow_equation_text, (self.treadmill_display_right + 50, 510))

            self.values['slow_control_type'] = 'equation'

        elif zone == 'fast':
            # textbox
            self.fast_equation_tb = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
                (self.treadmill_display_right + 95, 598), (200, 20)), initial_text='0.001x',
                manager=self.manager)  # 488

            # text
            fast_wip_text = self.font.render(
                ' lol Nerd (WIP)', True, self.black)
            self.screen.blit(fast_wip_text, (self.treadmill_display_right + 50, 580))  # 490
            fast_equation_text = self.font.render('Δv(x) = ', True, self.black)
            self.screen.blit(fast_equation_text, (self.treadmill_display_right + 50, 600))

            self.values['fast_control_type'] = 'equation'
    def create_step_text_box(self, zone, tb_type, number):
        match zone:
            case 'slow':
                match tb_type:
                    case 'division_location':
                        match number:
                            case 2:
                                self.slow_step_location_tb_2 = pygame_gui.elements.UITextEntryLine(
                                    relative_rect=pygame.Rect(
                                        (self.treadmill_display_right + 330, 547), (40, 20)),
                                    initial_text=str(self.values['slow_division_locations'][0]), manager=self.manager)  # 620
                            case 3:
                                self.slow_step_location_tb_3 = pygame_gui.elements.UITextEntryLine(
                                    relative_rect=pygame.Rect(
                                        (self.treadmill_display_right + 380, 547), (40, 20)),
                                    initial_text=str(self.values['slow_division_locations'][1]), manager=self.manager)  # 620
                            case 4:
                                self.slow_step_location_tb_4 = pygame_gui.elements.UITextEntryLine(
                                    relative_rect=pygame.Rect(
                                        (self.treadmill_display_right + 430, 547), (40, 20)),
                                    initial_text=str(self.values['slow_division_locations'][2]), manager=self.manager)
                            case 5:
                                self.slow_step_location_tb_5 = pygame_gui.elements.UITextEntryLine(
                                    relative_rect=pygame.Rect(
                                        (self.treadmill_display_right + 480, 547), (40, 20)),
                                    initial_text=str(self.values['slow_division_locations'][3]), manager=self.manager)  # 620
                    case 'velocity_change':
                        match number:
                            case 1:
                                self.slow_velocity_change_tb_1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
                                    (self.treadmill_display_right + 280, 526), (40, 20)),
                                    initial_text=str(self.values['slow_velocity_changes'][0]), manager=self.manager)  # 620
                            case 2:
                                self.slow_velocity_change_tb_2 = pygame_gui.elements.UITextEntryLine(
                                    relative_rect=pygame.Rect(
                                        (self.treadmill_display_right + 330, 526), (40, 20)),
                                    initial_text=str(self.values['slow_velocity_changes'][1]), manager=self.manager)  # 620
                            case 3:
                                self.slow_velocity_change_tb_3 = pygame_gui.elements.UITextEntryLine(
                                    relative_rect=pygame.Rect(
                                        (self.treadmill_display_right + 380, 526), (40, 20)),
                                    initial_text=str(self.values['slow_velocity_changes'][2]), manager=self.manager)  # 620
                            case 4:
                                self.slow_velocity_change_tb_4 = pygame_gui.elements.UITextEntryLine(
                                    relative_rect=pygame.Rect(
                                        (self.treadmill_display_right + 430, 526), (40, 20)),
                                    initial_text=str(self.values['slow_velocity_changes'][3]), manager=self.manager)  # 620
                            case 5:
                                self.slow_velocity_change_tb_5 = pygame_gui.elements.UITextEntryLine(
                                    relative_rect=pygame.Rect(
                                        (self.treadmill_display_right + 480, 526), (40, 20)),
                                    initial_text=str(self.values['slow_velocity_changes'][4]), manager=self.manager)  # 620
            case 'fast':
                match tb_type:
                    case 'division_location':
                        match number:
                            case 2:
                                self.fast_step_location_tb_2 = pygame_gui.elements.UITextEntryLine(
                                    relative_rect=pygame.Rect(
                                        (self.treadmill_display_right + 330, 637), (40, 20)),
                                    initial_text=str(self.values['fast_division_locations'][0]), manager=self.manager)  # 620
                            case 3:
                                self.fast_step_location_tb_3 = pygame_gui.elements.UITextEntryLine(
                                    relative_rect=pygame.Rect(
                                        (self.treadmill_display_right + 380, 637), (40, 20)),
                                    initial_text=str(self.values['fast_division_locations'][1]), manager=self.manager)  # 620
                            case 4:
                                self.fast_step_location_tb_4 = pygame_gui.elements.UITextEntryLine(
                                    relative_rect=pygame.Rect(
                                        (self.treadmill_display_right + 430, 637), (40, 20)),
                                    initial_text=str(self.values['fast_division_locations'][2]), manager=self.manager)  # 620
                            case 5:
                                self.fast_step_location_tb_5 = pygame_gui.elements.UITextEntryLine(
                                    relative_rect=pygame.Rect(
                                        (self.treadmill_display_right + 480, 637), (40, 20)),
                                    initial_text=str(self.values['fast_division_locations'][3]), manager=self.manager)  # 620
                    case 'velocity_change':
                        match number:
                            case 1:
                                self.fast_velocity_change_tb_1 = pygame_gui.elements.UITextEntryLine(
                                    relative_rect=pygame.Rect(
                                        (self.treadmill_display_right + 280, 616), (40, 20)),
                                    initial_text=str(self.values['fast_velocity_changes'][0]), manager=self.manager)  # 620
                            case 2:
                                self.fast_velocity_change_tb_2 = pygame_gui.elements.UITextEntryLine(
                                    relative_rect=pygame.Rect(
                                        (self.treadmill_display_right + 330, 616), (40, 20)),
                                    initial_text=str(self.values['fast_velocity_changes'][1]), manager=self.manager)  # 620
                            case 3:
                                self.fast_velocity_change_tb_3 = pygame_gui.elements.UITextEntryLine(
                                    relative_rect=pygame.Rect(
                                        (self.treadmill_display_right + 380, 616), (40, 20)),
                                    initial_text=str(self.values['fast_velocity_changes'][2]), manager=self.manager)  # 620
                            case 4:
                                self.fast_velocity_change_tb_4 = pygame_gui.elements.UITextEntryLine(
                                    relative_rect=pygame.Rect(
                                        (self.treadmill_display_right + 430, 616), (40, 20)),
                                    initial_text=str(self.values['fast_velocity_changes'][3]), manager=self.manager)  # 620
                            case 5:
                                self.fast_velocity_change_tb_5 = pygame_gui.elements.UITextEntryLine(
                                    relative_rect=pygame.Rect(
                                        (self.treadmill_display_right + 480, 616), (40, 20)),
                                    initial_text=str(self.values['fast_velocity_changes'][4]), manager=self.manager)  # 620

    def events(self):
        for event in pygame.event.get():
            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            self.manager.process_events(event)

            if event.type == pygame_gui.UI_CHECK_BOX_CHECKED:
                if event.ui_element == self.dead_zone_cb:
                    self.values['dead_zone'] = True
                if event.ui_element == self.stop_zone_cb:
                    self.values['stop_zone'] = True
                if self.slow_step:
                    if event.ui_element == self.slow_equally_spaced_cb:
                        self.values['slow_eq_sp'] = True
                        slow_current_delete = self.values['amount_slow_divisions']
                        while slow_current_delete > 0:
                            match slow_current_delete:
                                case 5:
                                    self.slow_step_location_tb_5.hide()
                                case 4:
                                    self.slow_step_location_tb_4.hide()
                                case 3:
                                    self.slow_step_location_tb_3.hide()
                                case 2:
                                    self.slow_step_location_tb_2.hide()

                            slow_current_delete -= 1

                        pygame.draw.rect(self.screen, self.white,
                                         pygame.Rect(self.treadmill_display_right + 279,
                                                     546,
                                                     275,
                                                     22))
                if self.fast_step:
                    if event.ui_element == self.fast_equally_spaced_cb:
                        self.values['fast_eq_sp'] = True
                        fast_current_delete = self.values['amount_fast_divisions']
                        while fast_current_delete > 0:
                            match fast_current_delete:
                                case 5:
                                    self.fast_step_location_tb_5.hide()
                                case 4:
                                    self.fast_step_location_tb_4.hide()
                                case 3:
                                    self.fast_step_location_tb_3.hide()
                                case 2:
                                    self.fast_step_location_tb_2.hide()

                            fast_current_delete -= 1

                        pygame.draw.rect(self.screen, self.white,
                                         pygame.Rect(self.treadmill_display_right + 279,
                                                     636,
                                                     275,
                                                     22))

            if event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
                if event.ui_element == self.dead_zone_cb:
                    self.values['dead_zone'] = False
                if event.ui_element == self.stop_zone_cb:
                    self.values['stop_zone'] = False
                if self.slow_step:
                    if event.ui_element == self.slow_equally_spaced_cb:
                        self.values['slow_eq_sp'] = False
                        slow_current_add = self.values['amount_slow_divisions']
                        while slow_current_add > 0:
                            match slow_current_add:
                                case 5:
                                    self.create_step_text_box('slow', 'division_location', 5)
                                case 4:
                                    self.create_step_text_box('slow', 'division_location', 4)
                                case 3:
                                    self.create_step_text_box('slow', 'division_location', 3)
                                case 2:
                                    self.create_step_text_box('slow', 'division_location', 2)
                            slow_current_add -= 1

                if self.fast_step:
                    if event.ui_element == self.fast_equally_spaced_cb:
                        self.values['fast_eq_sp'] = False
                        fast_current_add = self.values['amount_fast_divisions']
                        while fast_current_add > 0:
                            match fast_current_add:
                                case 5:
                                    self.create_step_text_box('fast', 'division_location', 5)
                                case 4:
                                    self.create_step_text_box('fast', 'division_location', 4)
                                case 3:
                                    self.create_step_text_box('fast', 'division_location', 3)
                                case 2:
                                    self.create_step_text_box('fast', 'division_location', 2)
                            fast_current_add -= 1

            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == self.dead_zone_tb:
                    self.values['dead_zone_height'] = float(event.text)
                if event.ui_element == self.stop_zone_tb:
                    self.values['stop_zone_height'] = float(event.text)
                if event.ui_element == self.origin_location_tb:
                    self.values['origin_location'] = float(event.text)
                if event.ui_element == self.neutral_zone_location_tb:
                    self.values['neutral_zone_location'] = float(event.text)
                if event.ui_element == self.neutral_zone_height_tb:
                    self.values['neutral_zone_height'] = float(event.text)
                if self.fast_step:
                    if event.ui_element == self.fast_divisions_tb:
                        self.values['amount_fast_divisions'] = int(event.text)
                        fast_diff = self.previous_amount_fast-self.values['amount_fast_divisions']
                        if fast_diff > 0:
                            fast_current_delete = self.previous_amount_fast
                            while fast_diff > 0:
                                if fast_current_delete == 5:
                                    self.fast_velocity_change_tb_5.hide()
                                    self.fast_step_location_tb_5.hide()
                                    pygame.draw.rect(self.screen, self.white,
                                                     pygame.Rect(self.treadmill_display_right + 479,
                                                                 615,
                                                                 42,
                                                                 44))
                                if fast_current_delete == 4:
                                    self.fast_velocity_change_tb_4.hide()
                                    self.fast_step_location_tb_4.hide()
                                    pygame.draw.rect(self.screen, self.white,
                                                     pygame.Rect(self.treadmill_display_right + 429,
                                                                 615,
                                                                 42,
                                                                 44))
                                if fast_current_delete == 3:
                                    self.fast_velocity_change_tb_3.hide()
                                    self.fast_step_location_tb_3.hide()
                                    pygame.draw.rect(self.screen, self.white,
                                                     pygame.Rect(self.treadmill_display_right + 379,
                                                                 615,
                                                                 42,
                                                                 44))
                                if fast_current_delete == 2:
                                    self.fast_velocity_change_tb_2.hide()
                                    self.fast_step_location_tb_2.hide()
                                    pygame.draw.rect(self.screen, self.white,
                                                     pygame.Rect(self.treadmill_display_right + 329,
                                                                 615,
                                                                 42,
                                                                 44))
                                fast_current_delete -= 1
                                fast_diff -= 1

                        elif fast_diff < 0:
                            fast_current_add = self.values['amount_fast_divisions']
                            while fast_diff < 0:
                                if fast_current_add == 5:
                                    self.create_step_text_box('fast', 'velocity_change', 5)
                                    if not self.values['fast_eq_sp']:
                                        self.create_step_text_box('fast', 'division_location', 5)
                                if fast_current_add == 4:
                                    self.create_step_text_box('fast', 'velocity_change', 4)
                                    if not self.values['fast_eq_sp']:
                                        self.create_step_text_box('fast', 'division_location', 4)

                                if fast_current_add == 3:
                                    self.create_step_text_box('fast', 'velocity_change', 3)
                                    if not self.values['fast_eq_sp']:
                                        self.create_step_text_box('fast', 'division_location', 3)
                                if fast_current_add == 2:
                                    self.create_step_text_box('fast', 'velocity_change', 2)
                                    if not self.values['fast_eq_sp']:
                                        self.create_step_text_box('fast', 'division_location', 2)
                                fast_current_add -= 1
                                fast_diff += 1
                        self.previous_amount_fast = self.values['amount_fast_divisions']

                    fast_loop = self.values['amount_fast_divisions']
                    if event.ui_element == self.fast_velocity_change_tb_1:
                        self.values['fast_velocity_changes'][0] = float(event.text)
                    while fast_loop > 1:
                        match fast_loop:
                            case 2:
                                if not self.values['fast_eq_sp']:
                                    if event.ui_element == self.fast_step_location_tb_2:
                                        self.values['fast_division_locations'][0] = float(event.text)
                                if event.ui_element == self.fast_velocity_change_tb_2:
                                    self.values['fast_velocity_changes'][1] = float(event.text)
                            case 3:
                                if not self.values['fast_eq_sp']:
                                    if event.ui_element == self.fast_step_location_tb_3:
                                        self.values['fast_division_locations'][1] = float(event.text)
                                if event.ui_element == self.fast_velocity_change_tb_3:
                                    self.values['fast_velocity_changes'][2] = float(event.text)
                            case 4:
                                if not self.values['fast_eq_sp']:
                                    if event.ui_element == self.fast_step_location_tb_4:
                                        self.values['fast_division_locations'][2] = float(event.text)
                                if event.ui_element == self.fast_velocity_change_tb_4:
                                    self.values['fast_velocity_changes'][3] = float(event.text)
                            case 5:
                                if not self.values['fast_eq_sp']:
                                    if event.ui_element == self.fast_step_location_tb_5:
                                        self.values['fast_division_locations'][3] = float(event.text)
                                if event.ui_element == self.fast_velocity_change_tb_5:
                                    self.values['fast_velocity_changes'][4] = float(event.text)

                        fast_loop -= 1

                if self.slow_step:
                    if event.ui_element == self.slow_divisions_tb:
                        self.values['amount_slow_divisions'] = int(event.text)
                        slow_diff = self.previous_amount_slow - self.values['amount_slow_divisions']
                        if slow_diff > 0:
                            slow_current_delete = self.previous_amount_slow
                            while slow_diff > 0:
                                if slow_current_delete == 5:
                                    self.slow_velocity_change_tb_5.hide()
                                    self.slow_step_location_tb_5.hide()
                                    pygame.draw.rect(self.screen, self.white,
                                                     pygame.Rect(self.treadmill_display_right + 479,
                                                                 525,
                                                                 42,
                                                                 44))
                                if slow_current_delete == 4:
                                    self.slow_velocity_change_tb_4.hide()
                                    self.slow_step_location_tb_4.hide()
                                    pygame.draw.rect(self.screen, self.white,
                                                     pygame.Rect(self.treadmill_display_right + 429,
                                                                 525,
                                                                 42,
                                                                 44))
                                if slow_current_delete == 3:
                                    self.slow_velocity_change_tb_3.hide()
                                    self.slow_step_location_tb_3.hide()
                                    pygame.draw.rect(self.screen, self.white,
                                                     pygame.Rect(self.treadmill_display_right + 379,
                                                                 525,
                                                                 42,
                                                                 44))
                                if slow_current_delete == 2:
                                    self.slow_velocity_change_tb_2.hide()
                                    self.slow_step_location_tb_2.hide()
                                    pygame.draw.rect(self.screen, self.white,
                                                     pygame.Rect(self.treadmill_display_right + 329,
                                                                 525,
                                                                 42,
                                                                 44))
                                slow_current_delete -= 1
                                slow_diff -= 1

                        elif slow_diff < 0:
                            slow_current_add = self.values['amount_slow_divisions']
                            while slow_diff < 0:
                                if slow_current_add == 5:
                                    self.create_step_text_box('slow', 'velocity_change', 5)
                                    if not self.values['slow_eq_sp']:
                                        self.create_step_text_box('slow', 'division_location', 5)
                                if slow_current_add == 4:
                                    self.create_step_text_box('slow', 'velocity_change', 4)
                                    if not self.values['slow_eq_sp']:
                                        self.create_step_text_box('slow', 'division_location', 4)
                                if slow_current_add == 3:
                                    self.create_step_text_box('slow', 'velocity_change', 3)
                                    if not self.values['slow_eq_sp']:
                                        self.create_step_text_box('slow', 'division_location', 3)
                                if slow_current_add == 2:
                                    self.create_step_text_box('slow', 'velocity_change', 2)
                                    if not self.values['slow_eq_sp']:
                                        self.create_step_text_box('slow', 'division_location', 2)
                                slow_current_add -= 1
                                slow_diff += 1
                        self.previous_amount_slow = self.values['amount_slow_divisions']

                    slow_loop = self.values['amount_slow_divisions']
                    if event.ui_element == self.slow_velocity_change_tb_1:
                        self.values['slow_velocity_changes'][0] = float(event.text)
                    while slow_loop > 1:
                        match slow_loop:
                            case 2:
                                if not self.values['slow_eq_sp']:
                                    if event.ui_element == self.slow_step_location_tb_2:
                                        self.values['slow_division_locations'][0] = float(event.text)
                                if event.ui_element == self.slow_velocity_change_tb_2:
                                    self.values['slow_velocity_changes'][1] = float(event.text)
                            case 3:
                                if not self.values['slow_eq_sp']:
                                    if event.ui_element == self.slow_step_location_tb_3:
                                        self.values['slow_division_locations'][1] = float(event.text)
                                if event.ui_element == self.slow_velocity_change_tb_3:
                                    self.values['slow_velocity_changes'][2] = float(event.text)
                            case 4:
                                if not self.values['slow_eq_sp']:
                                    if event.ui_element == self.slow_step_location_tb_4:
                                        self.values['slow_division_locations'][2] = float(event.text)
                                if event.ui_element == self.slow_velocity_change_tb_4:
                                    self.values['slow_velocity_changes'][3] = float(event.text)
                            case 5:
                                if not self.values['slow_eq_sp']:
                                    if event.ui_element == self.slow_step_location_tb_5:
                                        self.values['slow_division_locations'][3] = float(event.text)
                                if event.ui_element == self.slow_velocity_change_tb_5:
                                    self.values['slow_velocity_changes'][4] = float(event.text)

                        slow_loop -= 1

                if self.fast_linear:
                    if event.ui_element == self.fast_linear_slope_tb:
                        self.values['slow_linear_slope'] = float(event.text)
                    if event.ui_element == self.fast_linear_yintercept_tb:
                        self.values['slow_linear_yintercept'] = float(event.text)
                if self.slow_linear:
                    if event.ui_element == self.slow_linear_slope_tb:
                        self.values['slow_linear_slope'] = float(event.text)
                    if event.ui_element == self.slow_linear_yintercept_tb:
                        self.values['slow_linear_yintercept'] = float(event.text)
                if self.fast_equation:
                    if event.ui_element == self.fast_equation_tb:
                        self.values['fast_equation'] = event.text
                if self.slow_equation:
                    if event.ui_element == self.slow_equation_tb:
                        self.values['slow_equation'] = event.text
                if event.ui_element == self.sample_frequency_tb:
                    self.values['sample_frequency'] = int(event.text)
                if event.ui_element == self.starting_velocity_tb:
                    self.values['starting_velocity'] = float(event.text)
                if event.ui_element == self.acceleration_tb:
                    self.values['acceleration'] = int(event.text)
            if event.type == pygame_gui.UI_SELECTION_LIST_DROPPED_SELECTION:
                if event.ui_element == self.slow_control_select:
                    self.clear_slow_control_zone()
                    self.slow_step = False
                    self.slow_linear = False
                    self.slow_equation = False

                if event.ui_element == self.fast_control_select:
                    self.clear_fast_control_zone()
                    self.fast_step = False
                    self.fast_linear = False
                    self.fast_equation = False
            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                if event.ui_element == self.slow_control_select:
                    self.clear_slow_control_zone()
                    if event.text == 'step':
                        self.step_control_layout('slow')
                        self.slow_step = True

                    if event.text == 'linear':
                        self.linear_control_layout('slow')
                        self.slow_linear = True

                    if event.text == 'equation':
                        self.equation_control_layout('slow')
                        self.slow_equation = True

                if event.ui_element == self.fast_control_select:
                    self.clear_fast_control_zone()
                    if event.text == 'step':
                        self.step_control_layout('fast')
                        self.fast_step = True

                    if event.text == 'linear':
                        self.linear_control_layout('fast')
                        self.fast_linear = True

                    if event.text == 'equation':
                        self.equation_control_layout('fast')
                        self.fast_equation = True

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_button:
                    self.values['start'] = True
                if event.ui_element == self.stop_button:
                    # Set treadmill to speed to 0
                    self.values['start'] = False
                if event.ui_element == self.end_button:
                    quit()
                if event.ui_element == self.weight_calibration_button:
                    self.values['weight_calibration_clicked'] = True
                    self.values['calibration_weight'] = self.values['fz']
                    pygame.draw.rect(self.screen, self.white, pygame.Rect(599,
                                                                          679,
                                                                          201,
                                                                          20))
                    calibrated_weight_text = self.font.render('Weight Calibrated: ' + str(round(self.values['fz'], 0))
                                                              + ' N', True, self.black)
                    self.screen.blit(calibrated_weight_text, (600, 680))



        return self.values

    def update(self, time_delta):
        self.manager.update(time_delta)
        self.manager.draw_ui(self.screen)
        pygame.display.update()

    def calc_update(self, values):
        self.values = values
