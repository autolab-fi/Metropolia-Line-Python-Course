# **Lesson 7.2: P-controller**

### Objective

Learn how to use the Octoliner’s ready-made `track_line()` method to build a **P controller** for smooth line following. You’ll understand what data the method returns, how to interpret it, and how to turn that into motor commands.

---

## 1. What is a P Controller?

A **Proportional (P) controller** adjusts the motor speeds based on how far the robot is from the center of the line.

**Formula:**

```
output = Kp × error
```

- `Kp` is the proportional gain (a tuning constant).
- `error` tells how far the robot is from the center of the line.

If the robot is far from center, the correction is large. If it’s close, the correction is small. This makes the motion smooth and responsive.

---

## 2. `track_line()` — The Ready-Made Line Position Method

The Octoliner library provides a helper method called **`track_line()`**. It processes all 8 sensors for you and returns the position of the line **as a single number**.

### ✅ What does `track_line()` return?

- A **floating-point value between `-1` and `1`**
  - `-1` → line is far to the **left**
  - `0` → line is **centered**
  - `1` → line is far to the **right**
- **`None`** if the line is **lost** (no sensors detect it)

This makes it perfect for a P controller: we can directly use the returned value as the error.

---

## 3. Using the Error to Control Motors

We use the line position as the error, then calculate a correction value:

```
correction = Kp × error
```

Then adjust motor speeds:

- **Left motor** speeds up if line is on the right.
- **Right motor** speeds up if line is on the left.

---

## 4. Code Example: P Controller with `track_line()`

```python
import machine
from time import sleep
from octoliner import Octoliner
from lineRobot import Robot

# I2C and Octoliner
i2c = machine.I2C(
    scl=machine.Pin(22),
    sda=machine.Pin(21),
    freq=100000
)

octoliner = Octoliner()
octoliner.begin(i2c)
octoliner.set_sensitivity(248)

# Robot
robot = Robot()

# Motor enable pins
pin5 = machine.Pin(5, machine.Pin.OUT)
pin15 = machine.Pin(15, machine.Pin.OUT)
pin5.value(1)
pin15.value(1)

# P controller constant
Kp = 30

# Base speed
base_speed = 20

while True:
    # Line position from -1 to 1
    error = octoliner.track_line()
    print(error)

    # If line is lost, stop or slow down
    if error is None:
        robot.run_motors_speed(0, 0)
        sleep(0.05)
        continue

    # P regulator
    correction = Kp * error

    left_speed = int(base_speed + correction)
    right_speed = int(base_speed - correction)

    robot.run_motors_speed(left_speed, right_speed)
    sleep(0.01)
```

---

## 5. Tuning Tips

- **Increase `Kp`** → stronger correction, faster reaction, but risk of oscillation.
- **Decrease `Kp`** → smoother motion, but slower response.
- **Adjust `base_speed`** to control overall speed.

---

## Assignment 7.2 – P Controller with `track_line()`

### ✅ Task

1. Use the **ready-made `track_line()` function** to read the line position.
2. Build a **P controller** with `Kp` and a `base_speed`.
3. Handle the case where the line is lost (`None`).
4. Tune `Kp` so the robot follows the line smoothly without oscillating.

### ✅ Checkpoint Goal

Your robot should follow the line smoothly and complete the checkpoint without zigzagging or losing the line.

---

## Summary

- `track_line()` gives you an easy-to-use **error value** between `-1` and `1`.
- A P controller turns that error into motor corrections.
- This method is simpler and cleaner than reading each sensor manually.

Next, we’ll extend this idea to PI and PID controllers for even better stability.
