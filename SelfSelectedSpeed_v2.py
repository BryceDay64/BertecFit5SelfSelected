# import BertecRemoteControl
from time import sleep
import pygame

from BertecSelfSelectedSpeedGUI import BertecSelfSelectedSpeedGUI as Bertec

# TODO:
#  Add treadmill Control
#  Add COP marker
#  setting speed change in each division
#  adjusting speed
#  Future work: Add symbolic library for equation control X
#  add start and stop functionality
#  add equal spacing to step
#  Fix zone height readout

# Defaults
# Default Booleans:
values = {'dead_zone': False,
          'stop_zone': False,
          'start': False,
          'slow_eq_sp': False,
          'fast_eq_sp': False,
          'dead_zone_height': 0.1,
          'stop_zone_height': 0.28,
          'neutral_zone_height': 0.28,
          'origin_location': 0.7,
          'neutral_zone_location': 0.14,
          'amount_fast_divisions': 2,
          'amount_slow_divisions': 2,
          'sample_frequency': 20,
          'starting_velocity': 0,
          'current_velocity': 0,
          'acceleration': 1,
          'velocity_change': 0,
          'copx': 0,
          'copy': 0,
          'slow_linear_slope': 0.001,
          'slow_linear_yintercept': 0,
          'slow_equation': '0.001x',
          'fast_linear_slope': 0.001,
          'fast_linear_yintercept': 0,
          'fast_equation': '0.001x',
          'slow_division_locations': [0.112, 0.224, 0.336, 0.448],
          'slow_velocity_changes': [0.01, 0.015, 0.02, 0.025, 0.03],
          'fast_division_locations': [0.112, 0.224, 0.336, 0.448],
          'fast_velocity_changes': [0.01, 0.015, 0.02, 0.025, 0.03],
          'slow_control_type': 'step',
          'fast_control_type': 'step'
          }
gui = Bertec(values)

values['fast_zone_height'] = 1.4-int(values['neutral_zone_height'])/2
values['slow_zone_height'] = 1.4-int(values['neutral_zone_height'])/2

velocity_change_first_fast_division = 0.01
velocity_change_first_slow_division = 0.01

treadmill_width = 0.7   # meters
treadmill_length = 1.4  # meters

clock = pygame.time.Clock()

# Drawing Rectangle
while True:
    time_delta = clock.tick(60) / 1000.0

    # Actual zone calculations
    if values['dead_zone']:
        fast_zone_height = (treadmill_length-values['origin_location']-values['neutral_zone_height']
                            + values['neutral_zone_location']-values['dead_zone_height'])
    else:
        fast_zone_height = (treadmill_length - values['origin_location']
                            - values['neutral_zone_height']+values['neutral_zone_location'])

    if values['stop_zone']:
        slow_zone_height = values['origin_location'] - values['neutral_zone_location'] - values['stop_zone_height']
    else:
        slow_zone_height = values['origin_location'] - values['neutral_zone_location']

    gui.draw_treadmill(values)
    gui.update_text(values)

    pygame.display.flip()
    gui.events(values)
    gui.update(time_delta)

    sleep(1/values['sample_frequency'])
