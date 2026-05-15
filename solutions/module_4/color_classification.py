from lineRobot import Robot
import machine
from tcs3472 import tcs3472
import time

robot = Robot()

bus = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))
color_sensor = tcs3472(bus)

def detect_color_name(r, g, b):
    total = r + g + b
    if total == 0:
        return "Unknown"
    r_ratio = r / total
    g_ratio = g / total
    b_ratio = b / total
    if r_ratio > 0.5:
        return "Red"
    elif g_ratio > 0.4:
        return "Green"
    elif b_ratio > 0.4:
        return "Blue"
    else:
        return "Floor"

for step in range(6):
    r, g, b = color_sensor.rgb()
    detected_color = detect_color_name(r, g, b)
    print(f"Scan complete: {detected_color} (Raw: R:{r} G:{g} B:{b})")
    robot.move_forward_distance(10)
    time.sleep(0.5)

print("Smart scan complete.")
