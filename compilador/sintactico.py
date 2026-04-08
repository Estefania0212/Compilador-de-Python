import ply.yacc as yacc
from compilador.lexico import tokens, encontrar_columna

# Diccionario para almacenar variables (para análisis semántico simple)
variables = {}

# Precedencia de operadores
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUAL', 'DIFERENTE'),
    ('left', 'MENOR', 'MENORIGUAL', 'MAYOR', 'MAYORIGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO', 'MODULO'),
    ('right', 'UNARIO'),
)

# Programa: lista de sentencias
def p_programa(p):
    '''program : statements'''
    p[0] = ('program', p[1])

def p_sentencias_multiples(p):
    '''statements : statements statement'''
    p[0] = p[1] + [p[2]]

def p_sentencia_simple(p):
    '''statements : statement'''
    p[0] = [p[1]]

# Sentencias posibles
def p_sentencia_asignacion(p):
    '''statement : IDENTIFICADOR ASIGNAR expression'''
    variables[p[1]] = None  # Para análisis semántico simple
    p[0] = ('assign', p[1], p[3])

def p_sentencia_expresion(p):
    '''statement : expression'''
    p[0] = ('expr', p[1])

def p_sentencia_if(p):
    '''statement : IF expression DOS_PUNTOS statements
                 | IF expression DOS_PUNTOS statements ELSE DOS_PUNTOS statements'''
    if len(p) == 5:
        p[0] = ('if', p[2], p[4], None)
    else:
        p[0] = ('if', p[2], p[4], p[7])

def p_statement_while(p):
    '''statement : WHILE expression DOS_PUNTOS statements'''
    p[0] = ('while', p[2], p[4])

def p_statement_for(p):
    '''statement : FOR IDENTIFICADOR IN expression DOS_PUNTOS statements'''
    p[0] = ('for', p[2], p[4], p[6])

def p_statement_funcdef(p):
    '''statement : DEF IDENTIFICADOR PARENTESIS_IZQ params PARENTESIS_DER DOS_PUNTOS statements'''
    p[0] = ('funcdef', p[2], p[4], p[7])

def p_params_multiple(p):
    '''params : params COMA IDENTIFICADOR'''
    p[0] = p[1] + [p[3]]

def p_params_single(p):
    '''params : IDENTIFICADOR'''
    p[0] = [p[1]]

def p_params_empty(p):
    '''params : '''
    p[0] = []

# Expresiones
def p_expression_binop(p):
    '''expression : expression MAS expression
                  | expression MENOS expression
                  | expression POR expression
                  | expression DIVIDIDO expression
                  | expression MODULO expression
                  | expression IGUAL expression
                  | expression DIFERENTE expression
                  | expression MENOR expression
                  | expression MENORIGUAL expression
                  | expression MAYOR expression
                  | expression MAYORIGUAL expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_unario(p):
    '''expression : MENOS expression %prec UNARIO'''
    p[0] = ('uminus', p[2])

def p_expression_group(p):
    '''expression : PARENTESIS_IZQ expression PARENTESIS_DER'''
    p[0] = p[2]

def p_expresion_numero(p):
    '''expression : NUMERO'''
    p[0] = ('number', p[1])

def p_expresion_cadena(p):
    '''expression : CADENA'''
    p[0] = ('string', p[1])

def p_expression_identificador(p):
    '''expression : IDENTIFICADOR'''
    # Análisis semántico simple: variable debe estar declarada
    if p[1] not in variables:
        print(f"Error semántico: variable '{p[1]}' no declarada")
    p[0] = ('id', p[1])

def p_expression_call(p):
    '''expression : IDENTIFICADOR PARENTESIS_IZQ args PARENTESIS_DER'''
    p[0] = ('call', p[1], p[3])

def p_args_multiple(p):
    '''args : args COMA expression'''
    p[0] = p[1] + [p[3]]

def p_args_single(p):
    '''args : expression'''
    p[0] = [p[1]]

def p_args_empty(p):
    '''args : '''
    p[0] = []

def p_error(p):
    if p:
        col = encontrar_columna(p.lexer.lexdata, p)
        msg = f"Error de sintaxis: token inesperado '{p.value}' (tipo: {p.type}) en la Fila {p.lineno}, columna {col}"
        raise SyntaxError(msg)
    else:
        raise SyntaxError("Error de sintaxis: final inesperado del archivo")

def pretty_print_ast(node, indent=0):
    """
    Imprime el AST de forma legible con indentación.
    
    Args:
        node: Nodo del AST (tupla, lista o valor)
        indent: Nivel de indentación actual
    
    Returns:
        String con la representación del AST
    """
    if isinstance(node, tuple):
        head = node[0]
        children = node[1:]
        result = "  " * indent + f"{head}:\n"
        for child in children:
            result += pretty_print_ast(child, indent + 1)
        return result
    elif isinstance(node, list):
        result = ""
        for item in node:
            result += pretty_print_ast(item, indent)
        return result
    else:
        return "  " * indent + repr(node) + "\n"

parser = yacc.yacc()
