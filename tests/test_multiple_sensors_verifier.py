import ast
import math
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

source = Path(__file__).resolve().parents[1] / 'verifications/module_4.py'
function = next(n for n in ast.parse(source.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'multiple_sensors')
clock = SimpleNamespace(now=0)
namespace = {'math':math,'re':re,'time':SimpleNamespace(time=lambda:clock.now),
             'cv2':SimpleNamespace(putText=lambda *args:None,FONT_HERSHEY_SIMPLEX=0)}
exec(compile(ast.Module(body=[function],type_ignores=[]),str(source),'exec'),namespace)
verify = namespace['multiple_sensors']
code = (source.parents[1]/'solutions/module_4/multiple_sensors.py').read_text()

class MultipleSensorsTests(unittest.TestCase):
    def replay(self, messages, stop=(100,55), drift=(100,55), program=code):
        clock.now=0
        robot=SimpleNamespace(position=(45,18.5),position_px=None,draw_info=lambda image:image,get_msg=lambda:None)
        _,state,_,_=verify(robot,None,None,program)
        for index,msg in enumerate(messages):
            clock.now=index+1
            robot.position=stop if 'Blue:' in msg else (70,18)
            robot.get_msg=lambda:msg
            _,state,_,_=verify(robot,None,state,program)
        robot.position=drift
        robot.get_msg=lambda:None
        clock.now=19.5
        _,state,text,result=verify(robot,None,state,program)
        clock.now=20.1
        _,_,later_text,later=verify(robot,None,state,program)
        self.assertEqual(result,later)
        self.assertEqual(text,later_text)
        return result

    def test_color_led_and_stationary_blue_pass(self):
        self.assertTrue(self.replay(['Green (Raw: R:30 G:90 B:20)','Green: led on','Blue: Mission complete.'])['success'])

    def test_measured_blue_entry_stop_21891_passes(self):
        self.assertTrue(self.replay(['Green (Raw: R:121 G:98 B:62)', 'Green: led on', 'Blue: Mission complete.'], stop=(105.41,34.925), drift=(105.41,34.925))['success'])

    def test_missing_led_fails(self):
        self.assertFalse(self.replay(['Green (Raw: R:30 G:90 B:20)','Blue: Mission complete.'])['success'])

    def test_stop_away_from_blue_fails(self):
        self.assertFalse(self.replay(['Green (Raw: R:30 G:90 B:20)','Green: led on','Blue: Mission complete.'],stop=(45,18),drift=(45,18))['success'])

    def test_moving_after_stop_message_fails(self):
        self.assertFalse(self.replay(['Green (Raw: R:30 G:90 B:20)','Green: led on','Blue: Mission complete.'],drift=(107,55))['success'])

    def test_empty_code_fails_even_with_events(self):
        self.assertFalse(self.replay(['Green (Raw: R:30 G:90 B:20)','Green: led on','Blue: Mission complete.'],program='pass')['success'])

if __name__=='__main__':unittest.main()
