from collections import deque
from definitions import *


#***precedence should be global:w

def addToTree(tree, ty, val):
    tree.append({'type': ty, 'value': val})
    return tree

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
            lex.popleft()
        elif token in precedence:
            lex.popleft()

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
        elif token in specialCharacters:
            shunt = False
        else:
            outputStack.append(token)
            lex.popleft()

    while operatorStack:
        outputStack.append(operatorStack.pop())
    tree = treeitizeShunting(outputStack, precedence)[0]
    return lex, tree


def treeitizeShunting(outputStack, precedence):
    tree = deque([])
    if len(outputStack) == 1:
        #tree = addToTree(tree, 'object', int(outputStack[0]))
        tree = addToTree(tree, 'object', 'number')
        tree = addToTree(tree, 'parameters', int(outputStack[0]))
        return tree, outputStack
    operator = outputStack.pop()
    #BaseCase
    if outputStack[-2:] == [x for x in outputStack[-2:] if x.isdigit()]:
        tree = addToTree(tree, specialCharacters[operator], operator)
        par2 = outputStack.pop()
        par1 = outputStack.pop()
        tree = addToTree(tree, 'parameters', [par1, par2])
        return tree, outputStack
    params = []
    if (outputStack[-1].isdigit() or outputStack[-1] not in precedence):
        params.append(outputStack.pop())
    else:
        pars, outputStack = treeitizeShunting(outputStack, precedence)
        for x in pars:
            params.append(x)
    if (outputStack[-1].isdigit() or outputStack[-1] not in precedence):
        params.insert(0, outputStack.pop())
    else:
        pars, outputStack = treeitizeShunting(outputStack, precedence)
        for x in reversed(pars):
            params.insert(0,x)
    tree = addToTree(tree, specialCharacters[operator], operator)
    tree = addToTree(tree, 'parameters', params)
    return tree, outputStack



