import time
from lineRobot import Robot

robot = Robot()
tcs = robot.tcs3472
octoliner = robot.octoliner

# Configuration constants
SENSITIVITY = 240
LINE_LIMIT = 700
BASE_SPEED = 30
KP = 12

def get_mineral_color():
    """Detect mineral color with error handling"""
    try:
        r, g, b = tcs.rgb()
        total = r + g + b
        
        if r / total > 0.5:
            return "Red"
        elif g / total > 0.5:
            return "Green"
        else:
            return "Unknown"
    except ZeroDivisionError:
        return "Unknown"

def calculate_steering():
    """Calculate steering correction"""
    position = octoliner.track_line()
    return KP * position

def apply_movement(correction):
    """Apply motor speeds with correction"""
    left_speed = BASE_SPEED - correction
    right_speed = BASE_SPEED + correction
    robot.run_motors_speed(left_speed, right_speed)

# Main loop
while True:
    sensor_array = octoliner.analog_read_all()
    
    if max(sensor_array) < LINE_LIMIT:
        robot.stop()
        print("End of line")
        break
    
    # Check for minerals
    tcs.integration_time(SENSITIVITY)
    mineral = get_mineral_color()
    if mineral in ["Red", "Green"]:
        print(f"Mineral Detected: {mineral}!")
    
    # Line following
    correction = calculate_steering()
    apply_movement(correction)
    time.sleep(0.01)
