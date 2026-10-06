---
index: 25
module: module_4
task: multiple_sensors
previous: color_classification
next: data_logging
---

# Mission 4.5 Working with Multiple Sensors

<!-- metropolia-guidance:start -->
## Metropolia setup notes

**Guidance updated: 2026-10-06.**
The reference run passed the physical checker on **2026-10-06** (run 21892).

Starting settings for this exercise: `sensitivity = 245`, `threshold = 700`, `speed = 30`, `turn_speed = 3`.
Sensitivity is the Octoliner setup value (0–255); the detection threshold is a separate value applied to analog readings. Facing forward, sensors 0–2 are on the right, 3–4 in the center, and 5–7 on the left.
These settings apply to the Metropolia robot and lighting at the validation date. Inspect the readings again after changes to lighting, sensor height, wiring, or the track; a passing simulation alone does not confirm hardware calibration.

For line-following over tape: Red r/sum > 0.55; Green g/sum > 0.325 AND r/sum < 0.45 AND g > 1.3*b; Blue b/sum > 0.245 AND r/sum < 0.45; otherwise Floor. Handle sum=0 separately. These are local measured starting thresholds, not universal calibration.
The simulator uses measured sample colors, but does not fully reproduce sensor illumination and tape overlap. Use physical observations to validate color thresholds.
<!-- metropolia-guidance:end -->


## Objective
Combine the Octoliner and the Color Sensor in a single program. The rover must autonomously follow a black line while simultaneously scanning the ground, using an LED to signal anomalies without stopping.

![Advanced](https://img.shields.io/badge/Difficulty-Advanced-red)

## Introduction
Up until now, your rover has been doing one job at a time: either following a line blindly or scanning colors while driving straight. Real Lunar rovers perform multiple tasks simultaneously. 

Now is a major integration time. You will take your line-following algorithm from Module 3 and merge it with your smart color scanner from Mission 4.4!

## Theory

### 1. Sharing the Brain (The I2C Bus)
Remember how both the Octoliner and the Color Sensor use the I2C pins (`sda=21, scl=22`)? Because they have different hardware addresses, you only need to create **one** I2C bus and pass it to both sensors:

```python
# Create one shared bus
shared_bus = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))

# Connect both sensors to the same bus!
octoliner.begin(shared_bus)
color_sensor = tcs3472(shared_bus)
```

### 1. The Spam Problem (State Tracking)
Your line-following program runs inside a fast `while True` loop. If you just add a `print(color_name)` command inside that loop, the rover will print "Red" hundreds of times while driving over a single red square!

To fix this, we need to teach the rover to remember the last color it saw, and only print a message when the color changes. We do this by creating a memory variable outside the loop:

```python
last_color = "Floor"

while True:
    current_color = # ... detect color ...
    
    if current_color != last_color:
        print(f"New color detected: {current_color}")
        # React to the color here!
        
    last_color = current_color # Update memory for the next loop
```

## Assignment
Merge your systems! Program the rover to follow the track. If it sees a Green zone, it must turn on its LED (Pin 15) while continuing to drive. If it sees a Blue zone, the mission is complete, and it must stop permanently.

**Requirements:**
1. Hardware: Initialize the shared I2C bus, Octoliner, Color Sensor, and the LED on Pin 15.
2. Function: Copy your completed `detect_color_name(r, g, b)` function from Mission 4.4 and paste it into your code.
    * *Hint*: For your first test run, you might need to adjust your thresholds for Green and Blue, as the black line might interfere with the sensor. To see exactly what the robot sees, add a temporary print statement inside your function right after calculating the ratios: `print(f"R: {r_ratio} | G: {g_ratio} | B: {b_ratio}")`
   On the Metropolia track, following the black line gives weaker color contrast than holding the sensor over a solid patch. Measured normalized values were G=0.332–0.342 on green, B=0.253–0.256 on blue, and G<=0.313 / B<=0.243 on the sampled floor. Start with the conditions below, then inspect your own readings if lighting or sensor placement changes:

   ```python
   if r_ratio > 0.55:
       return "Red"
   elif g_ratio > 0.325 and r_ratio < 0.45 and g > 1.3 * b:
       return "Green"
   elif b_ratio > 0.245 and r_ratio < 0.45:
       return "Blue"
   return "Floor"
   ```

   The green-to-blue comparison prevents a solid blue patch from being mistaken for green. These are measured starting thresholds for this arena, not universal sensor constants.

3. * **Scanner Logic:** Inside the `while True` loop, read the color and use the "Spam Filter" (`last_color`) logic.
    * If Green: Turn LED ON.
    * If Blue: Stop the robot and `break` the loop.
    * If Floor: Turn LED OFF (so it turns off when leaving the Green zone).
4. Line Following: Below the color logic, add your line-following `if/elif` block. Use sensitivity `245`, threshold `700`, speed `30` and turn speed `3` to start. Sensors `0–2` are on the right: steer right with `(speed, turn_speed)`. Sensors `5–7` are on the left: steer left with `(turn_speed, speed)`.
5. Output: Print each new classification only when the color changes: `print(f"{current_color} (Raw: R:{r} G:{g} B:{b})")`. After turning on the LED, print `"Green: led on"`; on blue, print `"Blue: Mission complete."`, stop and break. The physical checker uses these messages together with camera confirmation that the robot has stopped near the blue area.


## Conclusion
Congratulations! You have just programmed a truly multi-tasking robot. By using a shared I2C bus and a non-blocking LED signal, your rover can navigate complex terrain while simultaneously scanning for scientific anomalies. 

> **Important:** Save your entire script. In the final mission of this module, we will upgrade this code to turn the rover into a silent, data-gathering probe that generates a massive post-mission report!
