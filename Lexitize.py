from collections import deque
from definitions import *


class Lexitize():
    def __init__(self):
        pass

    def lexitize(self, inp):

        #***parses in out of a string of 'string'
        #***only add to arith and comparison and others that need it
        def spCharSpaces(inp):
            excludeDef= ['comparisonWord', 'function', 'if', 'bool']
            for char in [x for x,y in specialCharacters.iteritems()
                         if y not in excludeDef]:
                inp = inp.replace(char, ' '+char+' ')
            #special case
            inp = inp.replace('*  *', '**')
            inp = inp.replace('=  =', '==')
            inp = inp.replace('<  =', '<=')
            inp = inp.replace('>  =', '>=')
            return inp

        def cleanWhiteSpace(lex):
            lex = [x for x in lex if x != '']
            return lex

        inp = spCharSpaces(inp)
        lexPieces = inp.split(' ')
        lexPieces = cleanWhiteSpace(lexPieces)
        return deque(lexPieces)
