import ast, math, re
from pathlib import Path
from types import SimpleNamespace
import unittest
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'verifications/module_4.py'
FUNCTIONS = {n.name: n for n in ast.parse(SOURCE.read_text()).body if isinstance(n, ast.FunctionDef) and n.name in ('color_sensor_basics', 'color_classification')}
class ColorScanVerifierTests(unittest.TestCase):
    def run_scan(self, name, count=6, moved=60, split=False, bad_rgb=False, code=None):
        clock = SimpleNamespace(now=0); pending = []
        ns = {'time': SimpleNamespace(time=lambda: clock.now), 're': re}
        exec(compile(ast.Module(body=[FUNCTIONS[name]], type_ignores=[]), str(SOURCE), 'exec'), ns)
        code = code if code is not None else (ROOT / 'solutions/module_4' / (name+'.py')).read_text()
        robot = SimpleNamespace(position=(125,84), draw_info=lambda image: image, delta_points=math.dist, get_msg=lambda: pending.pop(0) if pending else None)
        _, td, _, _ = ns[name](robot, None, None, code)
        r = 300 if bad_rgb else 120
        row = f'Scan - R:{r} G:60 B:30' if name == 'color_sensor_basics' else f'Scan - Red (Raw: R:{r} G:60 B:30)'
        stream = row * count
        pending.extend([stream[:15], stream[15:]] if split else [stream])
        clock.now = 19.5; robot.position = (125,84-moved)
        _, td, _, result = ns[name](robot, None, td, code)
        clock.now = 22; robot.position = (125,24); pending.append(row*6)
        self.assertEqual(result, ns[name](robot, None, td, code)[3])
        return result['success']
    def test_six_scans_and_full_route(self):
        for name in FUNCTIONS:
            self.assertTrue(self.run_scan(name))
            self.assertTrue(self.run_scan(name, split=True))
    def test_five_scans_cannot_pass_on_later_frames(self):
        for name in FUNCTIONS: self.assertFalse(self.run_scan(name, count=5))
    def test_printed_scans_without_movement_fail(self):
        for name in FUNCTIONS:
            self.assertFalse(self.run_scan(name, moved=0))
            self.assertFalse(self.run_scan(name, moved=20))
    def test_invalid_readings_or_missing_program_fail(self):
        for name in FUNCTIONS:
            self.assertFalse(self.run_scan(name, bad_rgb=True))
            self.assertFalse(self.run_scan(name, code='pass'))
