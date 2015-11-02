from ..thnake import *
import unittest

lexitize = Lexitize()
treeitize = Treeitize()
analyze = Analyze()

class TestArithmetic(unittest.TestCase):
    def test_empty(self):
        x = '[]'
        assert(execute_program(x, lexitize, treeitize, analyze) == [])

    def test_integers(self):
        x = '[1,2,3,4,5]'
        assert(execute_program(x, lexitize, treeitize, analyze) == [1,2,3,4,5])

    def test_arithmetic(self):
        x = '[3+5,17-3*2, 8]'
        assert(execute_program(x, lexitize, treeitize, analyze) == [8, 11, 8])

    def test_strings(self):
        x = '["test", "test2"]'
        assert(execute_program(x, lexitize, treeitize, analyze) == ['test', 'test2'])

    def test_comparison(self):
        x = '[1==2, 2<>3, 5>3]'
        assert(execute_program(x, lexitize, treeitize, analyze) == [False, True, True])

    def test_lists(self):
        x = '[[1,[2,3]],6, [3]]'
        assert(execute_program(x, lexitize, treeitize, analyze) == [[1, [2, 3]],6,[3]])

    def test_heavy_nested(self):
        x = '[[[[[[[[8]]]]]]]]'
        assert(execute_program(x, lexitize, treeitize, analyze) == [[[[[[[[8]]]]]]]])

    def test_all(self):
        x = '[[1],[1+1],[[12+13].get(0), ["test"]],[4==4],[1]]'
        #x = '[[[5].get(0),["test"]], [4]]'
        assert(execute_program(x, lexitize, treeitize, analyze) == [[1], [2], [25, ['test']], [True], [1]])

    def test_func_access(self):
        x = '[1,2,3].get(1)'
        assert(execute_program(x, lexitize, treeitize, analyze) == 2)

    def test_func_internal(self):
        x = '[[1,2,3].get(1)]'
        assert(execute_program(x, lexitize, treeitize, analyze) == [2])

    def test_func_mult(self):
        x = '[[1,2,3].get(1), 80]'
        assert(execute_program(x, lexitize, treeitize, analyze) == [2, 80])

