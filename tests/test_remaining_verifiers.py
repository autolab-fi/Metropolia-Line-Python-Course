import ast
import contextlib
import io
import math
import os
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RemainingVerifiersTests(unittest.TestCase):
    def replay(self, name, positions, messages=(), code=None):
        module = {'logical_operators':'module_3', 'data_logging':'module_4', 'adaptive_racing':'module_11'}[name]
        path = ROOT/'verifications'/(module+'.py')
        fn = next(n for n in ast.parse(path.read_text()).body
                  if isinstance(n, ast.FunctionDef) and n.name == name)
        clock = SimpleNamespace(now=0)
        ns = {'math':math, 're':re, 'ast':ast, 'os':os, '__file__':str(path),
              'time':SimpleNamespace(time=lambda:clock.now), 'cv2':SimpleNamespace(imread=lambda p:None)}
        exec(compile(ast.Module(body=[fn], type_ignores=[]), str(path), 'exec'), ns)
        if code is None:
            filename = 'adaptive_racing_reference' if name == 'adaptive_racing' else name
            code = (ROOT/'solutions'/module/(filename+'.py')).read_text()
        robot = SimpleNamespace(position=positions[0], position_px=None,
                                draw_info=lambda x:x, get_msg=lambda:None)
        robot.get_info = lambda:{'position':robot.position}
        with contextlib.redirect_stdout(io.StringIO()):
            _,td,_,_ = ns[name](robot,None,None,code)
        for i,pos in enumerate(positions):
            clock.now=i+1
            robot.position=pos
            robot.get_msg=lambda:messages[i] if i<len(messages) else None
            _,td,_,_=ns[name](robot,None,td,code)
        clock.now=td['end_time']-.5
        robot.get_msg=lambda:None
        _,td,_,result=ns[name](robot,None,td,code)
        clock.now+=1
        _,_,_,later=ns[name](robot,None,td,code)
        self.assertEqual(result,later)
        return result

    def test_routes_require_ordered_lap(self):
        for name in ('logical_operators','adaptive_racing'):
            with self.subTest(task=name):
                self.assertTrue(self.replay(name,[(40,18.5),(105,60),(60,79),(80,16)])['success'])
                self.assertFalse(self.replay(name,[(40,18.5),(100,18.5)])['success'])
                self.assertFalse(self.replay(name,[(40,18.5),(60,79),(105,60),(80,16)])['success'])
                self.assertFalse(self.replay(name,[(40,18.5),(105,60),(60,79),(80,16)],code='pass')['success'])

    def test_logging_requires_complete_report(self):
        messages=['Mission Start!','Found: Green | Raw Data: R:123 G:94 B:62','End of transmission']
        self.assertTrue(self.replay('data_logging',[(45,18.5)]*3,messages)['success'])
        self.assertFalse(self.replay('data_logging',[(45,18.5)]*2,messages[:2])['success'])
        self.assertFalse(self.replay('data_logging',[(45,18.5)]*2,[messages[0],messages[2]])['success'])
