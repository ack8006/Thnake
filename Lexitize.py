from collections import deque
from definitions import *
import re


class Lexitize():
    def __init__(self):
        pass

    @staticmethod
    def cleanWhiteSpace(lex):
        lex = [x for x in lex if x not in ['\t', ' ','']]
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

    def parseLinebreaks(self, lexPieces):
        lexOfLexes = []
        currentLex = deque([])
        structureCount = 0
        while lexPieces:
            current = lexPieces.pop(0)
            if current == '{':
                currentLex.append(current)
                structureCount += 1
            elif current == '}':
                currentLex.append(current)
                structureCount -= 1
            elif current != '\n':
                currentLex.append(current)
            elif (current == '\n' and structureCount !=0):
                currentLex.append(current)
                pass
            elif currentLex:
                lexOfLexes.append(currentLex)
                currentLex = deque([])
        if currentLex:
            lexOfLexes.append(currentLex)
        return lexOfLexes

    def lexitize(self, inp):
        lexPieces = [inp]
        for x in specialCharacters.keys():
            lexPieces = self.splitLexPieces(iter(lexPieces), x)
        lexPieces = self.cleanWhiteSpace(lexPieces)
        lexOfLexes = self.parseLinebreaks(lexPieces)
        return lexOfLexes
        #return deque(lexPieces)

