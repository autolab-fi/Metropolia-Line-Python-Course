import ast
import re
import unittest
from pathlib import Path

source = Path(__file__).resolve().parents[1] / 'verifications/module_5.py'
function = next(n for n in ast.parse(source.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'has_line_loss_failsafe')
namespace = {'re': re}
exec(compile(ast.Module(body=[function], type_ignores=[]), str(source), 'exec'), namespace)

class FailsafeTests(unittest.TestCase):
    def test_accepts_the_published_threshold_with_normal_spacing_variants(self):
        for code in ['if max(sensor_array) < 700: pass', 'if max(readings)<700: pass', 'if max (readings) < 700.0: pass']:
            self.assertTrue(namespace['has_line_loss_failsafe'](code), code)

    def test_rejects_invalid_thresholds_and_unrelated_comparison(self):
        for code in ['if max(sensor_array) < 0: pass', 'if max(sensor_array) < -1: pass', 'if max(sensor_array) < 7000: pass', 'if sensor_array[0] < 700: pass']:
            self.assertFalse(namespace['has_line_loss_failsafe'](code), code)

    def test_accepts_calibrated_thresholds_and_named_constants(self):
        for code in ['if max(sensor_array) < 500: pass', 'loss_threshold = 450\nif max(sensor_array) < loss_threshold: pass']:
            self.assertTrue(namespace['has_line_loss_failsafe'](code))

    def test_does_not_count_comments_or_printed_code_as_failsafe(self):
        for code in ['# if max(sensor_array) < 700: pass', 'print("max(sensor_array) < 700")']:
            self.assertFalse(namespace['has_line_loss_failsafe'](code))

if __name__ == '__main__':
    unittest.main()
