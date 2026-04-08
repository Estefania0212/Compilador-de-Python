class InterpreterError(Exception):
    pass

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise InterpreterError(f"Variable '{name}' no definida")

    def set(self, name, value):
        self.vars[name] = value

def interprete(node, env=None, output=None):
    if env is None:
        env = Environment()
    if output is None:
        output = []

    nodetype = node[0]

    if nodetype == 'program':
        for stmt in node[1]:
            interprete(stmt, env, output)
        return output

    elif nodetype == 'assign':
        varname = node[1]
        value = interprete(node[2], env, output)
        env.set(varname, value)
        return value

    elif nodetype == 'expr':
        return interprete(node[1], env, output)

    elif nodetype == 'number':
        return node[1]

    elif nodetype == 'string':
        return node[1]

    elif nodetype == 'id':
        return env.get(node[1])

    elif nodetype == 'binop':
        op = node[1]
        left = interprete(node[2], env, output)
        right = interprete(node[3], env, output)
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '%':
            return left % right
        elif op == '==':
            return int(left == right)
        elif op == '!=':
            return int(left != right)
        elif op == '<':
            return int(left < right)
        elif op == '<=':
            return int(left <= right)
        elif op == '>':
            return int(left > right)
        elif op == '>=':
            return int(left >= right)
        else:
            raise InterpreterError(f"Operador no soportado: {op}")

    elif nodetype == 'uminus':
        val = interprete(node[1], env, output)
        return -val

    elif nodetype == 'call':
        fname = node[1]
        args = [interprete(arg, env, output) for arg in node[2]]
        if fname == 'print':
            msg = " ".join(str(a) for a in args)
            output.append(msg)
            return None
        else:
            raise InterpreterError(f"Llamada a función desconocida: {fname}")

    elif nodetype == 'if':
        cond = interprete(node[1], env, output)
        if cond:
            interprete(('program', node[2]), Environment(env), output)
        elif node[3]:
            interprete(('program', node[3]), Environment(env), output)

    elif nodetype == 'while':
        while interprete(node[1], env, output):
            interprete(('program', node[2]), Environment(env), output)

    else:
        raise InterpreterError(f"Nodo AST desconocido: {nodetype}")