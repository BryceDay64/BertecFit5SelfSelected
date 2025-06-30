import BertecRemoteControl
from time import sleep
import pygame

from BertecSelfSelectedSpeedGUI import BertecSelfSelectedSpeedGUI as Bertec


def set_treadmill(bertec_remote, velocity, acceleration):
    bertec_remote.run_treadmill(velocity, acceleration, acceleration, velocity, acceleration, acceleration)


remote = BertecRemoteControl.RemoteControl()
res = remote.start_connection()
try:
    # Defaults
    # Default Booleans:
    values = {'dead_zone': False,
              'stop_zone': False,
              'start': False,
              'slow_eq_sp': False,
              'fast_eq_sp': False,
              'weight_stop': False,
              'wrap': False,
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
              'slow_velocity_changes': [-0.01, -0.015, -0.02, -0.025, -0.03],
              'fast_division_locations': [0.112, 0.224, 0.336, 0.448],
              'fast_velocity_changes': [0.01, 0.015, 0.02, 0.025, 0.03],
              'slow_control_type': 'step',
              'fast_control_type': 'step'
              }

    values['fast_zone_height'] = (1.4-values['neutral_zone_height'])/2
    values['slow_zone_height'] = (1.4-values['neutral_zone_height'])/2

    gui = Bertec(values)

    weight_count = 0
    first_start = True
    first_stop = False
    positive_velocity = None

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
            values['fast_zone_height'] = (treadmill_length-values['origin_location']-values['neutral_zone_height']
                                          + values['neutral_zone_location']-values['dead_zone_height'])
        else:
            values['fast_zone_height'] = (treadmill_length - values['origin_location']
                                          - values['neutral_zone_height']+values['neutral_zone_location'])

        if values['stop_zone']:
            values['slow_zone_height'] = (values['origin_location'] - values['neutral_zone_location']
                                          - values['stop_zone_height'])
        else:
            values['slow_zone_height'] = values['origin_location'] - values['neutral_zone_location']

        res = remote.get_force_data()
        values['copx'] = res['copx']
        values['copy'] = res['copy']
        fz = res['fz']

        if fz > 100:
            weight_count = 0
            values['weight_stop'] = False
        else:
            weight_count += 1
        if weight_count >= values['sample_frequency']*2:
            values['weight_stop'] = True
        if values['weight_stop']:
            values['start'] = False
        if values['start']:
            if first_start:
                values['velocity_change'] = values['starting_velocity']
                if values['starting_velocity'] > 0:
                    positive_velocity = True
                elif values['starting_velocity'] < 0:
                    positive_velocity = False
                first_start = False
                first_stop = True
            else:
                if values['stop_zone'] and values['copy'] <= values['stop_zone_height']:
                    quit()
                elif values['copy'] < values['origin_location']-values['neutral_zone_location']:
                    distance_from_neutral = (values['origin_location']
                                             - values['neutral_zone_location'] - values['copy'])
                    match values['slow_control_type']:
                        case 'step':
                            match values['slow_eq_sp']:
                                case True:
                                    slow_eq_sp_divisions = []
                                    slow_eq_sp_divisions_size = round(
                                        values['slow_zone_height']/values['amount_slow_divisions'], 3)
                                    for division_num in range(0, values['amount_slow_divisions']):
                                        slow_eq_sp_divisions.append(division_num*slow_eq_sp_divisions_size)
                                    if distance_from_neutral < slow_eq_sp_divisions[-1]:
                                        values['velocity_change'] = (
                                            values['slow_velocity_changes'][values['amount_slow_divisions']-1])
                                    else:
                                        for division_num in range(0, len(slow_eq_sp_divisions)):
                                            if distance_from_neutral > slow_eq_sp_divisions[division_num]:
                                                values['velocity_change'] = values['slow_velocity_changes'][division_num]
                                case False:
                                    if distance_from_neutral < (
                                            values['slow_division_locations'][values['amount_slow_divisions']-1]):
                                        values['velocity_change'] = (
                                            values['slow_velocity_changes'][values['amount_slow_divisions']-1])
                                    else:
                                        for division_num in range(0, values['amount_slow_divisions']):
                                            if distance_from_neutral > values['slow_division_locations'][division_num]:
                                                values['velocity_change'] = values['slow_velocity_changes'][division_num]
                        case 'linear':
                            values['velocity_change'] = (-1*distance_from_neutral*values['slow_linear_slope']
                                                         - values['slow_linear_yintercept'])
                        case 'equation':
                            print('equation functionality not ready')
                            quit()
                elif values['dead_zone'] and values['copy'] > 1.4 - values['dead_zone_height']:
                    pass
                elif values['copy'] > (values['origin_location']
                                       - values['neutral_zone_location']+values['neutral_zone_height']):
                    distance_from_neutral = (values['copy']-values['origin_location']
                                             - values['neutral_zone_location']+values['neutral_zone_height'])
                    match values['fast_control_type']:
                        case 'step':
                            match values['fast_eq_sp']:
                                case True:
                                    fast_eq_sp_divisions = []
                                    fast_eq_sp_divisions_size = round(
                                        values['fast_zone_height'] / values['amount_fast_divisions'], 3)
                                    for division_num in range(0, values['amount_fast_divisions']):
                                        fast_eq_sp_divisions.append(division_num * fast_eq_sp_divisions_size)
                                    if distance_from_neutral > fast_eq_sp_divisions[-1]:
                                        values['velocity_change'] = (
                                            values['fast_velocity_changes'][values['amount_fast_divisions'] - 1])
                                    else:
                                        for division_num in range(0, len(fast_eq_sp_divisions)):
                                            if distance_from_neutral < fast_eq_sp_divisions[division_num]:
                                                values['velocity_change'] = values['fast_velocity_changes'][division_num]
                                case False:
                                    if distance_from_neutral > (
                                            values['fast_division_locations'][values['amount_fast_divisions']-1]):
                                        values['velocity_change'] = (
                                            values['fast_velocity_changes'][values['amount_fast_divisions']-1])
                                    else:
                                        for division_num in range(0, values['amount_fast_divisions']):
                                            if distance_from_neutral < values['fast_division_locations'][division_num]:
                                                values['velocity_change'] = values['fast_velocity_changes'][division_num]

                        case 'linear':
                            values['velocity_change'] = (distance_from_neutral * values['slow_linear_slope']
                                                         + values['slow_linear_yintercept'])
                        case 'equation':
                            print('equation functionality not ready')
                            quit()
                else:
                    values['velocity_change'] = 0

            values['current_velocity'] = values['current_velocity'] + values['velocity_change']
            if positive_velocity and values['current_velocity'] < 0:
                values['start'] = False
                values['wrap'] = True
            if not positive_velocity and values['current_velocity'] > 0:
                values['start'] = False
                values['wrap'] = True
            if values['velocity_change'] != 0:
                set_treadmill(remote, values['current_velocity'], values['acceleration'])

        if not values['start'] and first_stop:
            values['current_velocity'] = 0
            values['velocity_change'] = 0
            set_treadmill(remote, values['current_velocity'], 2)
            first_stop = False
            first_start = True

        gui.calc_update(values)

        gui.draw_treadmill()
        gui.update_text()

        pygame.display.flip()
        values = gui.events()
        gui.update(time_delta)

        sleep(1/values['sample_frequency'])
finally:
    set_treadmill(remote, 0, 2)
    pygame.quit()
