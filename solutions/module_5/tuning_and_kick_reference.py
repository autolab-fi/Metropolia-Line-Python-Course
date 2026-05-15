import machine
import time
from lineRobot import Robot
from octoliner import Octoliner

robot = Robot()
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
octoliner = Octoliner()
octoliner.begin(i2c)

octoliner.set_sensitivity(245)

base_speed = 40
kp = 20

last_kick_time = time.time()  # Timer before loop

while True:
    sensor_array = octoliner.analog_read_all()
    time.sleep(0.01)
    position = octoliner.track_line()

    # Failsafe Check
    if max(sensor_array) < 700:
        print("Line lost! Emergency Stop.")
        robot.stop()
        break

    elapsed_time = time.time() - last_kick_time

    if elapsed_time > 5:
        print("KICK!")
        robot.run_motors_speed(40, -40)
        time.sleep(0.15)
        last_kick_time = time.time()  # Reset timer

    else:
        # P-Controller
        P = kp * position
        left_speed = int(base_speed + P)
        right_speed = int(base_speed - P)
        robot.run_motors_speed(left_speed, right_speed)

    time.sleep(0.01)
