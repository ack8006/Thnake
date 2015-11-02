from ..thnake import *
import unittest
import sys
from StringIO import StringIO

lexitize = Lexitize()
treeitize = Treeitize()
analyze = Analyze()

class TestComparison(unittest.TestCase):
    def test_if(self):
        x = 'if 1==1 {5}'
        output = run_and_get_stdout(x)
        assert(output == str(5))

    def test_if_fail(self):
        x = 'if 1==2 {5}'
        assert(execute_program(x, lexitize, treeitize, analyze) == None)

    def test_if_else_pass(self):
        x = 'if 5==5 {"pass"}{False}'
        output = run_and_get_stdout(x)
        assert(output == 'pass')

    def test_if_else_false(self):
        x = 'if 5==4 {True}{False}'
        output = run_and_get_stdout(x)
        assert(output == str(False))

    def test_if_else_types(self):
        x = 'if 5==5 {4+5*3}{3==3}'
        output = run_and_get_stdout(x)
        assert(output == str(19))

    def test_if_else_pass_conditional(self):
        x = 'if 5==4 {4+5*3}{3==3}'
        output = run_and_get_stdout(x)
        assert(output == str(True))

    def test_if_else_nested(self):
        x = 'if 5==4 {False}{if 1==1 {True}}'
        output = run_and_get_stdout(x)
        assert(output == str(True))


def run_and_get_stdout(x):
    out = StringIO()
    sys.stdout = out
    execute_program(x, lexitize, treeitize, analyze)
    output = out.getvalue().strip()
    return output
