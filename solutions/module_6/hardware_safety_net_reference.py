import time
from lineRobot import Robot
robot = Robot()

def detect_color_name(r, g, b):
    total = r + g + b
    
    try:
        # Protected division
        r_ratio = r / total
        g_ratio = g / total

        if r_ratio > 0.4:
            return "Red"
        elif g_ratio > 0.4:
            return "Green"
        else:
            return "Floor"

    except ZeroDivisionError:
        print("CRITICAL: Sensor Blind!")
        return "Unknown"

# Simulated scans with injected "Shadow Zones" (0,0,0)
scans = [(140, 30, 30), (0, 0, 0), (50, 150, 50), (0, 0, 0), (0, 0, 0), 
         (60, 60, 60), (150, 40, 40), (0, 0, 0), (40, 140, 40), (70, 70, 70)]

scan_num = 1
for r, g, b in scans:
    robot.run_motors_speed(25, -25)
    time.sleep(0.2)
    robot.stop()

    print(f"Sector #{scan_num}")
    color = detect_color_name(r, g, b)
    print(f"ANALYSIS: {color}\n")
    time.sleep(0.3)
    scan_num += 1

print("Survey Complete")
