import ply.lex as lex
from error_control import err

reserved = {
    'program': 'PROGRAM',
    'var': 'VAR',
    'if': 'IF',
    'else': 'ELSE',
    'float': 'FLOAT',
    'int': 'INT',
    'string': 'STRING',
    'bool': 'BOOL',
    'void': 'VOID',
    'and': 'AND',
    'or': 'OR',
    'print': 'PRINT',
    'repeat': 'REPEAT',
    'while': 'WHILE',
    'def': 'DEF',
    'return': 'RETURN',
    'main': 'MAIN',
    'emojiprint': 'EMOJIPRINT'
}

# List of tokens
tokens = [
    'ID',
    'CTE_I',
    'CTE_F',
    'CTE_STRING',
    'CTE_BOOL',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'FLOOR_DIVIDE',
    'NOT',
    'EQUAL',
    'EQUALEQUAL',
    'NOTEQUAL',
    'LT',
    'LTE',
    'GT',
    'GTE',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'COMMA',
    'SEMICOLON',
    'LSQBRACE',
    'RSQBRACE'
]

# Caracteres ignorados
t_ignore = ' \t\n'

# Arithmetic Operators
t_NOT = r'\!'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_FLOOR_DIVIDE = r'\/\/'

# Relational Operators
t_EQUAL = r'\='
t_EQUALEQUAL = r'\=\='
t_NOTEQUAL = r'\!\='
t_LT = r'\<'
t_LTE = r'\<\='
t_GT = r'\>'
t_GTE = r'\>\='

# Symbols
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r'\,'
t_SEMICOLON = r'\;'
t_LSQBRACE = r'\['
t_RSQBRACE = r'\]'


# Constants


def t_CTE_F(t):
    r'[0-9]+\.[0-9]+'
    t.type = reserved.get(t.value, 'CTE_F')
    t.value = float(t.value)
    return t


def t_CTE_I(t):
    r'[0-9]+'
    t.type = reserved.get(t.value, 'CTE_I')
    t.value = int(t.value)
    return t


def t_CTE_S(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.type = reserved.get(t.value, 'CTE_STRING')
    t.value = str(t.value)
    return t


def t_CTE_BOOL(t):
    r'(true|false)'
    if (t.value == 'false'):
        t.value = 0
    t.type = reserved.get(t.value, 'CTE_BOOL')
    t.value = bool(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


tokens = tokens + list(reserved.values())


def t_error(t):
    global success
    success = False
    err('Illegal character!', t.value[0])


# Construye el lexer
lex.lex()
