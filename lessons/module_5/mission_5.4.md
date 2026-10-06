---
index: 31
module: module_5
task: adaptive_speed
previous: proportional_control
next: art_of_debugging
---

# Mission 5.4 Adaptive Speed 

## Objective
Make the rover race-ready by implementing an Adaptive Speed algorithm that automatically slows down before corners using the `abs()` function.

![Advanced](https://img.shields.io/badge/Difficulty-Advanced-red)

## Introduction
Your Proportional Controller is stable, but it has a flaw: it drives at a constant `base_speed`. 
If you set the speed to `30`, the robot easily navigates sharp corners, but crawls agonizingly slowly on straightaways. If you increase the speed to `80`, it flies down the straights but crashes on the first sharp turn because it's going too fast to steer!

Think about real racing drivers. They don't press the gas pedal identically the whole track. They accelerate on the straights and hit the brakes *before* entering a turn. Today, we will teach your rover to do exactly that.

## Theory
### 1. Absolute Error (`abs`)
To know *when* to brake, the robot needs to know if it's approaching a turn. 
Our Error ranges from `-1.0` to `1.0`. We don't care if the turn is left or right; we only care about the *size* of the Error. 

Python has a built-in function called `abs()` (Absolute Value) that removes the minus sign:
* `abs(-0.8)` becomes `0.8`
* `abs(0.0)` stays `0.0`

### 2. The Adaptive Speed Formula
Instead of a fixed `base_speed`, we will calculate a `dynamic_speed` every single loop using this formula:
`dynamic_speed = max_speed - (braking_force * abs(position))`

* On a straight line (`position = 0.0`), the robot drives at the full `max_speed`.
* On a sharp turn (e.g., `position = 1.0`), the robot subtracts the full `braking_force` from its speed, safely slowing down to execute the turn!

## Assignment
Upgrade your P-Controller to the ultimate Adaptive Speed Controller!

**Requirements:**
1. **Setup:** Use your code from Mission 5.3.
2. **Control Variables:** Remove `base_speed`, set `kp = 25`, and create two new variables before the loop:
   * `max_speed = 40`
   * `braking_force = 20`
3. **Adaptive Math:** Inside the loop, before calculating `P`:
   * Calculate `dynamic_speed` using the formula with `abs(position)`.
4. **The P-Controller:**
   * Calculate `P` as usual (`kp * position`).
   * Calculate `left_speed` and `right_speed` using your new `dynamic_speed` instead of a fixed base speed. Don't forget to use `int()`!
5. **Execute:** Send the speeds to the motors. Watch your robot accelerate on the straights, dynamically brake for the corners, and **complete one full lap!**

**Verification:** Start with sensitivity `245`, a `0.01` second pause after reading the sensor array, and a `0.01` second pause at the end of the loop. Keep the `max(sensor_array) < 700` stop-and-break failsafe. The robot starts on the line facing right. The physical check lasts about `60` seconds and requires all three checkpoints in order; the simulator ends after that route is complete.

**The Tuning Challenge (Optional):**
After completing a lap, change one parameter at a time and compare the result:
* Increase or decrease `kp` slightly and observe steering corrections.
* Change `braking_force` and compare the speed on straights and corners.
* Increase `max_speed` in small steps only after the current setup reliably completes the route.

Retain the line-loss failsafe for every experiment.

## Conclusion
You have built a controller that adjusts its speed using the measured line error. Compare its lap with the fixed-speed controller from Mission 5.3 and change one parameter at a time when tuning.
