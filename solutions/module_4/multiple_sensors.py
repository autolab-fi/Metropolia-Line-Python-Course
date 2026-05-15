from lineRobot import Robot
from octoliner import Octoliner
from tcs3472 import tcs3472
import machine
import time

robot = Robot()
bus = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))

octoliner = Octoliner()
octoliner.begin(bus)
octoliner.set_sensitivity(245)

color_sensor = tcs3472(bus)

led = machine.Pin(15, machine.Pin.OUT)
led.value(0)

def detect_color_name(r, g, b):
    total = r + g + b
    if total == 0:
        return "Floor"
    r_ratio = r / total
    g_ratio = g / total
    b_ratio = b / total
    if r_ratio > 0.55:
        return "Red"
    elif g_ratio > 0.40:
        return "Green"
    elif b_ratio > 0.35:
        return "Blue"
    else:
        return "Floor"

threshold  = 700
speed      = 30
turn_speed = 3
last_color = "Floor"

print("Goal: LED on GREEN, Stop on BLUE.")

while True:
    r, g, b = color_sensor.rgb()
    current_color = detect_color_name(r, g, b)
    print(f"{current_color} (Raw: R:{r} G:{g} B:{b})")

    if current_color != last_color:
        if current_color == "Green":
            print("Green: led on")
            led.value(1)
        elif current_color == "Blue":
            print("Blue: Mission complete.")
            robot.stop()
            break
        elif current_color == "Floor":
            led.value(0)

    last_color = current_color

    sensor_data = octoliner.analog_read_all()
    if sensor_data[3] > threshold or sensor_data[4] > threshold:
        robot.run_motors_speed(speed, speed)
    elif sensor_data[0] > threshold or sensor_data[1] > threshold or sensor_data[2] > threshold:
        robot.run_motors_speed(turn_speed, speed)
    elif sensor_data[5] > threshold or sensor_data[6] > threshold or sensor_data[7] > threshold:
        robot.run_motors_speed(speed, turn_speed)
    else:
        robot.run_motors_speed(speed, speed)

    time.sleep(0.01)
