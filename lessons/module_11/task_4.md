---
index: 38
module: module_11
task: adaptive_racing
previous: visual_telemetry
next: 
---
# Task 4 Adaptive Racing

Starting settings for this exercise: `sensitivity = 245`, `max_speed = 40`, `kp = 25`, `braking_force = 20`.
Sensitivity is the Octoliner setup value (0–255); the detection threshold is a separate value applied to analog readings. Check the readings if lighting or sensor position changes.

## Objective
Demonstrate your ability to debug faulty logic, fix syntax errors, and organize code.

![Advanced](https://img.shields.io/badge/Difficulty-Advanced-red)

## Assignment
We have written an Advanced Adaptive Speed Controller for the rover's final race. However, the script is broken. The code contains **5 distinct bugs**.

Your task is to act as the Senior Engineer: find the bugs, fix them, and clean up the variables so the rover can navigate the track.

**Your Bug Hunt Checklist:**
1. **The Syntax Bug:** Python refuses to run the code.
2. **The Import Bug:** A crucial library is missing.
3. **The Setup Bug:** Something is initialized, but is not configured.
4. **The Array Bug:** The controller is trying to do math using an entire array of 8 sensors. Use the correct tracking function.
5. **The Coma Bug:** The rover is updating sensors too slowly.

## Conclusion
If you fix all 5 bugs and organize your variables, the rover will smoothly and rapidly navigate the final sector using adaptive braking. Good luck, Engineer!

Use the verified Metropolia starting settings: sensitivity `245`, `max_speed = 40`, `kp = 25`, `braking_force = 20`, and a `0.01` second loop pause. Keep the line-loss stop from the previous controller exercises. The robot starts at `(40, 18.5)` cm facing right and must pass `(105, 60)`, `(60, 79)`, then `(80, 16)` in order. Driving straight for 30 cm is not a completed race.
