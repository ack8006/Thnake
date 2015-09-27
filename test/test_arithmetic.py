from ..__init__ import *
import unittest

class TestArithmetic(unittest.TestCase):
    def test_addition(self):
        x = '3+4'
        assert(run_program(x) == 7)

    def test_subtraction(self):
        x = '6-2'
        assert(run_program(x) == 4)

    def test_mult(self):
        x = '5*4'
        assert(run_program(x) == 20)

    def test_divide(self):
        x = '15/2'
        assert(run_program(x) == 7)

    def test_exp(self):
        x = '3**3'
        assert(run_program(x) == 27)

    def test_orderOps(self):
        x = '3+4*6-(15-2)**2'
        assert(run_program(x) == -142)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
