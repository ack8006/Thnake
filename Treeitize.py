from definitions import *
from operatorFunc import shuntingYardAlgo, treeitizeShunting
from Tree import Tree
from collections import deque


class Treeitize():
    def __init__(self):
        pass

    def treeitize(self, lex):
        tree = Tree()

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

            #***handle negative HERE
            if curLex.isdigit() or curLex == '-': #and not currentBranch:
                lex.appendleft(curLex)
                lex, parTree = shuntingYardAlgo(lex, tree)
                tree += parTree

            #*** currently parens indicate arithmetic
            elif curLex in ['(',')']: #and not currentBranch:
                lex.appendleft(curLex)
                lex, parTree = shuntingYardAlgo(lex, tree)
                tree += parTree

            elif curLex not in specialCharacters:
                tree.addToTree('variable', curLex)
                if (not lex or specialCharacters[lex[0]] <> 'variable'):
                    tree.addToTree('parameters', None)

            elif curLex in specialCharacters:
                spCh = specialCharacters[curLex]

                if spCh == 'linebreak':
                    return tree, lex

                elif spCh == 'NullValue':
                    tree.addToTree('object', None)
                    tree.addToTree('parameters', None)

                elif spCh == 'variable':
                    valTree, lex = self.treeitize(lex)
                    tree.addToTree('parameters', valTree)

                #gets here if variable then arithmetic sym

                #****Needed or loop?
                #if arithmetic on a variable
                elif (spCh == 'arithmetic'):
                    lex.appendleft(curLex)
                    var = tree.popLeftObject().popleft()['value']
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
                    tree.addToTree('object', spCh)
                    tree.addToTree('parameters', ''.join(stringList))

                elif spCh =='boolean':
                    tree.addToTree('object', spCh)
                    if curLex == 'True':
                        curLex = True
                    else: curLex = False
                    tree.addToTree('parameters', curLex)

                elif spCh == 'comparison':
                    values = tree.popRightObject()

                    tree.addToTree(spCh, curLex)
                    parTree, lex = self.treeitize(lex)

                    values += parTree

                    tree.addToTree('parameters', values)

                    #NEW
                    return tree, lex

                elif spCh == 'list':
                    if curLex == '[':
                        tree.addToTree('object', spCh)
                        values = Tree()
                        while lex:
                            if lex[0] == ']':
                                curLex = lex.popleft()
                                break
                            varTree, lex = self.treeitize(lex)
                            values += varTree
                        tree.addToTree('parameters', values)
                    elif curLex == ']':
                        lex.appendleft(curLex)
                        return tree, lex

                elif spCh == 'conditional':
                    def getStructureTree():
                        strucLex = deque([lex.popleft()])
                        structureCount = 1
                        while structureCount >0:
                            current = lex.popleft()
                            strucLex.append(current)
                            if current == '{':
                                structureCount += 1
                            elif current == '}':
                                structureCount -= 1
                        strucTree = Tree([])
                        while strucLex:
                            retTree, strucLex = self.treeitize(strucLex)
                            strucTree += retTree
                        return strucTree

                    tree.addToTree('conditional', curLex)
                    conTree, lex = self.treeitize(lex)

                    ifTree = getStructureTree()
                    elseTree = None
                    if lex and lex.popleft() == '{':
                        elseTree = getStructureTree()

                    print 'TREES'
                    print ifTree
                    print elseTree
                    conTree.append(Tree([ifTree, elseTree]))
                    tree.addToTree('parameters', conTree)

                elif spCh == 'loop':
                    tree.addToTree(spCh, curLex)

                    loopParam, lex = self.treeitize(lex)
                    #listTree, lex = self.treeitize(lex)
                    loopActionTree = Tree([])
                    while lex:
                        actionTree, lex = self.treeitize(lex)
                        loopActionTree += actionTree

                    #***TREE FUNCT to consolidate multiple trees
                    values = Tree()
                    for x in [loopParam, loopActionTree]:
                        values += x
                    tree.addToTree('parameters', values)

                elif spCh == 'structure':
                    return tree, lex

                elif spCh == 'dot':
                    attribFunc = lex.popleft()
                    listObject = tree.popRightObject()
                    tree.addToTree('attribFunc', attribFunc)

                    parenCount = 1
                    attribLex = Tree([lex.popleft()])
                    while parenCount != 0:
                       curAtLex = lex.popleft()
                       attribLex += curAtLex
                       if curAtLex == '(':parenCount +=1
                       elif curAtLex == ')': parenCount -= 1

                    attribVal, attribLex = self.treeitize(attribLex)
                    tree.addToTree('parameters', Tree([attribVal, listObject]))


        return tree, lex




