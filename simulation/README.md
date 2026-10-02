# Browser simulation configuration

`manifest.json` defines start poses and checks for all 36 Pilot activities.
Every activity uses `simulation-and-lab`: both execution targets are available,
and simulator success never completes a lesson; physical verification is required. `lessons-list.json` carries the corresponding execution modes.
`course-info.json` publishes the generated configuration URL via
`simulationManifestUrl`. These source changes must be published and synchronized
with the backend before the production interface exposes the new modes.

Physical verification remains in `verifications/`. Browser checks run on actual
simulated motion, sensor events and program output, with source requirements where
the lesson explicitly requires a programming construct. Welcome and Sandbox are
ungraded activities; accepting an empty program there is intentional.

From the sibling `browser-robot-sim` repository, run `npm run build` to generate
`public/courses/metropolia-line/simulation-config.json`. Run
`npm run test:metropolia` with the private trusted-reference fixture installed to
check every activity against a correct program, a renamed robot variable, an empty
program and output-only cheating. The fixture is ignored by Git and is never
included in the student bundle. The generated audit records hashes, not solutions.

The October 2026 browser audit passes all 144 cases. Motion and sensor checks cover
manual drive, encoder distance, LED classification, color stops, ordered track
checkpoints, controller safety stops, timed kicks and telemetry. Reset terminates
an active Python worker, and each execution gets a fresh Python namespace.

## Physical alignment and limits

The Metropolia model uses device 14 settings: wheel radius 3.4 cm, wheelbase 19 cm,
2300 encoder pulses per revolution and maximum wheel speed 13 rad/s. Distance and
standard-turn timing use measured square runs from 2026-10-02. Both left and right
20 cm squares completed all segments; their closure errors were 1.61 cm and
0.49 cm respectively. These measurements support primitive motion only; they do
not establish acceptance of every course program on the physical track.

Raw PWM response is still provisional and inherited from HAMK. Color readings are
synthetic; acceleration, battery state and wheel slip are not modeled. Full-track
controllers and raw-motor exercises require separate physical acceptance.

Camera coordinates convert centimetres to metres and invert Y. Task-local pose
offsets keep the simulated body inside the arena or align its sensors with the
printed track. The full-loop final checkpoint is (80, 16) cm in camera coordinates,
corresponding to (0.80, 0.84) m in the simulator. Start poses and tolerances must be
reviewed against real runs; simulator success alone is insufficient evidence.

The electric-motor finish tolerance is 10 cm, matching the physical grader.
The while-loop exercise targets 39 cm using a 3.4 cm wheel radius, with the wall at
40 cm. The physical grader requires camera displacement as well as encoder output
to reject fabricated readings. Line-loss controller checks use the lesson's 700
threshold. Sensor indexing follows the robot API: left zone 5–7, right zone 0–2.

`generated/task-metadata.json` is derived from physical verifier target points via
`npm run course:extract`; explicit manifest overrides control browser start poses.
See the simulator's generated curriculum and physical-parity reports for evidence.
