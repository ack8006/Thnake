from ..__init__ import *
import unittest

class TestComparison(unittest.TestCase):
    def test_if(self):
        x = 'if 1==1 {5}'
        assert(run_program(x) == 5)

    def test_if_fail(self):
        x = 'if 1==2 {5}'
        assert(run_program(x) == None)

    def test_if_else_pass(self):
        x = 'if 5==5 {"pass"}{False}'
        assert(run_program(x) == 'pass')

    def test_if_else_false(self):
        x = 'if 5==4 {True}{False}'
        assert(run_program(x) == False)

    def test_if_else_types(self):
        x = 'if 5==5 {4+5*3}{3==3}'
        assert(run_program(x) == 19)

    def test_if_else_pass(self):
        x = 'if 5==4 {4+5*3}{3==3}'
        assert(run_program(x) == True)

    def test_if_else_nested(self):
        x = 'if 5==4 {False}{if 1==1 {True}}'
        assert(run_program(x) == True)



def main():
    unittest.main()

if __name__ == '__main__':
    main()
