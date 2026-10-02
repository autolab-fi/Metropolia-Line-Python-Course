"""Exercise the physical verdict with camera/encoder evidence, without a robot."""
import ast
import math
from pathlib import Path
from types import SimpleNamespace
import unittest

source = Path(__file__).resolve().parents[1] / 'verifications/module_2.py'
function = next(n for n in ast.parse(source.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'while_loops')
clock = SimpleNamespace(now=0.0)
namespace = {
    'math': math,
    'time': SimpleNamespace(time=lambda: clock.now),
    'cv2': SimpleNamespace(line=lambda *args: None),
}
exec(compile(ast.Module(body=[function], type_ignores=[]), str(source), 'exec'), namespace)
verify = namespace['while_loops']

class WallVerdictTests(unittest.TestCase):
    def verdict(self, distance_cm, encoder_cm=None, code='while robot.encoder_degrees_left() < target:\n    print(robot.encoder_degrees_left())'):
        clock.now = 0
        message = None
        robot = SimpleNamespace(position=(30., 50.), position_px=(600, 1000),
            draw_info=lambda frame: frame, get_msg=lambda: message)
        frame = SimpleNamespace(shape=(2000, 3000, 3))
        _, state, _, _ = verify(robot, frame, None, code)
        robot.position = (30. + distance_cm, 50.)
        robot.position_px = (int(robot.position[0] * 20), 1000)
        if encoder_cm is not None:
            message = str(encoder_cm / (2 * math.pi * 3.4) * 360)
        clock.now = 16
        return verify(robot, frame, state, code)[3]

    def test_correct_39_cm_run_passes(self):
        self.assertTrue(self.verdict(39, 39)['success'])

    def test_old_20_cm_solution_is_incomplete(self):
        self.assertFalse(self.verdict(20, 20)['success'])

    def test_fabricated_encoder_without_camera_motion_fails(self):
        self.assertFalse(self.verdict(0, 39)['success'])

    def test_wall_contact_fails(self):
        self.assertFalse(self.verdict(40, 39)['success'])

    def test_missing_encoder_fails(self):
        self.assertFalse(self.verdict(39)['success'])

    def test_banned_navigation_fails(self):
        self.assertFalse(self.verdict(39, 39, 'robot.move_forward_distance(39)')['success'])

if __name__ == '__main__':
    unittest.main()
