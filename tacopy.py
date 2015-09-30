from Lexitize import Lexitize
from Treeitize import Treeitize
from Analyze import Analyze

from collections import deque


def printTree(tree, sc = 0):
    spaces = '    '
    while tree:
        if isinstance(tree, deque):
            x = tree.popleft()
        if x and x['type'] is 'parameters' and not tree:
            print spaces*sc + str(x)
            if isinstance(x['value'], deque):
                printTree(x['value'], sc+1)
            else:
                return
        else:
            print spaces*sc + str(x)


if __name__ == "__main__":
    lexitize = Lexitize()
    treeitize = Treeitize()
    analyze = Analyze()
    x = 'Hello'
    while x != 'quit':
        x = raw_input('>>> ')
        print x
        lex = lexitize.lexitize(x)
        print lex
        tree = treeitize.treeitize(lex)[0]
        print 'TREE: ' + str(tree)
        #printTree(deque(tree))
        output = analyze.analyze(tree)
        if output is not None:
            print output

