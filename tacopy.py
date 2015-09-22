from Lexitize import Lexitize
from Treeitize import Treeitize
from Analyze import Analyze

from collections import deque



if __name__ == "__main__":
    lexitize = Lexitize()
    treeitize = Treeitize()
    analyze = Analyze()
    x = 'Hello'
    while x != 'quit':
        x = raw_input('>>> ')
        lex = lexitize.lexitize(x)
        print lex
        tree = treeitize.treeitize(lex)
        print tree
        output = analyze.analyze(tree)
        if output is not None:
            print output
