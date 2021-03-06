from Lexitize import Lexitize
from Treeitize import Treeitize
from Analyze import Analyze


def run_program(x):
    lexitize = Lexitize()
    treeitize = Treeitize()
    analyze = Analyze()

    lexOfLexes= lexitize.lexitize(x)
    for lex in lexOfLexes:
        tree = treeitize.treeitize(lex)[0]
        output = analyze.analyze(tree)
        if output is not None:
            return output
