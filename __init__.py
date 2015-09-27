from Lexitize import Lexitize
from Treeitize import Treeitize
from Analyze import Analyze
from collections import deque

def run_program(x):
    lexitize = Lexitize()
    treeitize = Treeitize()
    analyze = Analyze()
    lex = lexitize.lexitize(x)
    tree = treeitize.treeitize(lex)[0]
    output = analyze.analyze(tree)
    if output is not None:
        return output
