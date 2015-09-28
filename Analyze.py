from collections import deque
from Scope import Scope

class Analyze():
    def __init__(self):
        self.scope = Scope()

    def analyze(self, tree):

        def addToTree(tree, ty, val):
            tree.append({'type':ty,'value':val})
            return tree

        def getVariable(var):
            if self.scope.get(var):
                return deque(self.scope.get(var))
            else:
                raise IndexError

        def analyzeObject(topValue, parVal):
            if topValue in ['number', 'boolean', 'string']:
                return parVal
            elif topValue == 'list':
                newList = []
                #***This deque prevents dict overwrite scope problem, not sure
                #why there is a problem in the first place
                values = deque([])
                parVal = deque(parVal)
                objCount = 0
                while parVal:
                    if parVal[0]['type'] in ['object', 'arithmetic',
                                             'comparison', 'variable']:
                        objCount +=1
                    if objCount <= 1:
                        values.append(parVal.popleft())
                    if objCount > 1 or not parVal:
                        result = self.analyze(values)
                        newList.append(result)
                        objCount = 0
                        values = deque([])
                return newList

        def analyzeOpComp(operator, values):
            #finds two values
            tree1 = deque([values.popleft()])
            while values:
                if values[0]['type'] in ['object','arithmetic','variable']:
                    break
                else:
                    tree1.append(values.popleft())

            val1 = self.analyze(tree1)
            val2 = self.analyze(values)
            return eval(str(val1) + operator + str(val2))

        def analyzeVariable(parVal):
            var = self.analyze(parVal)
            varType = getVarType(var)
            if varType == 'list':
                var = createObjTree(var)
            return varType, var

        def analyzeConditional(conditional, parVal):
            #true or false to conditional
            compVal = analyzeOpComp(parVal.popleft()['value'],
                                    parVal.popleft()['value'])

            ifVal = deque([parVal.popleft()])
            #***Get list object
            while parVal:
                if parVal[0]['type'] in ['arithmetic', 'object', 'variable',
                                         'comparison', 'conditional']:
                    ifVal.append(parVal.popleft())
                else:
                    ifVal.append(parVal.popleft())
                    break

            if compVal:
                return self.analyze(ifVal)
            elif not compVal and parVal:
                return self.analyze(parVal)

        def analyzeLoop(loop, parVal):
            #if loop == 'for':
            loopVar = parVal.popleft()
            loopList = deque([])
            #***get list object
            while parVal:
                if parVal[0]['type'] in ['arithmetic', 'object', 'variable',
                                         'comparison', 'conditional']:
                    loopList.append(parVal.popleft())
                else:
                    loopList.append(parVal.popleft())
                    break

            print loopList
            loopList = self.analyze(loopList)
            for x in loopList:
                print x




        def analyzeAttrib(result, attrib, parVal):
            if attrib == 'get':
                param = self.analyze(parVal)
            return eval(str(result)+'['+str(param)+']')

        def getVarType(var):
            varType = None
            #***eventually replace
            #huh, bool is a subclass of int
            if isinstance(var, bool):
                varType = 'boolean'
            elif isinstance(var, (int, long, float, complex)):
                varType = 'number'
            elif isinstance(var, basestring):
                varType = 'string'
            elif isinstance(var, list):
                varType = 'list'
            return varType

        def createObjTree(variables):
            varTree = deque([])
            for x in variables:
                varType = getVarType(x)
                varTree = addToTree(varTree, 'object', varType)
                varTree = addToTree(varTree, 'parameters', x)
            return varTree


        result = None
        top = tree.popleft()
        topType = top['type']
        topValue = top['value']

        #check if in objects and return actual val
        if topType == 'object':
            parameters = tree.popleft()
            result = analyzeObject(topValue, parameters['value'])

        elif topType in ['arithmetic', 'comparison']:
            parameters = tree.popleft()
            result = analyzeOpComp(topValue, parameters['value'])

        #***reduce to 2 lines and sub function
        elif topType == 'variable':
            parameters = None
            #***THIS ASSUMES VAR LAST ITEM SHOULD PUT BACK IF NOT PARAMETERS
            if tree:
                parameters = tree.popleft()
            if (parameters and parameters['type'] == 'parameters'):
                objType, objValue = analyzeVariable(parameters['value'])
                varTree = deque([])
                varTree = addToTree(varTree, 'object', objType)
                varTree = addToTree(varTree, 'parameters', objValue)
                self.scope.add(topValue, varTree)
            else:
                if parameters:
                    tree.appendleft(parameters)
                varTree = getVariable(topValue)

                result = self.analyze(varTree)

        elif topType == 'conditional':
            parameters = tree.popleft()
            result = analyzeConditional(topValue, parameters['value'])

        elif topType == 'loop':
            parameters = tree.popleft()
            result = analyzeLoop(topValue, parameters['value'])


        if tree and isinstance(result, (list,basestring)):
            result = analyzeAttrib(result,
                                   tree.popleft()['value'],
                                   tree.popleft()['value'])

        return result
