# Define the transition table
transition_table = {
    'q0': {
        '$': 'q1',
        'digit': 'q3',
        "'": 'q6',
        '/': 'q9',
        '=': 'q14',
        '>': 'q16',
        '<': 'q17',
        "!": 'q18',
        '+': 'q20',
        '-': 'q21',
        '*': 'q22',
        ';': 'q23',
        '&': 'q24',
        '|': 'q26',
        "{": 'q28',
        '}': 'q29',
        '(': 'q30',
        ')': 'q31',
        '[': 'q32',
        ']': 'q33',
        ':': 'q34',
        ' ': 'q0'},

    # identifiers
    'q1': {'letter': 'q2', 'digit': 'q2'},
    'q2': {'letter': 'q2', 'digit': 'q2'},

    # numbers
    'q3': {'digit': 'q3', '.': 'q4', '>': 'q16', '<': 'q17', '!': 'q18'},
    'q4': {'digit': 'q5'},
    'q5': {'digit': 'q5',  '>': 'q16', '<': 'q17', '!': 'q18'},

    # strings
    'q6': {
        'letter': 'q7',
        'digit': 'q7',
        ' ': 'q7',
        '$': 'q7',
        "'": 'q7',
        '/': 'q7',
        '=': 'q7',
        '>': 'q7',
        '<': 'q7',
        "!": 'q7',
        '+': 'q7',
        '-': 'q7',
        '*': 'q7',
        ';': 'q7',
        '&': 'q7',
        '|': 'q7',
        "{": 'q7',
        '}': 'q7',
        '(': 'q7',
        ')': 'q7',
        '[': 'q7',
        ']': 'q7',
        ':': 'q7',
        '¿': 'q7',
        '?': 'q7',
        '!': 'q7',
        '¡': 'q7',
        ' ': 'q7'},

    'q7': {
        'letter': 'q7',
        'digit': 'q7',
        ' ': 'q7',
        '$': 'q7',
        "'": 'q7',
        '/': 'q7',
        '=': 'q7',
        '>': 'q7',
        '<': 'q7',
        "!": 'q7',
        '+': 'q7',
        '-': 'q7',
        '*': 'q7',
        ';': 'q7',
        '&': 'q7',
        '|': 'q7',
        "{": 'q7',
        '}': 'q7',
        '(': 'q7',
        ')': 'q7',
        '[': 'q7',
        ']': 'q7',
        ':': 'q7',
        '¿': 'q7',
        '?': 'q7',
        '!': 'q7',
        '¡': 'q7',
        ' ': 'q7',
        "'": 'q8'},

    'q8': {},

    # comments
    'q9': {'*': 'q10'},
    'q10': {'\n': 'q11', 'letter': 'q11', 'digit': 'q11', '*': 'q11', 'other': 'q11', ' ': 'q10'},
    'q11': {'\n': 'q11', 'letter': 'q11', 'digit': 'q11', '*': 'q12', 'other': 'q11', ' ': 'q11'},
    'q12': {'/': 'q13'},
    'q13': {},

    # operators
    'q14': {'=': 'q15'},
    'q16': {'=': 'q19'},
    'q17': {'=': 'q19'},
    'q18': {'=': 'q19'},
    'q24': {'&': 'q25'},
    'q26': {'|': 'q27'},

    # blank spaces
    'q15': {},
    'q19': {},
    'q20': {},
    'q21': {},
    'q22': {},
    'q23': {},
    'q25': {},
    'q27': {},
    'q28': {},
    'q29': {},
    'q30': {},
    'q31': {},
    'q32': {},
    'q33': {},
    'q34': {},
}

# Define the accepting states and their corresponding types
accepting_states = {
    'q2': 'id',
    'q3': 'entero',
    'q5': 'real',
    'q8': 'cadena',
    'q9': '/',
    'q13': 'comment',
    'q14': '=',
    'q15': '==',
    'q16': '>',
    'q17': '<',
    'q18': '!',
    'q19': 'operator',
    'q20': '+',
    'q21': '-',
    'q22': '*',
    'q23': ';',
    'q25': 'y',
    'q27': 'o',
    'q28': '{',
    'q29': '}',
    'q30': '(',
    'q31': ')',
    'q32': '[',
    'q33': ']',
    'q34': ':'
}

reserved_words = {
    '$ ',
    'programa',
    'principal',

    'init',

    'si',
    'Sino',
    'entonces',
    'fin_sino',

    'variable',
    'entero',
    'cadena',
    'real',
    'caracter',
    'arreglo',

    'leer',
    'escribir',

    'hasta',
    'mientras',
    'repetir',
    'para',
    'hacer',

    'booleano',
    'verdadero',
    'falso',
    '..',
    'de'
}

data_types = {
    'entero',
    'cadena',
    'real',
    'caracter',
    'arreglo',
    'booleano',
}
