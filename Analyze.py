from collections import deque
from Scope import Scope
from Lexitize import Lexitize
from Treeitize import Treeitize
import copy

class Analyze():
    def __init__(self):
        self.scope = Scope()

    def analyze(self, tree):

        def simplifyObject(objectString):
            objLex = Lexitize().lexitize(str(objectString))
            tree = Treeitize().treeitize(objLex)[0]
            return tree

        def analyzeObject(objectVariable):
            topValue = objectVariable.popleft()['value']
            parVal = objectVariable.popleft()['value']

            if topValue in ['number', 'boolean', 'string']:
                return parVal
            elif topValue == 'list':
                newList = []
                while parVal:
                    newList.append(self.analyze(parVal.popLeftObject()))
                return newList

        def analyzeVariable(objectVariable):
            variable = objectVariable.popleft()
            variableValue = None
            if objectVariable:
                variableValue = objectVariable.pop()['value']
                simplifiedVariable = simplifyObject(self.analyze(variableValue))
                self.scope.add(variable['value'],
                               simplifiedVariable)
            else:
                varTree = self.scope.get(variable['value'])
                if varTree == None:
                    raise IndexError
                return self.analyze(varTree)

        def analyzeOpComp(objectVariable):
            operator = objectVariable.popleft()['value']
            values = objectVariable.popleft()['value']

            val1 = self.analyze(values.popLeftObject())
            val2 = self.analyze(values.popLeftObject())
            if isinstance(val1, basestring):
                val1 = "'{}'".format(val1)
            if isinstance(val2, basestring):
                val2 = "'{}'".format(val2)
            return eval(str(val1) + operator + str(val2))

        def analyzeConditional(objectVariable):
            conditional = objectVariable.popleft()['value']
            parVal = objectVariable.popleft()['value']

            #true or false to conditional
            compVal = analyzeOpComp(parVal.popLeftObject())

            ifValue = parVal.popLeftObject()
            if compVal:
                return self.analyze(ifValue)
            elif not compVal and parVal:
                elseValue = parVal.popLeftObject()
                return self.analyze(elseValue)

        def analyzeLoop(objectVariable):
            loop = objectVariable.popleft()['value']
            parVal = objectVariable.popleft()['value']

            loopVar = parVal.popleft()['value']
            loopList = parVal.popLeftObject()

            variableExists = False
            if self.scope.get(loopVar):
                variableExists = True

            loopList = self.analyze(loopList)
            loopList = simplifyObject(loopList).pop()['value']

            while loopList:
                currentVarIteration = loopList.popLeftObject()
                self.scope.add(loopVar, currentVarIteration)
                result = self.analyze(copy.deepcopy(parVal))
                if result is not None:
                    print result
            if not variableExists:
                self.scope.pop(loopVar)

        def analyzeAttribFunc(objectVariable):
            attribFunc = objectVariable.popleft()['value']
            parVal = objectVariable.popleft()['value']
            functionParameterTree = parVal.popleft()
            functionObjectTree = parVal.pop()

            functionParameter = self.analyze(functionParameterTree)
            functionObject = self.analyze(functionObjectTree)
            return eval(str(functionObject) + '['+str(functionParameter)+']')


        typeAnalysis = {
            'arithmetic': analyzeOpComp,
            'comparison': analyzeOpComp,
            'object': analyzeObject,
            'variable': analyzeVariable,
            'conditional': analyzeConditional,
            'loop': analyzeLoop,
            'attribFunc': analyzeAttribFunc,
        }

        result = None
        currentObject = tree.popLeftObject()
        currentType = currentObject[0]['type']

        if currentType in typeAnalysis:
            return typeAnalysis[currentType](currentObject)
