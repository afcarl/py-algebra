from numbers import Number
from collections import Counter
from constants import *


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
        string = '%s(' % OP_NAMES[self.value]
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
        return value in OPS

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
