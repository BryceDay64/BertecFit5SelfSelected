import BertecRemoteControl
from time import sleep

remote = BertecRemoteControl.RemoteControl()
res = remote.start_connection()
print(res)


initialize_velocity = input("Set the initial velocity")

params = remote.get_run_treadmill_user_input()
res = remote.run_treadmill(initialize_velocity, 1, 1, initialize_velocity, 1, 1)

velocity = initialize_velocity

while True:
    res = remote.get_force_data()

    copy = res['copy']

    if copy >= 1.12:
        velocity = velocity+0.2
        res = remote.run_treadmill(velocity, 1, 1, velocity, 1, 1)
    elif copy >= 0.84:
        velocity = velocity+0.1
        res = remote.run_treadmill(velocity, 1, 1, velocity, 1, 1)
    elif copy <= 0.56:
        velocity = velocity-0.1
        res = remote.run_treadmill(velocity, 1, 1, velocity, 1, 1)
    elif copy <= 0.28:
        velocity = velocity-0.2
        res = remote.run_treadmill(velocity, 1, 1, velocity, 1, 1)
    elif copy <= 0.1:
        velocity = 0
        res = remote.run_treadmill(velocity, 1, 1, velocity, 1, 1)
        break
    sleep(0.05)
