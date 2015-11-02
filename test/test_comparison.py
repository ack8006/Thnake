from ..thnake import *
import unittest

lexitize = Lexitize()
treeitize = Treeitize()
analyze = Analyze()

class TestComparison(unittest.TestCase):
    def test_equals(self):
        x = '3==3'
        assert(execute_program(x, lexitize, treeitize, analyze) == True)

    def test_not_equals(self):
        x = '35<>12'
        assert(execute_program(x, lexitize, treeitize, analyze) == True)

    def test_greater_than(self):
        x = '7>3'
        assert(execute_program(x, lexitize, treeitize, analyze) == True)

    def test_less_than(self):
        x = '2<4'
        assert(execute_program(x, lexitize, treeitize, analyze) == True)

    def test_greater_equals(self):
        x = '4>=3'
        assert(execute_program(x, lexitize, treeitize, analyze) == True)

    def test_less_equals(self):
        x = '5<=7'
        assert(execute_program(x, lexitize, treeitize, analyze) == True)

    def test_equals_fail(self):
        x = '3==4'
        assert(execute_program(x, lexitize, treeitize, analyze) == False)

    def test_not_equals_fail(self):
        x = '35<>35'
        assert(execute_program(x, lexitize, treeitize, analyze) == False)

    def test_greater_than_fail(self):
        x = '7>30'
        assert(execute_program(x, lexitize, treeitize, analyze) == False)

    def test_less_than_fail(self):
        x = '20<4'
        assert(execute_program(x, lexitize, treeitize, analyze) == False)

    def test_greater_equals_fail(self):
        x = '4>=13'
        assert(execute_program(x, lexitize, treeitize, analyze) == False)

    def test_less_equals_fail(self):
        x = '15<=7'
        assert(execute_program(x, lexitize, treeitize, analyze) == False)

    def test_arithmetic_cond1(self):
        x = '3+4==7'
        assert(execute_program(x, lexitize, treeitize, analyze) == True)

    def test_arithmetic_cond2(self):
        x = '7==3+4'
        assert(execute_program(x, lexitize, treeitize, analyze) == True)

    def test_array_access(self):
        x = '[1,2,3].get(0) == 1'
        assert(execute_program(x, lexitize, treeitize, analyze) == True)

    def test_array_access2(self):
        x = '[[1],2,3].get(0) == [1]'
        assert(execute_program(x, lexitize, treeitize, analyze) == True)

    def test_list(self):
        x = '[1,2,3]==[1,2,3]'
        assert(execute_program(x, lexitize, treeitize, analyze) == True)

    def test_list_fail(self):
        x = '[1,2,3]==[1,4,3]'
        assert(execute_program(x, lexitize, treeitize, analyze) == False)

    def test_string(self):
        x = '"test"=="test"'
        assert(execute_program(x, lexitize, treeitize, analyze) == True)

    def test_string_fail(self):
        x = '"test"=="tasest"'
        assert(execute_program(x, lexitize, treeitize, analyze) == False)
