from operatorFunc import shuntingYardAlgo, treeitizeShunting


specialCharacters = {'(': None,
                     ')': None,
                     '+': 'operator',
                     '-': 'operator',
                     '*': 'operator',
                     '/': 'operator',
                     '%': 'operator',
                     '**': 'operator',
                     '[': None,
                     ']': None,
                     ',': None,
                     '{': None,
                     '}': None,
                     '.': None,
                     }
paramDefs = {'operator': 2,
             }

def lexization(inp):
    def spCharSpaces(inp):
        for char in specialCharacters:
            inp = inp.replace(char, ' '+char+' ')
        #special case
        inp = inp.replace(' *  * ', '**')
        return inp
    def cleanWhiteSpace(lex):
        lex = [x for x in lex if x != '']
        return lex

    inp = spCharSpaces(inp)
    lexPieces = inp.split(' ')
    lexPieces = cleanWhiteSpace(lexPieces)
    return lexPieces


def treeitize(lex):
    def addToTree(tree, ty, val):
        tree.append({'type': ty, 'value': val})
        return tree

    tree = []
    currentBranch = None
    currentIndex = 0
    #variables = {}

    #for token in lex:
    while len(lex) > 0:
        if lex[currentIndex].isdigit() and not currentBranch:
            lex, tree = shuntingYardAlgo(lex, tree)
        elif lex[currentIndex] in ['(',')'] and not currentBranch:
            lex, tree = shuntingYardAlgo(lex, tree)

        #elif token in specialCharacters:
        #    definition = specialCharacters[token]
        #    if definition == 'operator':
        #        tree = addToTree(tree, definition, token)
        #        currentBranch = definition


    return tree


def analyze(tree):
    def analyzeOperator(operator, parameters):
        if len(parameters['value']) == 2:
            vals = parameters['value']
            return eval('('+vals.pop(0)+')'+operator['value']+'('+vals.pop(0)+')')
        val1 = parameters['value'].pop(0)
        if isinstance(val1, dict):
            val1 = analyzeOperator(val1, parameters['value'].pop(0))
        val2 = parameters['value'].pop(0)
        if isinstance(val2, dict):
            val2 = analyzeOperator(val2, parameters['value'].pop(0))
        return eval('('+str(val1)+')' + operator['value'] + '('+str(val2)+')')


    result = None
    while len(tree) > 0:
        top = tree.pop(0)

        if top['type'] == 'operator':
            parameters = tree.pop()
            result = analyzeOperator(top, parameters)

    return result



if __name__ == '__main__':
    x = '3+4*2/(1-5)**2**3'
    lexPieces = lexization(x)
    tree = treeitize(lexPieces)
    result = analyze(tree)
    print result





