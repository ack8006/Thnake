from ..__init__ import *
import unittest

class TestComparison(unittest.TestCase):

    def test_string(self):
        x = "'test'"
        assert(run_program(x) == 'test')

    def test_string2(self):
        x = '"test"'
        assert(run_program(x) == 'test')

    def test_string_comparison(self):
        x = "'te3==3st'"
        assert(run_program(x) == 'te3==3st')

    def test_string_conditional(self):
        x = '"teifst"'
        assert(run_program(x) == 'teifst')

def main():
    unittest.main()

if __name__ == '__main__':
    main()
