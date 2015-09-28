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
            #***ONLY IN SPECIFIC CASES
            #lex.appendleft(token)


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
    if outputStack[-1].isdigit():
        tree = addToTree(tree, 'object', 'number')
        tree = addToTree(tree, 'parameters', int(outputStack.pop()))
        return tree, outputStack
    elif outputStack[-1] not in precedence:
        tree = addToTree(tree, 'variable', outputStack.pop())
        return tree, outputStack
    else:
        tree = addToTree(tree, 'arithmetic', outputStack.pop())
        val2, outputStack = treeitizeShunting(outputStack, precedence)
        val1, outputStack = treeitizeShunting(outputStack, precedence)
        values = deque([])
        for x in [val1, val2]:
            while x:
                values.append(x.popleft())
        tree = addToTree(tree, 'parameters', values)
    return tree, outputStack

