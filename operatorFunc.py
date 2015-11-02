from definitions import *
from Tree import Tree
from collections import deque
import Treeitize

#***precedence should be global:w

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
    while len(lex) >0:
        token = lex[0]
        if token is object:
            outputStack.append(tree.popRightObject())
            lex.popleft()
        elif token.isdigit():
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
            #Special Case, can refactor
            if token == '[':
                list_obj, lex = parse_out_list_access_object(lex)
                t = Treeitize.Treeitize()
                obj_tree, _ = t.treeitize(list_obj)
                outputStack.append(obj_tree.popLeftObject())

            else:
                break
        else:
            outputStack.append(token)
            lex.popleft()

    while operatorStack:
        outputStack.append(operatorStack.pop())
    tree = treeitizeShunting(outputStack, precedence)[0]
    return lex, tree


def treeitizeShunting(outputStack, precedence):
    tree = Tree()
    if type(outputStack[-1]) == Tree:
        tree += outputStack.pop()
        return tree, outputStack
    if outputStack[-1].isdigit():
        tree.addToTree('object', 'number')
        tree.addToTree('parameters', int(outputStack.pop()))
        return tree, outputStack
    elif outputStack[-1] not in precedence:
        tree.addToTree('variable', outputStack.pop())
        tree.addToTree('parameters', None)
        return tree, outputStack
    else:
        tree.addToTree('arithmetic', outputStack.pop())
        val2, outputStack = treeitizeShunting(outputStack, precedence)
        val1, outputStack = treeitizeShunting(outputStack, precedence)
        values = Tree([])
        for x in [val1, val2]:
            while x:
                values.append(x.popleft())
        tree.addToTree('parameters', values)
    return tree, outputStack

def parse_out_list_access_object(lex):
    list_obj = deque()
    current = None
    while current <> 'get':
        current = lex.popleft()
        list_obj.append(current)
    list_obj.append(lex.popleft())
    paren_count = 1
    while paren_count:
        current = lex.popleft()
        list_obj.append(current)
        if current == '(': paren_count += 1
        elif current == ')': paren_count -= 1
    return list_obj, lex

