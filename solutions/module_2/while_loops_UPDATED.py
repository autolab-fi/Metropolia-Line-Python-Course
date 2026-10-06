# All imports that you need

from lineRobot import Robot
import machine
import time
from octoliner import Octoliner
import math

robot = Robot()
radius = 3.4
Target_cm = 35

# Calculate Target
target = (Target_cm / (2 * math.pi * radius)) * 360

# Reset Encoders

robot.reset_left_encoder()
robot.reset_right_encoder()

# Run motors with low speed (values for each motor can be different)
robot.run_motor_left(150)
robot.run_motor_right(165)

# The Active Loop
last_report = -45
while  robot.encoder_degrees_left() < target:
    # Print the encoder data to see the progress
    degrees = robot.encoder_degrees_left()
    if degrees - last_report >= 45:
        print("Encoder degrees:", degrees)
        last_report = degrees

    # Small delay to let the processor send the print message
    time.sleep(0.02)

# This code only runs AFTER the loop finishes (Target Reached)
robot.stop_motor_left()
robot.stop_motor_right()

#Wait for full stop
time.sleep(0.2)

#Final encoder value after full stop
print("Final encoder degrees:", robot.encoder_degrees_left())

print("Target reached!")
print("Final value:", robot.encoder_degrees_left())
