class ErroSemantico(Exception):
    pass

BUILTIN_FUNCTIONS = {
    "print": ("function", ["value"]), 
    "len": ("function", ["string"]),   
    "input": ("function", []),         

}

class TablaSimbolos:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def declarar(self, name, value=None):
        if name in self.symbols:
            raise ErroSemantico(f"Variable '{name}' ya declarada en este ámbito")
        self.symbols[name] = value

    def asignar(self, name, value=None):
        if name in self.symbols:
            self.symbols[name] = value
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise ErroSemantico(f"Variable '{name}' no declarada")

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.lookup(name)
        elif name in BUILTIN_FUNCTIONS:
            return BUILTIN_FUNCTIONS[name]
        else:
            raise ErroSemantico(f"Variable '{name}' no declarada")

def analizar(node, symtab=None):
    if symtab is None:
        symtab = TablaSimbolos()

    nodetype = node[0]

    if nodetype == 'program':
        for stmt in node[1]:
            analizar(stmt, symtab)

    elif nodetype == 'assign':
        varname = node[1]
        expr = node[2]
        value = analizar(expr, symtab)
        if varname not in symtab.symbols:
            symtab.declarar(varname, value)
        else:
            symtab.asignar(varname, value)
        return value

    elif nodetype == 'expr':
        return analizar(node[1], symtab)

    elif nodetype == 'number':
        return 'number'

    elif nodetype == 'string':
        return 'string'

    elif nodetype == 'id':
        return symtab.lookup(node[1])

    elif nodetype == 'binop':
        left = analizar(node[2], symtab)
        right = analizar(node[3], symtab)
        op = node[1]
        # Suma
        if op == '+':
            if left == 'number' and right == 'number':
                return 'number'
            elif left == 'string' and right == 'string':
                return 'string'
            else:
                raise ErroSemantico(f"Error semántico: no se puede sumar {left} y {right}")
        # Resta, división, módulo
        elif op in ('-', '/', '%'):
            if left == 'number' and right == 'number':
                return 'number'
            else:
                raise ErroSemantico(f"Error semántico: el operador '{op}' solo se puede aplicar entre números")
        # Multiplicación
        elif op == '*':
            if left == 'number' and right == 'number':
                return 'number'
            elif (left == 'string' and right == 'number') or (left == 'number' and right == 'string'):
                return 'string'
            else:
                raise ErroSemantico(f"Error semántico: el operador '*' solo se puede aplicar entre números o string y número")
        # Comparaciones
        elif op in ('==', '!=', '<', '<=', '>', '>='):
            if left == right:
                return 'number'  # Consideramos booleano como número (0/1)
            else:
                raise ErroSemantico(f"Error semántico: comparación entre tipos incompatibles: {left} y {right}")
        # Lógicos
        elif op in ('and', 'or'):
            if left == 'number' and right == 'number':
                return 'number'
            else:
                raise ErroSemantico(f"Error semántico: el operador lógico '{op}' solo se puede aplicar entre números (0/1)")
        else:
            raise ErroSemantico(f"Operador no soportado: {op}")

    elif nodetype == 'uminus':
        val = analizar(node[1], symtab)
        if val != 'number':
            raise ErroSemantico("Error semántico: el operador unario '-' solo se puede aplicar a números")
        return 'number'

    elif nodetype == 'if':
        cond = analizar(node[1], symtab)
        if cond != 'number':
            raise ErroSemantico("Error semántico: la condición de 'if' debe ser numérica (0/1)")
        analizar(('program', node[2]), TablaSimbolos(symtab))
        if node[3]:
            analizar(('program', node[3]), TablaSimbolos(symtab))

    elif nodetype == 'while':
        cond = analizar(node[1], symtab)
        if cond != 'number':
            raise ErroSemantico("Error semántico: la condición de 'while' debe ser numérica (0/1)")
        analizar(('program', node[2]), TablaSimbolos(symtab))

    elif nodetype == 'for':
        varname = node[1]
        iterable = analizar(node[2], symtab)
        if iterable != 'string':
            raise ErroSemantico(f"Error semántico: el bucle 'for' espera un iterable de tipo string, se encontró {iterable}")
        # Crear un nuevo ámbito para el bucle
        loop_symtab = TablaSimbolos(symtab)
        # Declarar la variable de iteración como string (cada carácter)
        loop_symtab.declarar(varname, 'string')
        analizar(('program', node[3]), loop_symtab)

    elif nodetype == 'funcdef':
        fname = node[1]
        params = node[2]
        body = node[3]
        # Declarar función en la tabla de símbolos
        symtab.declarar(fname, ('function', params))
        # Crear un nuevo ámbito para los parámetros
        func_symtab = TablaSimbolos(symtab)
        for param in params:
            func_symtab.declarar(param, 'number')  # Suponemos tipo number por simplicidad
        analizar(('program', body), func_symtab)

    elif nodetype == 'call':
        fname = node[1]
        args = node[2]
        
        # Verificar si es una función built-in
        if fname in BUILTIN_FUNCTIONS:
            func = BUILTIN_FUNCTIONS[fname]
            params = func[1]
        else:
            # Si no es built-in, buscar en la tabla de símbolos
            func = symtab.lookup(fname)
            if func[0] != 'function':
                raise ErroSemantico(f"Error semántico: '{fname}' no es una función")
            params = func[1]
            
        # Verificar número de argumentos
        if len(args) != len(params):
            raise ErroSemantico(f"Error semántico: la función '{fname}' espera {len(params)} argumentos, se pasaron {len(args)}")
            
        # Verificar tipos de argumentos
        arg_types = [analizar(arg, symtab) for arg in args]
        
        # Retornar tipo según la función
        if fname == "len":
            return 'number'  # len retorna un número
        elif fname == "input":
            return 'string'  # input retorna un string
        else:
            return 'number'  # Por defecto asumimos que las funciones retornan número

    else:
        raise ErroSemantico(f"Error semántico: nodo AST desconocido: {nodetype}")
