# Metropolia camera measurements

The backend's DPI=22 defines existing reset, docking, and floor-zone coordinates.
It is not an accurate physical-distance scale at robot-tag height. Do not change
it independently of those coordinates.

`verifications/camera_geometry.py` maps physical route lengths into that existing
coordinate system from the four initial tag corners. The black square side is
7.590647 cm, taken from the uploaded `new_ondroid_hamk_а4_rgb.pdf` used to create
the simulator's `top-tag.png` (the white quiet zone is excluded). Printing is
assumed to preserve PDF dimensions; confirm with a ruler before treating these
measurements as absolute metrology. No floor homography is applied to the elevated
tag. Perspective/lens distortion and mechanical slip remain within the checker's
normal tolerance.

The initial forward/right vectors are fixed for the whole route. They are derived
from camera observations, never from wheel encoders or the submitted program.
Malformed, mirrored, or severely distorted observations do not fall back silently
to the nominal DPI. Both sequential navigation and final navigation use the same
conversion. Checkpoint tolerance stays 4 existing camera units rather than growing
with every waypoint. Reset points, dock position, physical color/line zones,
student command distances, and the simulator's metric coordinates are unchanged.

After the MicroPython 1.29 PCNT migration, device 14 was calibrated to effective
`wrad=3.26`, `wdist=19.49`, `er=2300`. An unmodified sequential-navigation reference
failed run 21931: the robot stopped around x=98.9 while the old checker expected
x=107. The initial tag observation predicts the corrected endpoint around x=100.
Keep calibration and checker changes separate: altering motor geometry to satisfy
an inaccurate screen coordinate system would distort physical movement again.
