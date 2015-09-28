from collections import OrderedDict


specialCharacters = OrderedDict({
                     '==': 'comparison',
                     #'!=': 'comparison',
                     '<>': 'comparison',
                     '>=': 'comparison',
                     '<=': 'comparison',
                     '>': 'comparison',
                     '<': 'comparison',
                     '(': 'parenOpen',#None
                     ')': 'parenClose',#None
                     '**': 'arithmetic',
                     '+': 'arithmetic',
                     '-': 'arithmetic',
                     '*': 'arithmetic',
                     '/': 'arithmetic',
                     '%': 'arithmetic',
                     '=': 'variable',
                     '\'': 'string',
                     '"': 'string',
                     '[': 'list',
                     ']': 'list',
                     ',': 'comma',#None
                     '{': 'structure',
                     '}': 'structure',
                     '.': 'dot',#None
                     'get': 'attribFunc',
                     'def': 'function',
                     #'is': 'comparisonWord',
                     #'in': 'comparisonWord',
                     #'not': 'comparisonWord',
                     'if': 'conditional',
                     'else': 'conditional',
                     'for': 'loop',
                     'in': 'loopParam',
                     'True': 'boolean',
                     'False': 'boolean',
                     'quit': 'quit',
                     '\n': 'linebreak'

                     })


paramDefs = {'arithmetic': 2,
             'object': 1,
             'variable': 1,
             'parameters':None,
             'comparison': None,
             'conditional':None,
             'attribFunc':None,
             }


