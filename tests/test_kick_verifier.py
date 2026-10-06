"""Replay the measured line route and verify that a final verdict stays final."""
import ast
import contextlib
import io
import math
import os
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

source = Path(__file__).resolve().parents[1] / 'verifications/module_5.py'
functions = [n for n in ast.parse(source.read_text()).body if isinstance(n, ast.FunctionDef)
             and n.name in ('has_line_loss_failsafe', 'tuning_and_kick')]
clock = SimpleNamespace(now=0.0)
namespace = {'math': math, 'os': os, 're': re, '__file__': str(source),
             'time': SimpleNamespace(time=lambda: clock.now),
             'cv2': SimpleNamespace(imread=lambda path: None)}
exec(compile(ast.Module(body=functions, type_ignores=[]), str(source), 'exec'), namespace)
verify = namespace['tuning_and_kick']
reference = (source.parents[1] / 'solutions/module_5/tuning_and_kick_reference.py').read_text()

class KickVerdictTests(unittest.TestCase):
    def run_case(self, messages, code=reference):
        clock.now = 0
        robot = SimpleNamespace(position=(40,18.5), position_px=None,
                                draw_info=lambda image: image, get_msg=lambda: None)
        _, state, _, _ = verify(robot, None, None, code)
        robot.position = (60,18.5)
        for index, message in enumerate(messages):
            clock.now = 5.2 * (index + 1)
            robot.get_msg = lambda: message
            _, state, _, _ = verify(robot, None, state, code)
        robot.get_msg = lambda: None
        clock.now = 29.5
        _, state, text, result = verify(robot, None, state, code)
        clock.now = 30.1
        _, _, later_text, later = verify(robot, None, state, code)
        self.assertEqual(later, result)
        self.assertEqual(later_text, text)
        return result

    def test_two_kicks_with_movement(self):
        self.assertTrue(self.run_case(['KICK!', 'KICK!'])['success'])

    def test_line_loss_after_two_kicks_fails(self):
        self.assertFalse(self.run_case(['KICK!', 'KICK!', 'Line lost! Emergency Stop.'])['success'])

    def test_debug_mentions_are_not_kicks(self):
        self.assertFalse(self.run_case(['no KICK!', 'no KICK!'])['success'])

    def test_missing_failsafe_fails(self):
        self.assertFalse(self.run_case(['KICK!', 'KICK!'], reference.replace('max(sensor_array) < 700', 'False'))['success'])

if __name__ == '__main__':
    unittest.main()
