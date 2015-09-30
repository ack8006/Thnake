from collections import deque
from definitions import *
import re


class Lexitize():
    def __init__(self):
        pass

    @staticmethod
    def cleanWhiteSpace(lex):
        lex = [x for x in lex if x not in [' ','']]
        return lex

    @staticmethod
    def splitLexPieces(lexPieces, spCh):
        splitLex = []
        for item in lexPieces:
            if item in specialCharacters.keys():
                splitLex.append(item)
                #skip ahead for string so don't accidentally analyze inside
                if specialCharacters[item] == 'string':
                    splitLex.append(lexPieces.next())
                    splitLex.append(lexPieces.next())
            else:
                #inserts split item and pops last one off
                for i in item.split(spCh):
                    splitLex.append(i)
                    splitLex.append(spCh)
                splitLex.pop()
        return splitLex

    def lexitize(self, inp):
        lexPieces = [inp]
        for x in specialCharacters.keys():
            lexPieces = self.splitLexPieces(iter(lexPieces), x)
        lexPieces = self.cleanWhiteSpace(lexPieces)
        return deque(lexPieces)




