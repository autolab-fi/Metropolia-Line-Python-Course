import time
from lineRobot import Robot
from octoliner import Octoliner
import machine

robot = Robot()
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)
octoliner.set_sensitivity(245)

base_speed = 30
kp = 15

print("Beginning Bug Hunt")

# FIXED: Added missing colon
while True:
    sensor_array = octoliner.analog_read_all()
    position = octoliner.track_line()

    # FIXED: Corrected spelling from 'sensor' to 'sensor_array'
    # print(sensor_array)  # Optional debug print

    # FIXED: Changed > to < for correct failsafe logic
    if max(sensor_array) < 700:
        print("CRITICAL: Failsafe triggered! Stopping motors.")
        robot.stop()
        break

    else:
        # FIXED: Changed + to * for proportional amplification
        P = kp * position

        # FIXED: Subtracted P from right wheel to create steering differential
        left_speed = int(base_speed + P)
        right_speed = int(base_speed - P)

        # FIXED: Added missing 's' (run_motors_speed)
        robot.run_motors_speed(left_speed, right_speed)
        time.sleep(0.05)
