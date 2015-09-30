from collections import deque
from definitions import *
from operatorFunc import shuntingYardAlgo, treeitizeShunting

#def addToTree(tree, ty, val):
#    tree.append({'type': ty, 'value': val})
#    return tree

class Treeitize():
    def __init__(self):
        pass

    def treeitize(self, lex): #held=[]):

        def addToTree(tree, ty, val):
            tree.append({'type': ty, 'value': val})
            return tree

        tree = deque([])

        while len(lex) > 0:

            curLex = lex.popleft()
            #print
            #print 'LEX: ' + str(lex)
            #print 'TREE: ' + str(tree)
            #print 'CURLEX: ' + str(curLex)
            #print

            #Really for List Management, only time with commas
            if curLex == ',':
                return tree, lex

            #handle negative HERE
            if curLex.isdigit() or curLex == '-': #and not currentBranch:
                lex.appendleft(curLex)
                lex, parTree = shuntingYardAlgo(lex, tree)
                tree += parTree

            # this is not right
            elif curLex in ['(',')']: #and not currentBranch:
                lex.appendleft(curLex)
                lex, parTree = shuntingYardAlgo(lex, tree)
                tree += parTree

            elif curLex not in specialCharacters:
                tree = addToTree(tree, 'variable', curLex)

            elif curLex in specialCharacters:
                spCh = specialCharacters[curLex]
                if spCh == 'variable':
                    valTree, lex = self.treeitize(lex)
                    tree = addToTree(tree, 'parameters', valTree)

                #gets here if variable then arithmetic sym

                #****Needed or loop?
                elif (spCh == 'arithmetic'):
                    lex.appendleft(curLex)
                    var = tree.pop()['value']
                    lex.appendleft(var)
                    lex, parTree = shuntingYardAlgo(lex, tree)
                    tree += parTree

                # STRINGS
                elif spCh == 'string':
                    stringList = []
                    curPop = lex.popleft()
                    while curPop != curLex:
                        #bootleg fix, if there are many spaces, it only adds one
                        if stringList:
                            stringList.append(' ')
                        stringList.append(curPop)
                        curPop = lex.popleft()
                    tree = addToTree(tree, 'object', spCh)
                    tree = addToTree(tree, 'parameters', ''.join(stringList))

                elif spCh =='boolean':
                    tree = addToTree(tree, 'object', spCh)
                    if curLex == 'True':
                        curLex = True
                    else: curLex = False
                    tree = addToTree(tree, 'parameters', curLex)

                elif spCh == 'comparison':
                    values = deque([])
                    popped = tree.pop()
                    #this grabs the first full element which will be either
                    #a variable or an object
                    while popped['type'] not in ['variable','object', 'arithmetic']:
                        values.appendleft(popped)
                        popped = tree.pop()
                    values.appendleft(popped)

                    tree = addToTree(tree, spCh, curLex)
                    parTree, lex = self.treeitize(lex)


                    while parTree:
                        values.append(parTree.popleft())
                    tree = addToTree(tree, 'parameters', values)


                elif spCh == 'list':
                    if curLex == '[':
                        tree = addToTree(tree, 'object', spCh)
                        values = deque([])
                        while lex:
                            if lex[0] == ']':
                                curLex = lex.popleft()
                                break
                            varTree, lex = self.treeitize(lex)
                            values += varTree
                        tree = addToTree(tree, 'parameters', values)
                    elif curLex == ']':
                        lex.appendleft(curLex)
                        return tree, lex

                elif spCh == 'conditional':
                    tree = addToTree(tree, 'conditional', curLex)
                    conTree, lex = self.treeitize(lex)
                    ifTree, lex = self.treeitize(lex)
                    elseTree, lex = self.treeitize(lex)

                    values = deque([])
                    for x in [conTree, ifTree, elseTree]:
                        while x:
                            values.append(x.popleft())
                    tree = addToTree(tree, 'parameters', values)

                elif spCh == 'structure':
                    if curLex == '{':
                        return tree, lex
                    elif curLex == '}':
                        return tree, lex

                elif spCh == 'dot':
                    attribFunc = lex.popleft()

                    parenCount = 1
                    attribLex = deque([lex.popleft()])
                    while parenCount != 0:
                       curAtLex = lex.popleft()
                       attribLex += curAtLex
                       if curAtLex == '(':parenCount +=1
                       elif curAtLex == ')': parenCount -= 1

                    attribVal, attribLex = self.treeitize(attribLex)

                    tree = addToTree(tree, 'attribFunc', attribFunc)
                    tree = addToTree(tree, 'parameters', attribVal)

                elif spCh == 'loop':
                    tree = addToTree(tree, spCh, 'for')
                    listTree, lex = self.treeitize(lex)
                    actionTree, lex = self.treeitize(lex)

                    #***TREE FUNCT to consolidate multiple trees
                    values = deque([])
                    for x in [listTree, actionTree]:
                        while x:
                            values.append(x.popleft())
                    tree = addToTree(tree, 'parameters', values)


        return tree, lex
