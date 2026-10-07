# Metropolia selected-course validation — 2026-10-07

Scope: the 21 required tasks selected for Moodle course 2 / Ondroid course 11,
Python Programming for Mobile Robotics @ Metropolia. Optional sandbox and
archived tasks are outside the physical audit.

All 21 canonical physical references completed successfully under test account
DmitryS (user 32). The database was rechecked after the final run: all 21 have
`status=success` and `finished=true`. Videos were confirmed at completion in the
saved run records; older videos are not all retained in the current database.

| Task | Successful physical submission |
| --- | --- |
| `welcome` | 21955 |
| `test_drive` | 21956 |
| `directional_movement` | 21945 |
| `python_variables_commands` | 21929 |
| `maneuvering` | 21930 |
| `sequential_navigation` | 21934 |
| `electric_motors` | 21952 |
| `defining_functions` | 21953 |
| `for_loops` | 21941 |
| `python_lists` | 21954 |
| `intro_to_octoliner` | 21957 |
| `conditional_logic` | 21958 |
| `processing_sensor_data` | 21959 |
| `arrays_and_elif` | 21960 |
| `led_feedback` | 21961 |
| `simple_line_follower` | 21966 |
| `logical_operators` | 21963 |
| `concept_of_error` | 21974 |
| `upgraded_relay_controller` | 21970 |
| `proportional_control` | 21971 |
| `adaptive_speed` | 21972 |

## Final Concept of Error change

- Physical start: `(108, 65)`, direction `(0, -30)` (facing up), on the right-hand line.
- Three supervised trials from the dock passed with the unchanged 5 cm departure.
  Core reset times: 24.509, 24.706, 24.723 seconds, with internal corrections.
- Ordinary submission 21974 passed with grade and video. Reset activity completed
  on attempt 1 in 28.198 seconds, including preparation. Physical readings:
  left `[0.25, 0.75, 1, 1, 1]`, right `[-0.5, -1, -1, -1, -1]`.
- Simulator start: `(1.02, 0.35)` metres, heading `pi/2`. This aligns the sensor
  with the simulator artwork; a literal camera-coordinate conversion to x=1.08
  passed the basic checker but failed to illustrate the second sweep.
  With the chosen start, readings are left `[0.375, 0.5, 0.625, 0.875, 1]`,
  right `[-0.5, -0.625, -0.875, -1, -1]`.
- Same canonical Concept program in both environments. Lesson and tutor context
  describe the start and the discrete, last-valid-value behaviour of track_line.
- Simulator curriculum regression now checks that both Concept reference sweeps
  change values and demonstrate the expected signs, in addition to task checks.

## Validation and limits

Course unit/replay suite: 77 passed. Final simulator curriculum suite: all 35
course tasks, 140 cases (reference, renamed reference, empty and output-only),
matched expectations. This includes all 21 selected Moodle tasks.

Timed open-loop exercises intentionally use environment-specific tuned reference
parameters where configured (Electric Motors and Defining Functions). Passing
both environments does not mean their motor dynamics or numerical settings are
identical. Simulator coordinates follow its artwork rather than an exact camera map.

The Relay route requirement and frozen Concept verdict were regression-tested
with positive and negative cases. The final Concept live run also used the new
grader. This audit is finite evidence, not a guarantee that every future reset
or connection will succeed. The old dock-side Concept reset route exhibited
uncommanded rotation near the dock; relocating this task avoids that route,
but does not change the general reset planner or diagnose the mechanical cause.
No firmware, calibration, motor-speed or worker changes are part of this update.

After the final physical run the robot was docked, three fresh samples confirmed
charging (last battery 24.62 V, input 24.9575 V), Stop was acknowledged, automatic
charging restored and the maintenance lease released.
