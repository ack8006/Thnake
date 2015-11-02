from ..thnake import *
import unittest

lexitize = Lexitize()
treeitize = Treeitize()
analyze = Analyze()

class TestComparison(unittest.TestCase):

    def test_string(self):
        x = "'test'"
        assert(execute_program(x, lexitize, treeitize, analyze) == 'test')

    def test_string2(self):
        x = '"test"'
        assert(execute_program(x, lexitize, treeitize, analyze) == 'test')

    def test_string_comparison(self):
        x = "'te3==3st'"
        assert(execute_program(x, lexitize, treeitize, analyze) == 'te3==3st')

    def test_string_conditional(self):
        x = '"teifst"'
        assert(execute_program(x, lexitize, treeitize, analyze) == 'teifst')

