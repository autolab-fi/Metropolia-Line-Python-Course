import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MeasuredPaletteTests(unittest.TestCase):
    def test_measured_floor_and_line_patch_samples(self):
        samples = {
            'Floor': [(133,79,59),(129,89,66),(130,88,70),(132,87,67),(133,89,69),(0,0,0)],
            'Green': [(123,94,62),(123,96,62),(125,94,64),(125,95,64),(104,107,52),(101,106,49),(30,220,30)],
            'Blue': [(127,89,73),(126,89,74),(127,90,74),(125,88,72),(85,94,101),(30,30,220)],
            'Red': [(220,30,30)],
        }
        for task in ('multiple_sensors', 'data_logging'):
            path = ROOT/'solutions/module_4'/(task+'.py')
            fn = next(n for n in ast.parse(path.read_text()).body
                      if isinstance(n, ast.FunctionDef) and n.name == 'detect_color_name')
            namespace = {}
            exec(compile(ast.Module(body=[fn], type_ignores=[]), str(path), 'exec'), namespace)
            for expected, values in samples.items():
                for rgb in values:
                    with self.subTest(task=task, rgb=rgb):
                        self.assertEqual(namespace['detect_color_name'](*rgb), expected)
