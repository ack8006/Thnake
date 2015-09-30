from ..__init__ import *
import unittest

class TestComparison(unittest.TestCase):

    def test_arith_loop(self):
        x = 'for x in [1] {x}'
        assert(run_program(x) == '1')

    def test_equals(self):
        x = '3==3'
        assert(run_program(x) == True)

    def test_equals(self):
        x = '3==3'
        assert(run_program(x) == True)

    def test_equals(self):
        x = '3==3'
        assert(run_program(x) == True)




def main():
    unittest.main()

if __name__ == '__main__':
    main()
