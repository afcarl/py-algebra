from numbers import Number

class Expr():
    """
    An expression.  Is generally a node in a larger expression tree.

    A terminal is considered to be a Symbol or a number.
    (instance of numbers.Number). Examples: Symbol('x'), 5, 5.585, etc.

    An operator is a valid char from Expr.OPS.
    """
    OPS = ['+', '*', '^', '/']
    OP_NAMES = {'+': 'Add', '*': 'Mul', '^': 'Exp', '/': 'Div'}

    def __init__(self, value, operands=None):
        """
        Constructor for Expr.

        value: (a terminal or operator) - The value.  Must be one listed in OPS.
        operands: (list of Exprs) - The operands (children) of this expression.
        """
        if not value:
            raise ExprException('Node must have a value')
        if self.is_terminal(value):
            if operands==None:
                self.value = value
                self.operands = []
            else:
                raise ExprException(
                        'A node with a terminal value cannot have any'
                        'operands.')
        elif self.is_operator(value):
            # TODO(smilli): Maybe don't allow no operands when the value
            # is an operator
            if operands==None:
                raise ExprException(
                        'An expression with an operator as a value must have'
                        ' operands')
            self.value = value
            self.operands = []
            self.add_operands(operands)
        else:
            raise ExprException('Invalid value for expression node: %s' %
                    str(value))

    def __eq__(self, other):
        if (isinstance(other, self.__class__)
            and self.value == other.value
            and self.num_operands == other.num_operands):
            for operand, other_operand in zip(self.operands, other.operands):
                if operand != other_operand:
                    return False
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        if self.value:
            string = '%s(' % self.OP_NAMES[self.value]
        else:
            string = '('
        for index, operand in enumerate(self.operands):
            if index == len(self.operands) - 1:
                string += repr(operand)
            else:
                string += '%s, ' % repr(operand)
        string += ')'
        return string

    def __str__(self):
        string = ''
        for index, operand in enumerate(self.operands):
            if index == len(self.operands) - 1:
                string += str(operand)
            else:
                string += '%s %s ' % (str(operand), self.value)
        return string

    def is_operator(self, value=None):
        if value == None:
            value = self.value
        return value in self.OPS 

    def is_terminal(self, value=None):
        if value == None:
            value = self.value
        return isinstance(value, Symbol) or isinstance(value, Number)

    def add_operand(self, operand):
        if not self.is_operator():
            raise ExprException('This node\'s value is not an operator')
        if isinstance(operand, Expr):
            self.operands.append(operand)
        else:
            raise ExprException('Operand must be an expression')

    def add_operands(self, operands):
        """
        Convenience method for adding multiple operands at once.

        operands: (list) list of operands
        """
        if not self.is_operator():
            raise ExprException('This node\'s value is not an operator')
        if all([isinstance(operand, Expr) for operand in operands]):
            self.operands.extend(operands)
        else:
            raise ExprException('Operands must be expressions')

    @property
    def num_operands(self):
        return len(self.operands)


class ExprException(Exception):
    """Thrown when an error occurs when calling a method of an Expr."""
    pass


class Symbol():
    """An algebraic symbol like x, y, a, etc."""
    def __init__(self, symbol_name):
        self.symbol_name = symbol_name

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.symbol_name == other.symbol_name)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.symbol_name


class Fraction():
    def __init__(self, numer, denom):
        self.numer = numer
        self.denom = denom


class ParseExprException(Exception):
    """Thrown when a string cannot be parsed into an expression."""
    pass


def parse_str(expr_str):
    """Parses a string into an Expr object."""
    expr = parse_str_helper(expr_str)
    return flatten_expr(expr)


def parse_str_helper(expr_str):
    expr = Expr()
    index = 0
    while index < len(expr_str):
        if expr_str[index].isalpha():
            symbol_name = ''
            while index < len(expr_str) and expr_str[index].isalpha():
                symbol_name += expr_str[index]
                index += 1
            expr.add_operand(Symbol(symbol_name))
        elif expr_str[index].isdigit() or expr_str[index] == '.':
            num_string = ''
            while (index < len(expr_str) and
                (expr_str[index].isdigit() or expr_str[index] == '.')):
                num_string += expr_str[index]
                index += 1
            try:
                number = float(num_string)
                expr.add_operand(number)
            except ValueError:
                raise ParseExprException('Invalid number %s' % num_string)
        elif expr_str[index] == '(':
            close_paren_index = find_close_paren_index(expr_str, index)
            # check if * should be added before (
            if (index > 0 and
                (expr_str[index-1].isalpha()
                or expr_str[index-1].isdigit())):
                expr.set_op('*')
            expr.add_operand(parse_str_helper(
                expr_str[(index+1):close_paren_index]))
            index = close_paren_index + 1
            # check if * should be added after )
            if (index < len(expr_str) and
                (expr_str[index].isalpha()
                or expr_str[index].isdigit()
                or expr_str[index] == '(')):
                expr.set_op('*')
            continue
        elif expr_str[index] in Expr.OPS:
            if expr.is_op_set:
                # check to make sure not malformed
                old_expr = expr
                expr = Expr(expr_str[index])
                expr.add_operand(old_expr)
            else:
                expr.set_op(expr_str[index])
            expr.add_operand(parse_str_helper(expr_str[(index+1):]))
            return expr
        else:
            # if space just increment index
            index += 1
    return expr


def find_close_paren_index(expr_str, open_paren_ind):
    """
    Finds the index of the closing paranthesees in expr_str.

    Finds the index of the close paren corresponding to the open paren at
    the index provided in expr_str.

    expr_str: (string) The string to search in
    open_paren_ind: (int) The index of the open paren to match with
    """
    stack = []
    stack.append(expr_str[open_paren_ind])
    index = open_paren_ind
    while stack:
        index += 1
        if (index >= len(expr_str)):
            raise ParseExprException('Malformed paranthesees')
        elif (expr_str[index] == '('):
            stack.append(expr_str[index])
        elif (expr_str[index] == ')'):
            stack.pop()
    return index


def flatten_expr(expr):
    """
    Flattens an Expr object.

    At the end of this there should be no Expr objects without operations
    set.

    expr: (Expr object) - the expression to flatten
    """
    if isinstance(expr, Expr):
        for index, operand in enumerate(expr.operands):
            if not isinstance(operand, Expr):
                continue
            elif not operand.is_op_set() and operand.num_operands == 1:
                # Flatten numbers and symbols
                expr.operands[index] = flatten_expr(operand.operands[0])
            elif expr.get_op() == operand.get_op():
                expr.operands.remove(operand)
                operand = flatten_expr(operand)
                expr.add_operands(operand.operands)
            else:
                flatten_expr(operand)
    return expr

def simplify(expr):
    """
    Simplifies an expression by combining operands of the same type.

    Does not modify the expression passed in.
    Returns a new expression instead.

    Parameters:
    expr: (Expr object) - the expression to simplify

    Returns:
    new_expr: (Expr object) - the simplified expression
    """
    pass

def substitute(expr, var, new_var):
    """
    Substitutes a new number, variable, or expr in the expression.

    This does not simplify the expression.  It simply replaces all occurences
    of var with new_var.

    Parameters:
    expr: (Expr object) - the expression to simplify
    var: (Symbol object or string) - either the string name of the symbol to
        replace or a Symbol object with that string name.  I.e. passing in
        Symbol('x') is equivalent to passing in 'x'.
    new_var:
        -Type: Anything valid to place in an expression -- a number,
        Symbol object, string name for Symbol, Expr object, etc
        -Description: What to replace var with in the expression

    Returns:
    new_expr: (Expr object) - a new expression that is the result of performing
        the substitution on the given expr
    """
    pass

def evalute(expr, var, new_var):
    """
    Evaluates the expression by replacing the given variable with the new value.

    This is equivalent to using substitute and then simplify.

    Parameters:
    expr: (Expr object) - the expression to simplify
    var: (Symbol object or string) - either the string name of the symbol to
        replace or a Symbol object with that string name.  I.e. passing in
        Symbol('x') is equivalent to passing in 'x'.
    new_var:
        -Type: Anything valid to place in an expression -- a number,
        Symbol object, string name for Symbol, Expr object, etc
        -Description: What to replace var with in the expression

    Returns:
    new_expr: (Expr object) - a new expression that is the result of evaluating
        the given expr
    """
    pass
