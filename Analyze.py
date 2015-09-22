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
                #where there is a problem in the first place
                values = deque(parVal)
                while values:
                    result = self.analyze(values)
                    newList.append(result)
                return newList

        def analyzeOpComp(operator, values):
            #pops first value pair into new deque
            tree1 = deque([values.popleft() for _i in xrange(2)])
            val1 = self.analyze(tree1)
            val2 = self.analyze(values)
            return eval(str(val1) + operator + str(val2))

        def analyzeVariable(parVal):
            var = self.analyze(parVal)
            varType = getVarType(var)
            if varType == 'list':
                var = createObjTree(var)
            return varType, var

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

        elif topType == 'variable':
            parameters = None
            if tree:
                parameters = tree.popleft()
            if (parameters and parameters['type'] == 'parameters'):
                objType, objValue = analyzeVariable(parameters['value'])
                varTree = deque([])
                varTree = addToTree(varTree, 'object', objType)
                varTree = addToTree(varTree, 'parameters', objValue)
                self.scope.add(topValue, varTree)
            else:
                varTree = getVariable(topValue)
                #DEQUE index access as ends is O(1)
                result = analyzeObject(varTree[0]['value'],
                                       varTree[1]['value'])

        return result
