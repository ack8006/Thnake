from collections import deque
from definitions import *
from operatorFunc import shuntingYardAlgo, treeitizeShunting

#def addToTree(tree, ty, val):
#    tree.append({'type': ty, 'value': val})
#    return tree

class Treeitize():
    def __init__(self):
        pass

    def treeitize(self, lex, held=[]):

        def addToTree(tree, ty, val):
            tree.append({'type': ty, 'value': val})
            return tree

        tree = deque([])

        #*** Do I need Loop?
        while len(lex) > 0:

            curLex = lex.popleft()
            #print
            #print 'LEX: ' + str(lex)
            #print 'TREE: ' + str(tree)
            #print 'HELD: ' + str(held)
            #print 'CURLEX: ' + str(curLex)
            #print

            #SPECIAL/BASE CASES
            #**** should also handle if

            if (held and held[-1] == 'comparison' and curLex in [',',']']):
                lex.appendleft(curLex)
                return tree, lex, held

            if (held and held[-1] == 'attribFunc' and curLex in
                [x for x,y in specialCharacters.iteritems() if y in ['comparison', 'comma']]):

                lex.appendleft(curLex)
                return tree, lex, held


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
                #held.append(curLex)
                #tree = addToTree(tree, 'variable', curLex)

            elif curLex in specialCharacters:
                spCh = specialCharacters[curLex]
                if spCh == 'variable':
                    valTree, lex, held = self.treeitize(lex, held)
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

                    held.append('comparison')
                    parTree, lex, held = self.treeitize(lex, held)

                    held.pop()


                    while parTree:
                        values.append(parTree.popleft())
                    #if (held and held[-1] == 'comparison'):
                    #    held.pop()
                    tree = addToTree(tree, 'parameters', values)

                elif spCh == 'list':
                    if (held and (held[-1] == '[' and curLex == ']')):
                        held.pop()
                        return tree, lex, held
                    elif curLex == '[':
                        held.append(curLex)
                        tree = addToTree(tree, 'object', spCh)
                        parTree, lex, held = self.treeitize(lex, held)
                        tree = addToTree(tree, 'parameters', parTree)
                        #if not lex:
                        #    return tree,lex,held

                elif spCh == 'conditional':
                    held.append(curLex)
                    tree = addToTree(tree, 'conditional', curLex)
                    conTree, lex, held = self.treeitize(lex, held)
                    ifTree, lex, held = self.treeitize(lex, held)
                    elseTree, lex, held = self.treeitize(lex, held)

                    values = deque([])
                    for x in [conTree, ifTree, elseTree]:
                        while x:
                            values.append(x.popleft())
                    tree = addToTree(tree, 'parameters', values)

                elif spCh == 'structure':
                    if curLex == '{':
                        #if (held and held[-1] =='comparison'):
                        #    held.pop()
                        held.append(curLex)
                        return tree, lex, held
                    elif curLex == '}':
                        held.pop()
                        return tree, lex, held

                elif spCh == 'dot':
                    held.append('attribFunc')
                    attribFunc = lex.popleft()
                    attribVal, lex, held = self.treeitize(lex, held)
                    held.pop()

                    tree = addToTree(tree, 'attribFunc', attribFunc)
                    tree = addToTree(tree, 'parameters', attribVal)

                elif spCh == 'loop':
                    held.append('loop')
                    tree = addToTree(tree, spCh, 'for')
                    listTree, lex, held = self.treeitize(lex, held)
                    actionTree, lex, held = self.treeitize(lex, held)

                    #***TREE FUNCT to consolidate multiple trees
                    values = deque([])
                    for x in [listTree, actionTree]:
                        while x:
                            values.append(x.popleft())
                    tree = addToTree(tree, 'parameters', values)


                #elif spCh == 'loopParam' and held[-1] == 'loop':
                #    pass




                #elif spCh == 'linebreak':
                #    if held:
                #        return tree, lex, held
                #    if lex:
                #        parTree,lex,held = self.treeitize(lex)
                #    while parTree:
                #        tree.append(parTree.popleft())
                #    return tree, lex, held


        #if (held and not tree and held[-1] not in specialCharacters and not lex):
        #    tree = addToTree(tree, 'variable', held.pop())

        return tree, lex, held
