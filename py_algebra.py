from numbers import Number
from collections import Counter

_OPS = ['+', '*', '^', '/']
_OP_PRECEDENCES = {'+': 1, '*': 2, '/': 2, '^': 3, '(': 0}
_OP_NAMES = {'+': 'Add', '*': 'Mul', '^': 'Exp', '/': 'Div'}

class Expr():
    """
    An expression.  Is generally a node in a larger expression tree.

    A terminal is considered to be a Symbol or a number.
    (instance of numbers.Number). Examples: Symbol('x'), 5, 5.585, etc.

    An operator is a valid char from Expr.OPS.
    """

    def __init__(self, value, operands=None):
        """
        Constructor for Expr.

        value: (a terminal or operator) - The value.  Must be one listed in OPS.
        operands: (list of Exprs) - The operands (children) of this expression.
        """
        if not value:
            raise ExprException('Node must have a value')
        if self.is_terminal(value):
            if not operands:
                self.value = value
                self.operands = []
            else:
                raise ExprException(
                        'A node with a terminal value cannot have any'
                        'operands.')
        elif self.is_operator(value):
            # TODO(smilli): Maybe don't allow no operands when the value
            # is an operator
            if not operands:
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
                and self.value == other.value):
            return Counter(self.operands) == Counter(other.operands)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        if not self.operands:
            return repr(self.value)
        string = '%s(' % _OP_NAMES[self.value]
        for index, operand in enumerate(self.operands):
            if index == len(self.operands) - 1:
                string += repr(operand)
            else:
                string += '%s, ' % repr(operand)
        string += ')'
        return string

    def __str__(self):
        if not self.operands:
            return str(self.value)
        string = ''
        for index, operand in enumerate(self.operands):
            if index == len(self.operands) - 1:
                string += str(operand)
            else:
                string += '%s %s ' % (str(operand), self.value)
        return string

    def __hash__(self):
        # The value of this hash will change when the obj changes
        # Should only currently be used in __eq__
        # TODO(smilli): Find better way to do this
        if not self.operands:
            return hash(self.value)
        hash_value = hash(self.value)
        for operand in self.operands:
            hash_value ^= hash(operand)
        return hash_value

    def is_operator(self, value=None):
        if value == None:
            value = self.value
        return value in _OPS

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

    def __hash__(self):
        return hash(self.symbol_name)

    def __repr__(self):
        return self.symbol_name


class Fraction():
    def __init__(self, numer, denom):
        self.numer = numer
        self.denom = denom


class ParseExprException(Exception):
    """Thrown when a string cannot be parsed into an expression."""
    pass


class Parser():
    """Class that wraps methods related to parsing"""

    @classmethod
    def parse(cls, expr_str):
        """Parses a string into an Expr object."""
        expr_str = expr_str.replace(' ', '')
        expr = cls._parse_helper(expr_str)
        expr = flatten_expr(expr)
        return expr

    @classmethod
    def _parse_helper(cls, expr_str):
        """
        Converts expression string to Expr object.

        Uses Djikstra's Shunting Yard algorithm.
        """
        output = []
        op_stack = []
        index = 0
        while index < len(expr_str):
            if expr_str[index].isalpha():
                symbol_name = ''
                while index < len(expr_str) and expr_str[index].isalpha():
                    symbol_name += expr_str[index]
                    index += 1
                output.append(Expr(Symbol(symbol_name)))
            elif expr_str[index].isdigit() or expr_str[index] == '.':
                num_string = ''
                while (index < len(expr_str) and
                    (expr_str[index].isdigit() or expr_str[index] == '.')):
                    num_string += expr_str[index]
                    index += 1
                try:
                    number = float(num_string)
                    output.append(Expr(number))
                except ValueError:
                    raise ParseExprException('Invalid number %s' % num_string)
            elif expr_str[index] == '(':
                op_stack.append(expr_str[index])
                index += 1
            elif expr_str[index] == ')':
                while op_stack and op_stack[-1] != '(':
                    cls._pop_oper(output, op_stack)
                if not op_stack:
                    raise ParseExprException('Mismatched parentheses')
                op_stack.pop() # pop the '('
                index += 1
            elif expr_str[index] in _OPS:
                new_op = expr_str[index]
                while (op_stack and
                    _OP_PRECEDENCES[new_op] <= _OP_PRECEDENCES[op_stack[-1]]):
                        cls._pop_oper(output, op_stack)
                op_stack.append(new_op)
                index += 1
        while op_stack:
            if op_stack[-1] == '(':
                raise ParseExprException('Mismatched parentheses')
            cls._pop_oper(output, op_stack)
        if len(output) > 1:
            raise ParseExprException('Malformed expression')
        return output[0]

    @classmethod
    def _pop_oper(cls, output, op_stack):
        """Pops an op off the stack and applies it to the operands in the output"""
        op = op_stack.pop()
        operand2 = output.pop()
        operand1 = output.pop()
        output.append(Expr(op, [operand1, operand2]))


def flatten_expr(expr):
    """
    Flattens an Expr object.

    At the end of this there should be no operators that have the same
    operator as a child.  For example no '+' should have a '+' as a child.

    expr: (Expr object) - the expression to flatten
    """
    # TODO(smilli): Still need to implement this for '/', '^'
    if not expr.operands:
        return expr
    for index, operand in enumerate(expr.operands):
        operand = flatten_expr(operand)
        if operand.value == expr.value:
            expr.operands.remove(operand)
            expr.add_operands(operand.operands)
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
    of var with new_var.  It returns a new expression and does not modify expr.

    Parameters:
    expr: (Expr object) - the expression to substitute new_var in 
    var: (Symbol object or string) - either the string name of the symbol to
        replace or a Symbol object with that string name.  I.e. passing in
        Symbol('x') is equivalent to passing in 'x'.
    new_var:
        (a number, Symbol object, string name for Symbol, Expr object)
        - what to replace var with in the expression

    Returns:
    new_expr: (Expr object) - a new expression that is the result of performing
        the substitution on the given expr
    """
    if not isinstance(var, Symbol):
        var = Symbol(var)
    if not isinstance(new_var, (Number, Symbol, Expr)):
        new_var = Symbol(new_var)
    if not isinstance(new_var, Expr):
        new_var = Expr(new_var)
    return _substitute_helper(expr, var, new_var)


def _substitute_helper(expr, var, new_var_expr):
    """
    Helper method for substitute.

    Parameters:
    expr: (Expr object) - the expression to subtitute new_expr in
    var: (Symbol object or string) - the string name or symbol to replace
    new_var_expr: (Expr object) - the expression that will replace ones
        that have var as the value
    """
    if not expr.operands and expr.value == var:
        return new_var_expr
    operands = [_substitute_helper(operand, var, new_var_expr)
        for operand in expr.operands]
    return Expr(expr.value, operands)


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
