from definitions import *
from operatorFunc import shuntingYardAlgo, treeitizeShunting
from Tree import Tree


class Treeitize():
    def __init__(self):
        pass

    def treeitize(self, lex): #held=[]):
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
                tree.addToTree('variable', curLex)

            elif curLex in specialCharacters:
                spCh = specialCharacters[curLex]
                if spCh == 'variable':
                    valTree, lex = self.treeitize(lex)
                    tree.addToTree('parameters', valTree)

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
                    tree.addToTree('conditional', curLex)
                    conTree, lex = self.treeitize(lex)
                    ifTree, lex = self.treeitize(lex)
                    elseTree, lex = self.treeitize(lex)

                    values = Tree()
                    for x in [conTree, ifTree, elseTree]:
                        values += x
                    tree.addToTree('parameters', values)

                elif spCh == 'structure':
                    if curLex == '{':
                        return tree, lex
                    elif curLex == '}':
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

                elif spCh == 'loop':
                    tree.addToTree(spCh, 'for')
                    listTree, lex = self.treeitize(lex)
                    actionTree, lex = self.treeitize(lex)

                    #***TREE FUNCT to consolidate multiple trees
                    values = Tree()
                    for x in [listTree, actionTree]:
                        values += x
                    tree.addToTree('parameters', values)

        return tree, lex
