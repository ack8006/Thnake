from interpreter import *


def runTest(string):
    print string
    lex = lexization(string)
    print lex
    tree = treeitize(lex)
    print tree
    result = analyze(tree)
    print result
    print


def arithmeticTest():
    return ['1+1', '1+2*4**3', '3+4*2/(1-5)**2**2']

def objectTest():
    return ['5', '"string"', "'string2'"]

def variableTest():
    return ['x=5', 'x="test"', 'x=4+5']

def dataStructTest():
    return ['[1,2,3,4]','[[1,2],1]']


if __name__ == '__main__':
    print 'ArithmeticTests'
    for x in arithmeticTest():
        runTest(x)
    print '\n\n OBJECT TEST'
    for x in objectTest():
        runTest(x)
    print '\n\n VARIBLE TEST'
    for x in variableTest():
        runTest(x)
    print '\n\n DataStruct Test'
    for x in dataStructTest():
        runTest(x)

