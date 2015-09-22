from collections import deque
from definitions import *
from operatorFunc import shuntingYardAlgo, treeitizeShunting

class Treeitize():
    def __init__(self):
        pass

    def treeitize(self, lex, variables=[], currentBranch=deque([]), held=[]):

        def addToTree(tree, ty, val):
            tree.append({'type': ty, 'value': val})
            return tree

        tree = deque([])

        #****CurrentBranch currently not doing anything
        #*should matter when looping, not recursing? maybe?
        while len(lex) > 0:

            curLex = lex.popleft()
            #print
            #print 'LEX: ' + str(lex)
            #print 'TREE: ' + str(tree)
            #print 'ANALYZE'
            #print currentBranch
            #print held
            #print curLex
            #print

            if (held and held[-1] == 'comparison' and curLex in [',',']']):
                lex.append(curLex)
                return tree, lex, held

            #handle negative HERE
            if curLex.isdigit() or curLex == '-': #and not currentBranch:
                lex.appendleft(curLex)
                lex, parTree = shuntingYardAlgo(lex, tree)
                tree += parTree

            # this is not right
            elif curLex in ['(',')'] and not currentBranch:
                lex.appendleft(curLex)
                lex, parTree = shuntingYardAlgo(lex, tree)
                tree += parTree

            elif curLex not in specialCharacters:
                held.append(curLex)
                #tree = addToTree(tree, 'variable', curLex)

            elif curLex in specialCharacters:
                spCh = specialCharacters[curLex]
                if spCh == 'variable':
                    var = held.pop()
                    valTree, lex, held = self.treeitize(lex)
                    #currentBranch.append(spCh)
                    tree = addToTree(tree, spCh, var)
                    tree = addToTree(tree, 'parameters', valTree)
                # STRINGS
                elif spCh == 'string':
                    stringList = [curLex]
                    curPop = None
                    while curPop != curLex:
                        curPop = lex.popleft()
                        stringList.append(curPop)
                    tree = addToTree(tree, 'object', spCh)
                    tree = addToTree(tree, 'parameters', ''.join(stringList))

                elif spCh =='boolean':
                    tree = addToTree(tree, 'object', spCh)
                    if curLex == 'True':
                        curLex = True
                    else: curLex = False
                    tree = addToTree(tree, 'parameters', curLex)

                elif spCh == 'comparison':
                    par1 = tree.pop()
                    obj1 = tree.pop()
                    tree = addToTree(tree, spCh, curLex)
                    values = deque([])
                    values.append(obj1)
                    values.append(par1)
                    held.append('comparison')
                    #parTree = self.treeitize(lex, variables, currentBranch, held)
                    parTree, lex, held = self.treeitize(lex, variables, currentBranch, held)

                    if isinstance(parTree, tuple):
                        parTree, lex, held = parTree
                    while parTree:
                        values.append(parTree.popleft())
                    if (held and held[-1] == 'comparison'):
                        held.pop()
                    tree = addToTree(tree, 'parameters', values)

                elif spCh == 'list':
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
                        tree = addToTree(tree, 'object', spCh)
                        parTree, lex, held = self.treeitize(lex, variables, currentBranch, held)
                        if (held and held[-1] == '['):
                            held.pop()
                        tree = addToTree(tree, 'parameters', parTree)


        if (held and not lex):
            tree = addToTree(tree, 'variable', held.pop())
            #return tree
        #    return tree, lex, held

        #if lex or held:
        #    return tree, lex, held
        #else:
        #    #return tree
        #    return tree, lex, held
        return tree, lex, held
