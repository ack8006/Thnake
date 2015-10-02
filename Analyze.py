from Scope import Scope
from Lexitize import Lexitize
from Treeitize import Treeitize
import copy

class Analyze():
    def __init__(self):
        self.scope = Scope()

    def analyze(self, tree):

        def simplifyObject(objectString):
            if isinstance(objectString, basestring):
                objectString = "'{}'".format(objectString)
            objLex = Lexitize().lexitize(str(objectString))[0]
            tree = Treeitize().treeitize(objLex)[0]
            return tree

        def getTopObjectAndParameter(objectVariable):
            return (objectVariable.popleft()['value'],
                    objectVariable.popleft()['value'])

        def analyzeObject(objectVariable):
            topValue, parVal = getTopObjectAndParameter(objectVariable)

            if topValue in ['number', 'boolean', 'string', None]:
                return parVal
            elif topValue == 'list':
                newList = []
                while parVal:
                    newList.append(self.analyze(parVal.popLeftObject()))
                return newList

        def analyzeVariable(objectVariable):
            variable, variableValue = getTopObjectAndParameter(objectVariable)
            if variableValue == None:
                variableTree = self.scope.get(variable)
                return self.analyze(variableTree)
            else:
                simplifiedVariable = simplifyObject(self.analyze(variableValue))
                self.scope.add(variable, simplifiedVariable)

        def analyzeOpComp(objectVariable):
            operator, values = getTopObjectAndParameter(objectVariable)

            val1 = self.analyze(values.popLeftObject())
            val2 = self.analyze(values.popLeftObject())
            if isinstance(val1, basestring):
                val1 = "'{}'".format(val1)
            if isinstance(val2, basestring):
                val2 = "'{}'".format(val2)
            return eval(str(val1) + operator + str(val2))

        def analyzeConditional(objectVariable):
            conditional, parVal = getTopObjectAndParameter(objectVariable)

            #true or false to conditional
            values = parVal.pop()
            ifValueTree = values.popleft()
            compVal = analyzeOpComp(parVal)

            if compVal:
                return executeConditionStructure(ifValueTree)
            elif not compVal and values:
                elseValue = values.pop()
                return executeConditionStructure(elseValue)

        def analyzeLoop(objectVariable):
            loop, parVal = getTopObjectAndParameter(objectVariable)
            if loop == 'while':
                analyzeWhileLoop(parVal)
            elif loop == 'for':
                analyzeForLoop(parVal)

        def analyzeWhileLoop(parVal):
            loopCondition = parVal.popLeftObject()
            while self.analyze(copy.deepcopy(loopCondition)):
                executeConditionStructure(parVal)

        def analyzeForLoop(parVal):
            loopVar = parVal.popLeftObject().popleft()['value']
            loopList = parVal.popLeftObject()
            loopList = self.analyze(loopList)
            loopList = simplifyObject(loopList).pop()['value']

            variableExists = False
            if self.scope.get(loopVar):
                variableExists = True

            while loopList:
                currentVarIteration = loopList.popLeftObject()
                self.scope.add(loopVar, currentVarIteration)
                executeConditionStructure(parVal)

            if not variableExists:
                self.scope.pop(loopVar)

        def executeConditionStructure(parVal):
            parVal = copy.deepcopy(parVal)
            while parVal:
                result = self.analyze(parVal.popLeftObject())
                if result is not None:
                    print result
            return result


        def analyzeAttribFunc(objectVariable):
            attribFunc, parVal = getTopObjectAndParameter(objectVariable)

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
