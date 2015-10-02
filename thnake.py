from Lexitize import Lexitize
from Treeitize import Treeitize
from Analyze import Analyze
import sys
import os.path



def execute_program(programInput, lexitize, treeitize, analyze):
    if programInput == 'quit':
        sys.exit(0)
    lexOfLexes = lexitize.lexitize(programInput)
    for lex in lexOfLexes:
        #print lex
        tree = treeitize.treeitize(lex)[0]
        #print tree
        #while tree:
        output = analyze.analyze(tree.popLeftObject())
        if output is not None:
            return output
            #print output


if __name__ == "__main__":
    lexitize = Lexitize()
    treeitize = Treeitize()
    analyze = Analyze()
    programInput = None

    if len(sys.argv) > 1:
        fileExtension = os.path.splitext(sys.argv[1])[1]
        if fileExtension == '.thnk':
            with open(sys.argv[1], 'r') as f:
                programInput = f.read()
                execute_program(programInput, lexitize, treeitize, analyze)

        elif fileExtension:
            'Please Input File of Type .thnk'
            sys.exit(0)

    else:
        while True:
            programInput = raw_input('>>> ')
            execute_program(programInput, lexitize, treeitize, analyze)


            #if x == 'quit':
            #    sys.exit(0)
            #print x
            #lex = lexitize.lexitize(x)
            #print lex
            #tree = treeitize.treeitize(lex)[0]
            #print 'TREE: ' + str(tree)
            #output = analyze.analyze(tree)
            #if output is not None:
            #    print output

