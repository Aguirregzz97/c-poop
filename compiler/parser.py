import ply.yacc as yacc
import lexer
import symbol_table
from symbol_table import Var
import semantic_cube
import ops_table
import sys
import pprint

tokens = lexer.tokens
cube = semantic_cube.cube

success = True

context = 'main'
my_list = []


def changeContext(func_name):
    global context
    context = func_name


def addVariablesToFunction():
    global context
    global my_list
    for var in my_list:
        symbol_table.insert_var(
            context, var['var_name'], var['type'], var['addr'], var['value'])
        my_list = []


# --- GENERALES ---

def p_program(p):
    '''program : PROGRAM ID SEMICOLON main_dec bloque
               | PROGRAM ID SEMICOLON vars main_dec bloque
               | PROGRAM ID SEMICOLON funciones main_dec bloque
               | PROGRAM ID SEMICOLON vars funciones main_dec bloque'''


def p_funciones(p):
    '''funciones : funcion
                 | funcion funciones'''


def p_main_dec(p):
    '''main_dec : MAIN LPAREN RPAREN'''


def p_vars(p):
    '''vars : VAR varAux1'''


def p_varAux1(p):
    '''varAux1 : tipo varAux2 SEMICOLON
               | tipo varAux2 SEMICOLON varAux1'''
    # symbol_table.insert_var(context, p[2]['name'], p[1], 0, p[2]['value'])
    my_list.append({
        'var_name': p[2]['name'],
        'type': p[1],
        'addr': 0,
        'value': p[2]['value']
    })


def p_varAux2(p):
    '''varAux2 : ID
               | ID COMMA varAux2
               | ID EQUAL expresion
               | ID EQUAL expresion COMMA varAux2'''

    # ESTOS HANDLERS PODRIAN MANEJARSE EN OTRO ARCHIVO DESPUES REFACTORIZAMOS
    # FIXME : checar por comas
    if (len(p) > 2):
        if (p[2] == '='):
            p[0] = {'name': p[1], 'value': 'xd'}
    else:
        p[0] = {'name': p[1], 'value': 'null'}


def p_tipo(p):
    '''tipo : INT
            | FLOAT
            | STRING
            | BOOL'''
    p[0] = p[1]


def p_bloque(p):
    '''bloque : LBRACE RBRACE
              | LBRACE bloqueAux RBRACE'''


def p_bloqueAux(p):
    '''bloqueAux : estatuto
                 | estatuto bloqueAux'''


def p_estatuto(p):
    '''estatuto : asignacion
                | condicion
                | escritura
                | loop
                | func_call'''


def p_asignacion(p):
    '''asignacion : ID EQUAL expresion SEMICOLON'''


def p_condicion(p):
    '''condicion : IF LPAREN expresion RPAREN bloque SEMICOLON
                 | IF LPAREN expresion RPAREN bloque ELSE bloque SEMICOLON'''


def p_escritura(p):
    '''escritura : PRINT LPAREN escrituraAux RPAREN SEMICOLON'''


def p_escrituraAux(p):
    '''escrituraAux : expresion
                    | expresion COMMA escrituraAux'''


def p_expresion(p):
    '''expresion : exp2
                 | exp2 AND expresion
                 | exp2 OR expresion'''



# --- NIVEL EXP2 ---

def p_exp2(p):
    '''exp2 : exp3
            | exp3 LT exp3
            | exp3 LTE exp3
            | exp3 GT exp3
            | exp3 GTE exp3
            | exp3 EQUALEQUAL exp3
            | exp3 NOTEQUAL exp3'''
    p[0] = p[1]




# --- NIVEL EXP3 ---

def p_exp3(p):
    '''exp3 : termino
            | addition
            | subtraction'''
    p[0] = p[1]

def p_addition(p):
    '''addition : termino PLUS exp3'''
    p[0] = resolve_operation('+', p[1], p[3])

def p_subtraction(p):
    '''subtraction : termino MINUS exp3'''
    p[0] = resolve_operation('-', p[1], p[3])




# --- NIVEL TERMINO ---

def p_termino(p):
    '''termino : factor
               | mult
               | div
               | floor_div'''
    p[0] = p[1]

def p_mult(p):
    '''mult : factor TIMES termino'''
    p[0] = resolve_operation('*', p[1], p[3])

def p_div(p):
    '''div : factor DIVIDE termino'''
    p[0] = resolve_operation('/', p[1], p[3])

def p_floor_div(p):
    '''floor_div : factor FLOOR_DIVIDE termino'''
    p[0] = resolve_operation('//', p[1], p[3])




# --- NIVEL FACTOR ---

def p_factor(p):
    '''factor : LPAREN expresion RPAREN
              | factorAux'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_factorAux(p):
    '''factorAux : unary_plus
                 | unary_minus
                 | unary_not
                 | var_cte'''
    p[0] = p[1]

def p_unary_plus(p):
    '''unary_plus : PLUS var_cte'''
    p[0] = resolve_operation2('unary+', p[2])

def p_unary_minus(p):
    '''unary_minus : MINUS var_cte'''
    p[0] = resolve_operation2('unary-', p[2])

def p_unary_not(p):
    '''unary_not : NOT var_cte'''
    p[0] = resolve_operation2('unary!', p[2])



# --- VARIABLE DECLARATION ---

def p_var_cte(p):
    '''var_cte : id
               | cte_i
               | cte_f
               | cte_string
               | cte_bool
               | func_call_var
               '''
    p[0] = p[1]


def p_id(p):
    '''id : ID'''

    # FIXME: should search id in symbol table based on context and return value
    p[0] = Var('string', 'fixme')

def p_cte_i(p):
    '''cte_i : CTE_I'''
    p[0] = Var('int', int(p[1]))

def p_cte_f(p):
    '''cte_f : CTE_F'''
    p[0] = Var('float', float(p[1]))

def p_cte_string(p):
    '''cte_string : CTE_STRING'''
    p[1] = p[1][1:-1]
    p[0] = Var('string', str(p[1]))

def p_cte_bool(p):
    '''cte_bool : CTE_BOOL'''
    p[0] = Var('bool', bool(p[1]))


# --- CONTROL ---

def p_loop(p):
    '''loop : LOOP LPAREN expresion RPAREN bloque
            | LOOP CTE_I bloque'''


# --- FUNCIONES ---

def p_funcion(p):
    '''funcion : DEF tipo funcionAux RETURN expresion SEMICOLON RBRACE
               | DEF VOID funcionAux RBRACE'''
    symbol_table.insert_func(p[3]['func_name'], p[2], 100)
    addVariablesToFunction()


def p_funcionAux(p):
    '''funcionAux : dec_func LBRACE
                  | dec_func LBRACE vars
                  | dec_func LBRACE funcionAux2
                  | dec_func LBRACE vars funcionAux2'''
    p[0] = {'func_name': p[1]['func_name']}


def p_funcionAux2(p):
    '''funcionAux2 : estatuto
                   | estatuto funcionAux2'''


def p_dec_func(p):
    '''dec_func : ID LPAREN RPAREN
                | ID LPAREN dec_func_aux RPAREN'''
    p[0] = {'func_name': p[1]}
    changeContext(p[1])


def p_dec_func_aux(p):
    '''dec_func_aux : tipo ID
                    | tipo ID COMMA dec_func_aux'''


def p_func_call(p):
    '''func_call : ID LPAREN RPAREN SEMICOLON
                 | ID LPAREN func_call_aux RPAREN SEMICOLON'''

    # FIXME: should evaluate function and return a value
    p[0] = Var('string', 'fixme')


def p_func_call_var(p):
    '''func_call_var : ID LPAREN RPAREN
                 | ID LPAREN func_call_aux RPAREN'''


def p_func_call_aux(p):
    '''func_call_aux : expresion
                     | expresion COMMA func_call_aux'''


# --- ERRORS ---

def p_error(p):
    global success
    success = False
    print("Error de sintaxis en '%s'" % p.value)
    sys.exit()


def type_mismatch(op1, op, op2):
    print('ERROR: Type mismatch! => ' + str(op1) + op + str(op2))



# --- UTILS ---

def resolve_operation(op, op1, op2):
    type = cube[op][op1.type][op2.type]

    if (type == 'error'):
        type_mismatch(op1.value, op, op2.value)
        sys.exit()
    else:
        val = ops_table.ops[op](op1.value, op2.value)
        return Var(type, val)

def resolve_operation2(op, op1):
    type = cube[op][op1.type]['']

    if (type == 'error'):
        type_mismatch(op1.value, op)
        sys.exit()
    else:
        val = ops_table.ops[op](op1.value)
        return Var(type, val)

# --- PARSING ---
parser = yacc.yacc(debug=False, write_tables=False)


archivo = "tests/exp3_test.txt"
f = open(archivo, 'r')
s = f.read()

parser.parse(s)

if success == True:
    print("Archivo aprobado")

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(symbol_table.func_table)

    sys.exit()
else:
    print("Archivo no aprobado")
    sys.exit()
