from collections import OrderedDict


specialCharacters = OrderedDict((
                     ('\'', 'string'),
                     ('"', 'string'),
                     ('==', 'comparison'),
                     #('!=', 'comparison'),
                     ('<>', 'comparison'),
                     ('>=', 'comparison'),
                     ('<=', 'comparison'),
                     ('>', 'comparison'),
                     ('<', 'comparison'),
                     ('(', 'parenOpen'),#None
                     (')', 'parenClose'),#None
                     ('**', 'arithmetic'),
                     ('+', 'arithmetic'),
                     ('-', 'arithmetic'),
                     ('*', 'arithmetic'),
                     ('/', 'arithmetic'),
                     ('%', 'arithmetic'),
                     ('=', 'variable'),
                     ('[', 'list'),
                     (']', 'list'),
                     (',', 'comma'),#None
                     ('{', 'structure'),
                     ('}', 'structure'),
                     ('.', 'dot'),#None
                     ('get', 'attribFunc'),
                     #('append', 'attribFunc'),
                     #('remove', 'attribFunc'),
                     #('def', 'function'),
                     #('is', 'comparisonWord'),
                     #('in', 'comparisonWord'),
                     #('not', 'comparisonWord'),
                     ('lambda', 'lambda'),
                     ('if', 'conditional'),
                     ('for', 'loop'),
                     ('in', 'loopParam'),
                     ('True', 'boolean'),
                     ('False', 'boolean'),
                     ('quit', 'quit'),
                     #('\n', 'linebreak'),
                     (' ', 'whitespace'),

                     ))

objectTypes = [
    'arithmetic',
    'comparison',
    'object',
    'variable',
    'conditional',
]


typeAnalysis = {
    'arithmetic': None,
    'comparison': None,
    'object': None,
    'variable': None,
    'conditional': None,
    'loop': None,
}


paramDefs = {'arithmetic': 2,
             'object': 1,
             'variable': 1,
             'parameters':None,
             'comparison': None,
             'conditional':None,
             'attribFunc':None,
             }


