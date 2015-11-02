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
                     #('lambda', 'lambda'),
                     ('if', 'conditional'),
                     ('for', 'loop'),
                     ('while', 'loop'),
                     ('in', 'loopParam'),
                     ('True', 'boolean'),
                     ('False', 'boolean'),
                     ('None', 'NullValue'),
                     #('quit', 'quit'),
                     ('\n', 'linebreak'),
                     ('\t', 'tabs'),
                     (' ', 'whitespace'),

                     ))

objectTypes = [
    'arithmetic',
    'comparison',
    'object',
    'variable',
    'conditional',
    'attribFunc'

]


#typeAnalysis = {
#    'arithmetic': None,
#    'comparison': None,
#    'object': None,
#    'variable': None,
#    'conditional': None,
#    'loop': None,
#}

