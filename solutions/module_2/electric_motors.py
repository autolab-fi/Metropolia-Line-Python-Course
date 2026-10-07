from lineRobot import Robot
import time
robot = Robot()
robot.run_motors_speed(28, 50.5)
time.sleep(2.5)
robot.stop()
