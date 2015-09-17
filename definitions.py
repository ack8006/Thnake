specialCharacters = {'(': None,
                     ')': None,
                     '+': 'arithmetic',
                     '-': 'arithmetic',
                     '*': 'arithmetic',
                     '/': 'arithmetic',
                     '%': 'arithmetic',
                     '**': 'arithmetic',
                     '=': 'variable',
                     '\'': 'object',
                     '"': 'object',
                     '[': 'dataStructure',
                     ']': 'dataStructure',
                     ',': None,
                     '{': 'dataStructure',
                     '}': 'dataStructure',
                     '.': None,
                     'def': 'function',
                     '==': 'comparison',
                     '!=': 'comparison',
                     '<>': 'comparison',
                     '>': 'comparison',
                     '<': 'comparison',
                     '>=': 'comparison',
                     '<=': 'comparison',
                     'is': 'comparison',
                     'in': 'comparison',
                     'not': 'comparison',

                     }


paramDefs = {'arithmetic': 2,
             'object': 1,
             'variable': 1,
             }


