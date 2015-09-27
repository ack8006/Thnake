from ..__init__ import *
import unittest

class TestComparison(unittest.TestCase):
    def test_if(self):
        x = 'if 1==1 {5}'
        assert(run_program(x) == 5)

    def test_if_fail(self):
        x = 'if 1==2 {5}'
        assert(run_program(x) == None)



def main():
    unittest.main()

if __name__ == '__main__':
    main()
