from Lexitize import Lexitize
from Treeitize import Treeitize
from Analyze import Analyze
import sys



if __name__ == "__main__":
    lexitize = Lexitize()
    treeitize = Treeitize()
    analyze = Analyze()
    x = 'Hello'
    while x != 'quit':
        x = raw_input('>>> ')
        if x == 'quit':
            sys.exit(0)
        print x
        lex = lexitize.lexitize(x)
        print lex
        tree = treeitize.treeitize(lex)[0]
        print 'TREE: ' + str(tree)
        output = analyze.analyze(tree)
        if output is not None:
            print output

