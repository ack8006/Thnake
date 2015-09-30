from collections import deque
from Scope import Scope
import copy

class Analyze():
    def __init__(self):
        self.scope = Scope()

    def analyze(self, tree):

        def getVariable(var):
            if self.scope.get(var):
                return copy.deepcopy(self.scope.get(var))
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
                parVal = parVal
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

            loopList = self.analyze(loopList)
            print 'PV'
            print parVal
            for x in loopList:
                print x

        def analyzeAttrib(result, attrib, parVal):
            if attrib == 'get':
                param = self.analyze(parVal)
            return eval(str(result)+'['+str(param)+']')



        typeAnalysis = {
            'arithmetic': analyzeOpComp,
            'comparison': analyzeOpComp,
            'object': analyzeObject,
            'conditional': analyzeConditional,
            'loop': analyzeLoop
        }

        result = None
        top = tree.popleft()
        topType = top['type']
        topValue = top['value']

        if topType in typeAnalysis:
            result = typeAnalysis[topType](topValue, tree.popleft()['value'])

        elif topType == 'variable':
            if tree and tree[0]['type'] == 'parameters':
                self.scope.add(topValue, tree.popleft()['value'])
            else:
                varTree = getVariable(topValue)
                result = self.analyze(varTree)

        while tree and isinstance(result, (list,basestring)):
            result = analyzeAttrib(result,
                                   tree.popleft()['value'],
                                   tree.popleft()['value'])

        return result
