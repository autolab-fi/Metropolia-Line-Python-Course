# All imports that you need

from lineRobot import Robot
import machine
import time
from octoliner import Octoliner
import math

robot = Robot()
radius = 3.21  # Updated wheel radius in cm
Target_cm = 39

# Calculate Target
target = (Target_cm / (2 * math.pi * radius)) * 360

# Reset Encoders

robot.reset_left_encoder()
robot.reset_right_encoder()

# Run motors with low speed (values for each motor can be different)
robot.run_motor_left(130)
robot.run_motor_right(130)

# The Active Loop
while robot.encoder_degrees_left() < target:
    # Print the encoder data to see the progress
    print(robot.encoder_degrees_left())

    # Small delay to let the processor send the print message
    time.sleep(0.02)

# This code only runs AFTER the loop finishes (Target Reached)
robot.stop_motor_left()
robot.stop_motor_right()

# Wait for full stop
time.sleep(0.2)

# Final encoder value after full stop
print(robot.encoder_degrees_left())

print("Target reached! Target was", target)
print("Final value:", robot.encoder_degrees_left())
