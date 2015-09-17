from operatorFunc import shuntingYardAlgo, treeitizeShunting
from definitions import *
from collections import deque



def lexization(inp):

    #***parses in out of a string of 'string'
    #***only add to arith and comparison and others that need it
    def spCharSpaces(inp):
        for char in specialCharacters:
            inp = inp.replace(char, ' '+char+' ')
        #special case
        inp = inp.replace('*  *', '**')
        inp = inp.replace('=  =', '==')
        inp = inp.replace('<  =', '<=')
        inp = inp.replace('>  =', '>=')
        return inp

    def cleanWhiteSpace(lex):
        lex = [x for x in lex if x != '']
        return lex

    inp = spCharSpaces(inp)
    lexPieces = inp.split(' ')
    lexPieces = cleanWhiteSpace(lexPieces)
    return deque(lexPieces)



def treeitize(lex, variables=[], currentBranch=deque([]), held=[]):

    def addToTree(tree, ty, val):
        tree.append({'type': ty, 'value': val})
        return tree

    tree = deque([])

    #****CurrentBranch currently not doing anything
    #*should matter when looping, not recursing? maybe?
    while len(lex) > 0:
        #print 'LEX: ' + str(lex)
        #print 'TREE: ' + str(tree)
        #print 'ANALYZE'
        #print currentBranch
        #print held
        #print tree
        curLex = lex.popleft()
        #print curLex
        #print
        if curLex.isdigit(): #and not currentBranch:
            lex.appendleft(curLex)
            lex, parTree = shuntingYardAlgo(lex, tree)
            tree += parTree
        # this is not right
        elif curLex in ['(',')'] and not currentBranch:
            lex.appendleft(curLex)
            lex, parTree = shuntingYardAlgo(lex, tree)
            tree += parTree

        #****check if in variables if variable, make object
        elif curLex not in specialCharacters:
            held.append(curLex)

        #***this is also catching all nones in spchar
        elif curLex in specialCharacters:
            spCh = specialCharacters[curLex]
            if spCh == 'variable':
                var = held.pop()
                variables.append(var)
                valTree = treeitize(lex)
                currentBranch.append(spCh)
                tree = addToTree(tree, spCh, var)
                tree = addToTree(tree, 'parameters', valTree)
            # STRINGS
            elif spCh == 'object':
                stringList = [curLex]
                curPop = None
                while curPop != curLex:
                    curPop = lex.popleft()
                    stringList.append(curPop)
                tree = addToTree(tree, spCh, ''.join(stringList))

            elif spCh == 'dataStructure':
                lastHeld = None
                if held:
                    lastHeld = held[-1]
                if ((lastHeld == '[' and curLex == ']') or
                        (lastHeld == '{' and curLex == '}')):
                    held.pop()
                    return tree, lex, held
                else:
                    currentBranch.append(spCh)
                    held.append(curLex)
                    tree = addToTree(tree, spCh, curLex)
                    parTree, lex, held = treeitize(lex, variables, currentBranch, held)
                    tree = addToTree(tree, 'parameters', parTree)



    if lex or held:
        return tree, lex, held
    else:
        return tree




def analyze(tree, objects = {}):

    #***also needs to handle objects
    def analyzeOperator(operator, parameters):
        if len(parameters['value']) == 2:
            vals = deque(parameters['value'])
            return eval('('+vals.popleft()+')'+operator['value']+'('+vals.popleft()+')')
        val1 = parameters['value'].pop(0)
        if isinstance(val1, dict):
            val1 = analyzeOperator(val1, parameters['value'].pop(0))
        val2 = parameters['value'].pop(0)
        if isinstance(val2, dict):
            val2 = analyzeOperator(val2, parameters['value'].pop(0))
        return eval('('+str(val1)+')' + operator['value'] + '('+str(val2)+')')

    def analyzeVariable(parameters, objects):
        return analyze(parameters['value'])

    def analyzeDataStructure(topValue, parameters, objects):
        if topValue == '[':
            newList = []
            values = parameters['value']
            while values:
                result = analyze(values, objects)
                newList.append(result)
            return newList



    #**********analyzing needs references to existing objects
    #**cannot just recreate analyze, need to at least pass objects
    result = None

    #while len(tree) > 0:

    top = tree.popleft()
    topType = top['type']
    topValue = top['value']

    #check if in objects and return actual val
    if topType == 'object':
        if topValue in objects:
            #return objects[topValue]
            result = objects[topValue]
        else:
            #return topValue
            result = topValue

    if topType == 'arithmetic':
        #popleft?
        parameters = tree.popleft()
        result = analyzeOperator(top, parameters)

    elif topType == 'variable':
        #popleft?
        parameters = tree.popleft()
        objects[topValue] = analyzeVariable(parameters, objects)
        print objects
        #return objects[topValue]
        result = objects[topValue]

    elif topType == 'dataStructure':
        parameters = tree.popleft()
        result = analyzeDataStructure(topValue, parameters, objects)

    return result



if __name__ == '__main__':
    x = '1, 2'
    x = '["a", "b"]'
    x = '[[1,2+3],3]'
    print x
    lexPieces = lexization(x)
    print lexPieces
    tree = treeitize(lexPieces)
    print tree
    result = analyze(tree)
    print result





