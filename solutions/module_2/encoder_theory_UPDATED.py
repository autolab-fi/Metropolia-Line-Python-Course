from lineRobot import Robot
import time
import math

robot = Robot()
radius = 3.21  # Updated wheel radius in cm

# 1. Reset both encoders

robot.reset_left_encoder()
robot.reset_right_encoder()

# 2. Pulse: Start motors using manual PWM and wait - here you need to adjust parameters
robot.run_motor_left(550)
robot.run_motor_right(550)
time.sleep(0.8)

# 3. Stop motors manually to preserve encoder values
robot.stop_motor_left()
robot.stop_motor_right()

# 4. Read and print the encoder degrees
left_deg = robot.encoder_degrees_left()
print("Encoder degrees left:", left_deg)

# 5. Calculate distance in cm
distance = (left_deg / 360) * (2 * math.pi * radius)

# 6. Print the distance result
print("Distance in cm:", distance)
