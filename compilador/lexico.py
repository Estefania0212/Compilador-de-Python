import ply.lex as lex

# Palabras reservadas actualizadas para Python 3.12
reserved = {
    'False': 'FALSE',
    'None': 'NONE',
    'True': 'TRUE',
    'and': 'AND',
    'as': 'AS',
    'assert': 'ASSERT',
    'async': 'ASYNC',
    'await': 'AWAIT',
    'break': 'BREAK',
    'case': 'CASE',
    'class': 'CLASS',
    'continue': 'CONTINUE',
    'def': 'DEF',
    'del': 'DEL',
    'elif': 'ELIF',
    'else': 'ELSE',
    'except': 'EXCEPT',
    'finally': 'FINALLY',
    'for': 'FOR',
    'from': 'FROM',
    'global': 'GLOBAL',
    'if': 'IF',
    'import': 'IMPORT',
    'in': 'IN',
    'is': 'IS',
    'lambda': 'LAMBDA',
    'match': 'MATCH',
    'nonlocal': 'NONLOCAL',
    'not': 'NOT',
    'or': 'OR',
    'pass': 'PASS',
    'raise': 'RAISE',
    'return': 'RETURN',
    'try': 'TRY',
    'while': 'WHILE',
    'with': 'WITH',
    'yield': 'YIELD'
}

# Lista de tokens
tokens = [
    'IDENTIFICADOR', 'NUMERO', 'CADENA',
    # Operadores aritméticos
    'MAS', 'MENOS', 'POR', 'DIVIDIDO', 'MODULO', 'POTENCIA', 'DIVISION_ENTERA',
    # Operadores de comparación y asignación
    'IGUAL', 'DIFERENTE', 'MENOR', 'MENORIGUAL', 'MAYOR', 'MAYORIGUAL', 'ASIGNAR',
    # Delimitadores
    'PARENTESIS_IZQ', 'PARENTESIS_DER',
    'CORCHETE_IZQ', 'CORCHETE_DER',
    'LLAVE_IZQ', 'LLAVE_DER',
    'COMA', 'PUNTO', 'DOS_PUNTOS', 'PUNTO_COMA',
    # Símbolos y operadores adicionales
    'ARROBA',         # @
    'ALMOHADILLA',    # #
    'DOLAR',          # $
    'PORCENTAJE',     # %
    'AMPERSAND',      # &
    'BARRA_VERTICAL', # |
    'BACKSLASH',      # \
    'SLASH',          # /
    'ADMIRACION',     # !
    'INTERROGACION',  # ?
    'COMILLASIMPLE',  # '
    'COMILLADOBLE',   # "
    'MENOR_MENOR',    # <<
    'MAYOR_MAYOR',    # >>
    'FLECHA',         # ->
    'FLECHA_GORDA',   # =>
    'TILDE',          # ~
    'GUION_BAJO',     # _
    'PUNTO_PUNTO',    # ..
    'PUNTO_PUNTO_PUNTO', # ...
    'DOBLE_AMPERSAND',   # &&
    'DOBLE_BARRA',       # ||
    'DOBLE_PUNTO',       # ::
    'DOBLE_IGUAL',       # ==
    'ADMIGUAL',          # !=
    'MENOS_MAYOR',       # ->
    # Operadores compuestos
    'PORCENTAJE_IGUAL',  # %=
    'MAS_IGUAL',         # +=
    'MENOS_IGUAL',       # -=
    'POR_IGUAL',         # *=
    'DIVIDIDO_IGUAL',    # /=
    'AND_IGUAL',         # &=
    'OR_IGUAL',          # |=
    'XOR_IGUAL',         # ^=
    'DESPLAZA_IZQ_IGUAL',# <<=
    'DESPLAZA_DER_IGUAL',# >>=
    'MODULO_IGUAL',      # %=
    'PREGUNTA_DOS_PUNTOS', # ?:
    # Operadores bit a bit
    'AND_BIN', 'OR_BIN', 'XOR_BIN', 'NOT_BIN', 'DESPLAZA_IZQ', 'DESPLAZA_DER',
    # Incremento y decremento
    'INCREMENTO', 'DECREMENTO'
] + list(reserved.values())

# Expresiones regulares
# Operadores aritméticos
t_MAS             = r'\+'
t_MENOS           = r'-'
t_POR             = r'\*'
t_DIVIDIDO        = r'/'
t_MODULO          = r'%'
t_POTENCIA        = r'\*\*'
t_DIVISION_ENTERA = r'//'

# Operadores de comparación y asignación
t_IGUAL           = r'=='
t_DIFERENTE       = r'!='
t_MENORIGUAL      = r'<='
t_MAYORIGUAL      = r'>='
t_MENOR           = r'<'
t_MAYOR           = r'>'
t_ASIGNAR         = r'='

# Delimitadores
t_PARENTESIS_IZQ  = r'\('
t_PARENTESIS_DER  = r'\)'
t_CORCHETE_IZQ    = r'\['
t_CORCHETE_DER    = r'\]'
t_LLAVE_IZQ       = r'\{'
t_LLAVE_DER       = r'\}'
t_COMA            = r','
t_PUNTO           = r'\.'
t_DOS_PUNTOS      = r':'
t_PUNTO_COMA      = r';'

# Símbolos y operadores adicionales
t_ARROBA          = r'@'
t_ALMOHADILLA     = r'\#'
t_DOLAR           = r'\$'
t_PORCENTAJE      = r'%'
t_AMPERSAND       = r'&'
t_BARRA_VERTICAL  = r'\|'
t_BACKSLASH       = r'\\'
t_SLASH           = r'/'
t_ADMIRACION      = r'!'
t_INTERROGACION   = r'\?'
t_COMILLASIMPLE   = r'\''
t_COMILLADOBLE    = r'\"'
t_MENOR_MENOR     = r'<<'
t_MAYOR_MAYOR     = r'>>'
t_FLECHA          = r'->'
t_FLECHA_GORDA    = r'=>'
t_TILDE           = r'~'
t_GUION_BAJO      = r'_'
t_PUNTO_PUNTO     = r'\.\.'
t_PUNTO_PUNTO_PUNTO = r'\.\.\.'
t_DOBLE_AMPERSAND = r'&&'
t_DOBLE_BARRA     = r'\|\|'
t_DOBLE_PUNTO     = r'::'
t_DOBLE_IGUAL     = r'=='
t_ADMIGUAL        = r'!='
t_MENOS_MAYOR     = r'->'

# Operadores compuestos
t_PORCENTAJE_IGUAL = r'%='
t_MAS_IGUAL        = r'\+='
t_MENOS_IGUAL      = r'-='
t_POR_IGUAL        = r'\*='
t_DIVIDIDO_IGUAL   = r'/='
t_AND_IGUAL        = r'&='
t_OR_IGUAL         = r'\|='
t_XOR_IGUAL        = r'\^='
t_DESPLAZA_IZQ_IGUAL = r'<<='
t_DESPLAZA_DER_IGUAL = r'>>='
t_MODULO_IGUAL     = r'%='
t_PREGUNTA_DOS_PUNTOS = r'\?:'

# Operadores bit a bit
t_AND_BIN          = r'&'
t_OR_BIN           = r'\|'
t_XOR_BIN          = r'\^'
t_NOT_BIN          = r'~'
t_DESPLAZA_IZQ     = r'<<'
t_DESPLAZA_DER     = r'>>'

# Incremento y decremento
t_INCREMENTO       = r'\+\+'
t_DECREMENTO       = r'--'

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

def t_COMENTARIOS(t):
    r'\#.*'
    pass  # Ignorar comentarios

def t_CADENA(t):
    r'(\"([^\\\n]|(\\.))*?\")|(\'([^\\\n]|(\\.))*?\')'
    t.value = t.value[1:-1]  # Quitar comillas
    return t

def t_NUMERO(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_IDENTIFICADOR(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFICADOR')  # Verificar si es palabra reservada
    return t

def t_nuevalinea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    col = encontrar_columna(t.lexer.lexdata, t)
    msg = f"Error léxico: Carácter ilegal '{t.value[0]}' en la Fila {t.lineno}, Columna {col}"
    raise Exception(msg)

def encontrar_columna(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    return token.lexpos - last_cr

lexer = lex.lex()
