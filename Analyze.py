from collections import deque
from Scope import Scope

class Analyze():
    def __init__(self):
        self.scope = Scope()

    def analyze(self, tree):

        def addToTree(tree, ty, val):
            tree.append({'type':ty,'value':val})
            return tree

        #doing too much?
        def getVariable(var):
            if self.scope.get(var):
                vt = deque(self.scope.get(var))
                return analyzeObject(vt.popleft()['value'],
                                     vt.popleft()['value'])
            else: return var

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

        #***scope check should be cleaner
        #***should receive topVal instead of whole item(operator)
        def analyzeOperator(operator, parameters):
            if len(parameters['value']) == 2:
                vals = deque(parameters['value'])
                val1 = getVariable(vals.popleft())
                val2 = getVariable(vals.popleft())
                return eval('('+str(val1)+')'+operator['value']+'('+str(val2)+')')
            val1 = parameters['value'].pop(0)
            if isinstance(val1, dict):
                val1 = analyzeOperator(val1, parameters['value'].pop(0))
            val2 = parameters['value'].pop(0)
            if isinstance(val2, dict):
                val2 = analyzeOperator(val2, parameters['value'].pop(0))
            val1 = getVariable(val1)
            val2 = getVariable(val2)
            return eval('('+str(val1)+')' + operator['value'] + '('+str(val2)+')')

        def analyzeComparison(operator, values):
            tree1 = deque([])
            tree1.append(values.popleft())
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

        #**********analyzing needs references to existing objects
        #**cannot just recreate analyze, need to at least pass objects
        result = None


        top = tree.popleft()
        topType = top['type']
        topValue = top['value']

        #check if in objects and return actual val
        if topType == 'object':
            parameters = tree.popleft()
            result = analyzeObject(topValue, parameters['value'])

        elif topType == 'arithmetic':
            #popleft?
            parameters = tree.popleft()
            result = analyzeOperator(top, parameters)

        elif topType == 'comparison':
            parameters = tree.popleft()
            result = analyzeComparison(topValue, parameters['value'])


        elif topType == 'variable':
            #popleft?
            parameters = None
            if tree:
                parameters = tree.popleft()
            if (parameters and parameters['type'] == 'parameters'):
                objType, objValue = analyzeVariable(parameters['value'])
                varTree = deque([])
                varTree = addToTree(varTree, 'object', objType)
                varTree = addToTree(varTree, 'parameters', objValue)
                self.scope.add(topValue, varTree)
                #result = analyzeObject(objType, objValue)
            else:
                varTree = deque(self.scope.get(topValue))

#DEQUE index access as ends is O(1)
                result = analyzeObject(varTree[0]['value'],
                                       varTree[1]['value'])
            print self.scope.variables

            #if result: return result
            #else:
            #    raise IndexError


        return result
