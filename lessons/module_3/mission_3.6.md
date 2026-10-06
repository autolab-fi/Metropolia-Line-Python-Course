---
index: 19
module: module_3
task: simple_line_follower
previous: led_feedback
next: logical_operators
---

# Mission 3.6 Simple Line Follower

<!-- metropolia-guidance:start -->
## Metropolia setup notes

**Guidance updated: 2026-10-06.**
The reference run passed the physical checker on **2026-10-06** (run 21887).

Starting settings for this exercise: `sensitivity = 245`, `threshold = 700`, `speed = 15`, `turn_angle = 5`.
Sensitivity is the Octoliner setup value (0–255); the detection threshold is a separate value applied to analog readings. Facing forward, sensors 0–2 are on the right, 3–4 in the center, and 5–7 on the left.
These settings apply to the Metropolia robot and lighting at the validation date. Inspect the readings again after changes to lighting, sensor height, wiring, or the track; a passing simulation alone does not confirm hardware calibration.
<!-- metropolia-guidance:end -->


## Objective
Combine your spatial logic (`elif`) with motor commands to build a Relay (Bang-Bang) controller, allowing the rover to autonomously follow a line.

![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-orange)

## Introduction
You have successfully built a system that scans the ground, extracts specific data points, and reacts using LEDs. But the Artemis rover cannot rely on Mission Control to steer it manually based on blinking lights. 

It is time to close the loop. In this mission, we will replace the LED warning signals with actual steering commands. Your rover is about to drive itself!

## Theory

### 1. The Relay Controller (Bang-Bang)
The algorithm you are about to build is called a **Relay Controller** (also known as a Bang-Bang controller). It is the simplest type of automated control system. 

It does not care *how far* the robot is from the center of the line; it only knows binary states: Left, Right, or Center. 

Because the corrections are sharp and abrupt, a Relay controller usually results in a wobbling, zigzag movement along the line.

### 2. Steering Logic
To make the robot follow the track, we must think about *why* a specific sensor sees the line and *how* to fix it:
* If the **Center Scout** (Index 3) sees the line, we are perfectly aligned → **Drive Straight** (`speed, speed`).
* If the **Left Scout** (Index 6) sees the line, it means the rover has drifted too far to the *right* → **Steer Left** by slowing down the left motor (`turn_speed, speed`).
* If the **Right Scout** (Index 1) sees the line, it means the rover has drifted too far to the *left* → **Steer Right** by slowing down the right motor (`speed, turn_speed`).

## Assignment
Write an autonomous line-following algorithm using your scout sensors and `elif` logic. The rover must navigate a straight section of the track and pass through the checkpoints.

**Requirements:**
1. **Setup:** Define the variables: `threshold`, `speed`, `turn_angle`.
2. **Continuous Loop:** The rover must drive continuously. Use an infinite `while True:` loop.
3. **Read Data:** Inside the loop, read octoliner and extract your three scouts (index 1, 3/4, and 6) into variables.
4. **Steering Logic (`if/elif/else`):** Start with `turn_left_angle(turn_angle)` / `turn_right_angle(turn_angle)` using `turn_angle = 5` degrees. Differential motor-speed steering is an alternative that needs its own tuning.
5. **Stability:** Add a tiny delay at the end of the loop.

*Hint*: in the loop, it's better to print sensor's data in order to understand what values should be set as a treshhold and sensitivity.

## Conclusion
Congratulations! You have just programmed your first autonomous robot. 

Watch how it navigates the track. You will notice the characteristic "wobble" of the Relay controller as it bounces between its left and right sensors. 

**Wait, did the rover lose the line on a sharp turn?** Because we are only using 3 "scout" sensors, there are blind spots between them! If the line slips under Sensor 2 or Sensor 4, the rover won't see it. In our next and final mission of the module, we will learn how to activate all 8 sensors at once to fix this blind spot!
