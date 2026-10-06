from lineRobot import Robot
from octoliner import Octoliner
import machine
import time

robot = Robot()
bus = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))

octoliner = Octoliner()
octoliner.begin(bus)
octoliner.set_sensitivity(245)

threshold = 700
speed = 30
turn_speed = 3

while True:
    sensor_data = octoliner.analog_read_all()
    if sensor_data[3] > threshold or sensor_data[4] > threshold:
        robot.run_motors_speed(speed, speed)
    elif sensor_data[0] > threshold or sensor_data[1] > threshold or sensor_data[2] > threshold:
        robot.run_motors_speed(speed, turn_speed)
    elif sensor_data[5] > threshold or sensor_data[6] > threshold or sensor_data[7] > threshold:
        robot.run_motors_speed(turn_speed, speed)
    else:
        robot.run_motors_speed(speed, speed)

    time.sleep(0.01)
