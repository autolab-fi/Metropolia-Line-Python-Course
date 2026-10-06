---
index: 29
module: module_5
task: proportional_control
previous: upgraded_relay_controller
next: adaptive_speed
---

# Mission 5.3 Proportional Control Logic

<!-- metropolia-guidance:start -->
## Metropolia setup notes

**Guidance updated: 2026-10-06.**
The reference run passed the physical checker on **2026-10-06** (run 21872).

Starting settings for this exercise: `sensitivity = 245`, `base_speed = 30`, `kp = 20`.
Sensitivity is the Octoliner setup value (0–255); the detection threshold is a separate value applied to analog readings. Facing forward, sensors 0–2 are on the right, 3–4 in the center, and 5–7 on the left.
These settings apply to the Metropolia robot and lighting at the validation date. Inspect the readings again after changes to lighting, sensor height, wiring, or the track; a passing simulation alone does not confirm hardware calibration.
<!-- metropolia-guidance:end -->


## Objective
Understand the mathematical concept of Proportional Control and write a P-controller algorithm to smoothly steer the rover based on the continuous Error gradient.

![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-orange)

## Introduction
Your Upgraded Relay Controller in the last mission was smart, but it still wobbled. Why? 
Because it still turned at a *fixed* speed, regardless of the situation. Whether the rover drifted 2 millimeters or 5 centimeters off the line, it applied the exact same turning force. 

Imagine driving a car on a highway. If you drift slightly from the center of your lane, you don't instantly yank the steering wheel all the way to the side! You make a *small* correction. If you drift significantly, you make a *larger* correction.

This natural driving logic is called a **Proportional Controller (P-Controller)**. The steering correction is directly proportional to the size of the error. Now we will teach rover to drive like a professional.

## Theory

### 1. The Amplification Problem
Our `track_line()` function gives us an Error value from `-1.0` to `1.0`. 
If the rover's base speed is `25`, and the Error is `0.5`, what happens if we just add the Error to the speed? The new speed becomes `25.5`. That tiny difference will not turn the robot at all.

To turn this small decimal Error into a strong motor command, we must amplify it by multiplying it by a constant number. In control theory, this amplifier is called the **Proportional Coefficient**, or *K_p*.

### 2. The Math of Steering
The formula for a Proportional Controller is beautiful in its simplicity. 

First, we calculate the required steering power *P* using our coefficient *K_p*: **P = K_p * Error**

Next, we apply this steering power to the wheels. To turn smoothly, we *add P* to the left motor and *subtract P* from the right motor.
* **`left_speed = base_speed + P`**
* **`right_speed = base_speed - P`**

**Let's test the math:** Imagine the line drifts to the right (Error = `0.5`). Let's say our *K_p* is `30`, and `base_speed` is `25`.
1. Calculate Power: P = 30 * 0.5 = 15
2. Left Motor: 25 + 15 = 40
3. Right Motor: 25 - 15 = 10

Because the left wheel is now spinning at `40` and the right wheel at `10`, the rover smoothly arcs to the right, perfectly bringing the line back to the center! If the Error was smaller (e.g., `0.1`), the speed difference would be much smaller, resulting in a gentle, almost invisible correction.

## Assignment
Write a Proportional Control loop to navigate the track. You will replace your bulky `if/elif/else` steering blocks with just three elegant lines of mathematical code.

**Requirements:**
1. **Setup:** Initialize `Robot`, the I2C bus and `Octoliner` as in the previous mission. Set `octoliner.set_sensitivity(245)`. Use the `machine` and `time` modules; this controller does not need the `math` library.
2. **Control Variables:** Before the loop, create two variables:
   * `base_speed = 30`
   * `kp = 20` (The starting coefficient verified on the Metropolia track).
3. **The Loop:** Inside your `while True:` loop:
   * Read `sensor_array = octoliner.analog_read_all()`, wait `time.sleep(0.01)`, then read `position = octoliner.track_line()`.
   * Include the Failsafe from the previous mission: if `max(sensor_array) < 700`, print a critical error message, call `robot.stop()`, and `break`.
   * If the data is valid (`else:`), perform the P-Controller math:
     * Calculate `P` by multiplying `kp` and `position`.
     * Calculate `left_speed` and `right_speed`. *(Note: Wrap your final math in `int()` like this: `int(base_speed + P)` to ensure the motor function receives whole numbers).*
     * Send the speeds to the motors using `run_motors_speed()`.
   * Keep `time.sleep(0.01)` at the end of the loop. A longer delay changes the controller response; use these timings for the initial run.

4. **Route:** Follow the line through all three checkpoints in order. Driving only the first straight section is not enough to pass. If the failsafe stops the rover before the route is complete, review the starting parameters and loop timing, then retry.

Execute the code! Watch closely. The rover should navigate the track much smoother than before, automatically adjusting its turn sharpness.

## Conclusion
Brilliant! You have successfully implemented a Proportional Controller. 

Look at your code: you replaced complicated logical conditions with pure, elegant mathematics. The rover repeatedly adjusts both wheel speeds in proportion to the measured line error.

However, you might notice it still isn't *perfect*. Maybe it turns a little too sluggishly, or maybe it shakes a bit on the straightaways. In the next mission, we will learn how engineers **"Tune"** the *K_p* value to achieve flawless movement!

> **Important:** Save your standard P-Controller math. You will need to copy and paste this into your next mission.
