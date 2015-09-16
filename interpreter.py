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

    #calc
    def shuntingYardAlgo(lex, tree):
        outputStack = []
        operatorStack = []
        precedence = {'**': [4, 'R'],
                      '*': [3, 'L'],
                      '/': [3, 'L'],
                      '%': [3, 'L'],
                      '+': [2, 'L'],
                      '-': [2, 'L'],
                      '(': [6, 'L'],
                      ')': [0, 'L']
                      }
        shunt = True
        while shunt and len(lex) >0:
            token = lex[0]
            if token.isdigit():
                outputStack.append(token)
                lex.pop(0)
            elif token in precedence:
                lex.pop(0)

                if token is '(':
                    operatorStack.append(token)
                elif token is ')':
                    while len(operatorStack)>0:
                        poppedOp = operatorStack.pop()
                        if poppedOp == '(':
                            break
                        outputStack.append(poppedOp)
                elif operatorStack and ((precedence[token][0]<=precedence[operatorStack[-1]][0]
                                and precedence[token][1] == 'L')
                            or (precedence[token][1] == 'R'
                                and precedence[token][0] < precedence[operatorStack[-1]][0])):
                    if operatorStack[-1] is not '(':
                        outputStack.append(operatorStack.pop())
                    operatorStack.append(token)
                else:
                    operatorStack.append(token)
            else:
                shunt = False

        while operatorStack:
            outputStack.append(operatorStack.pop())
        tree = treeitizeShunting(outputStack)[0]
        return lex, tree

    def treeitizeShunting(outputStack):
        tree = []
        operator = outputStack.pop()
        if outputStack[-2:] == [x for x in outputStack[-2:] if x.isdigit()]:
            tree = addToTree(tree, specialCharacters[operator], operator)
            par2 = outputStack.pop()
            par1 = outputStack.pop()
            tree = addToTree(tree, 'parameters', [par1, par2])
            return tree, outputStack
        params = []
        if outputStack[-1].isdigit():
            params.append(outputStack.pop())
        else:
            pars, outputStack = treeitizeShunting(outputStack)
            for x in pars:
                params.append(x)
        if outputStack[-1].isdigit():
            params.insert(0, outputStack.pop())
        else:
            pars, outputStack = treeitizeShunting(outputStack)
            for x in reversed(pars):
                params.insert(0,x)
        tree = addToTree(tree, specialCharacters[operator], operator)
        tree = addToTree(tree, 'parameters', params)
        return tree, outputStack




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
            return eval(vals.pop(0)+operator['value']+vals.pop(0))
        val1 = parameters['value'].pop(0)
        if isinstance(val1, dict):
            val1 = analyzeOperator(val1, parameters['value'].pop(0))
        val2 = parameters['value'].pop(0)
        if isinstance(val2, dict):
            val2 = analyzeOperator(val2, parameters['value'].pop(0))
        return eval(str(val1) + operator['value'] + str(val2))


    result = None
    while len(tree) > 0:
        top = tree.pop(0)

        if top['type'] == 'operator':
            parameters = tree.pop()
            result = analyzeOperator(top, parameters)

    return result



if __name__ == '__main__':
    x = '3+4*2/(1-5)** 2 **3'
    lexPieces = lexization(x)
    tree = treeitize(lexPieces)
    result = analyze(tree)
    print result





