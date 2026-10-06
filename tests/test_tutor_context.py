import ast
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_tutor_context', ROOT/'scripts/build_tutor_context.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class TutorContextTests(unittest.TestCase):
    def test_generated_context_is_fresh(self):
        builder.build(check=True)

    def test_parameters_match_reference_and_populated_starters(self):
        notes = json.loads((ROOT/'tutor/task-notes.json').read_text())['tasks']
        lessons = {t['str_id']: t for m in json.loads((ROOT/'lessons-list.json').read_text()) for t in m['lessons']}
        for key,note in notes.items():
            with self.subTest(task=key):
                source = (ROOT/note['reference']).read_text()
                tree = ast.parse(source)
                constants = {n.targets[0].id: n.value.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and isinstance(n.value,ast.Constant)}
                calls = [n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='set_sensitivity']
                for name,value in note['parameters'].items():
                    if name=='sensitivity':
                        self.assertTrue(calls)
                        arg=calls[0].args[0]
                        actual=arg.value if isinstance(arg,ast.Constant) else constants[arg.id]
                        self.assertEqual(actual,value)
                    else:
                        self.assertEqual(constants[name],value)
                if note['physicalValidation']['status']=='verified':
                    self.assertIsNotNone(note['physicalValidation']['submissionId'])
                    self.assertIsNotNone(note['physicalValidation']['date'])
                self.assertEqual(lessons[key]['executionMode'],'simulation-and-lab')

    def test_racing_starter_has_the_five_documented_fixes(self):
        lessons = {t['str_id']:t for m in json.loads((ROOT/'lessons-list.json').read_text()) for t in m['lessons']}
        code=lessons['adaptive_racing']['template']
        self.assertNotIn('import time',code)
        for old,new in [('while True\n','while True:\n'),('set_sensitivity()','set_sensitivity(245)'),('position = sensor_array','position = octoliner.track_line()'),('time.sleep(5)','time.sleep(0.01)')]:
            self.assertEqual(code.count(old),1)
            code=code.replace(old,new)
        ast.parse('import time\n'+code)
        self.assertIn('robot.stop()',code)
        self.assertIn('max(sensor_array) < 700',code)

if __name__=='__main__': unittest.main()
