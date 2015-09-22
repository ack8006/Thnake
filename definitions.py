specialCharacters = {'(': 'paren',#None
                     ')': 'paren',#None
                     '+': 'arithmetic',
                     '-': 'arithmetic',
                     '*': 'arithmetic',
                     '/': 'arithmetic',
                     '%': 'arithmetic',
                     '**': 'arithmetic',
                     '=': 'variable',
                     '\'': 'string',
                     '"': 'string',
                     '[': 'list',
                     ']': 'list',
                     ',': 'comma',#None
                     '{': 'dataStructure',
                     '}': 'dataStructure',
                     '.': 'dot',#None
                     'def': 'function',
                     '==': 'comparison',
                     '!=': 'comparison',
                     '<>': 'comparison',
                     '>': 'comparison',
                     '<': 'comparison',
                     '>=': 'comparison',
                     '<=': 'comparison',
                     #'is': 'comparisonWord',
                     #'in': 'comparisonWord',
                     #'not': 'comparisonWord',
                     'if': 'if',
                     'True': 'boolean',
                     'False': 'boolean',
                     'quit': 'quit',

                     }


paramDefs = {'arithmetic': 2,
             'object': 1,
             'variable': 1,
             }


