from lineRobot import Robot
from octoliner import Octoliner
from tcs3472 import tcs3472
import machine
import time

robot = Robot()
bus = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))

octoliner = Octoliner()
octoliner.begin(bus)
octoliner.set_sensitivity(240)

color_sensor = tcs3472(bus)

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

threshold = 700
speed = 30
turn_speed = 3

last_color = "Floor"

anomaly_log = []
mission_duration = 30
start_time = time.time()

print("Mission Start!")

while True:
    elapsed_time = time.time() - start_time

    if elapsed_time > mission_duration:
        robot.stop()
        break

    r, g, b = color_sensor.rgb()
    current_color = detect_color_name(r, g, b)

    if current_color != last_color and current_color != "Floor":
        anomaly_log.append([current_color, r, g, b])

    last_color = current_color

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

print("========")
print(" Transmitting mission report to Earth")
print("========")

print(f"Mission Duration: {mission_duration} seconds")
print(f"Total anomalies recorded: {len(anomaly_log)}\n")

for item in anomaly_log:
    c_name = item[0]
    r_val  = item[1]
    g_val  = item[2]
    b_val  = item[3]
    print(f"Found: {c_name} | Raw Data: R:{r_val} G:{g_val} B:{b_val}")

print("========")
print("End of transmission")
