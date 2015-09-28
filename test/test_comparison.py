from ..__init__ import *
import unittest

class TestComparison(unittest.TestCase):
    def test_equals(self):
        x = '3==3'
        assert(run_program(x) == True)

    def test_not_equals(self):
        x = '35<>12'
        assert(run_program(x) == True)

    def test_greater_than(self):
        x = '7>3'
        assert(run_program(x) == True)

    def test_less_than(self):
        x = '2<4'
        assert(run_program(x) == True)

    def test_greater_equals(self):
        x = '4>=3'
        assert(run_program(x) == True)

    def test_less_equals(self):
        x = '5<=7'
        assert(run_program(x) == True)

    def test_equals_fail(self):
        x = '3==4'
        assert(run_program(x) == False)

    def test_not_equals_fail(self):
        x = '35<>35'
        assert(run_program(x) == False)

    def test_greater_than_fail(self):
        x = '7>30'
        assert(run_program(x) == False)

    def test_less_than_fail(self):
        x = '20<4'
        assert(run_program(x) == False)

    def test_greater_equals_fail(self):
        x = '4>=13'
        assert(run_program(x) == False)

    def test_less_equals_fail(self):
        x = '15<=7'
        assert(run_program(x) == False)

    def test_arithmetic_cond1(self):
        x = '3+4==7'
        assert(run_program(x) == True)

    def test_arithmetic_cond2(self):
        x = '7==3+4'
        assert(run_program(x) == True)

    def test_arithmetic_cond3(self):
        x = '[1,2,3].get(0) == 1'
        assert(run_program(x) == True)




def main():
    unittest.main()

if __name__ == '__main__':
    main()
