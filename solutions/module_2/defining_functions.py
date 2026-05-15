from lineRobot import Robot
import time

robot = Robot()

t_speed = 28
t_time = 1
t_offset = 10

def turn_180(sp, t, off):
    robot.run_motors_speed(sp, -(sp + off))
    time.sleep(t)
    robot.stop()

turn_180(t_speed, t_time, t_offset)
