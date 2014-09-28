class Expr():
    """An expression."""
    OPS = ['+', '*']
    OP_NAMES = {'+': 'Add', '*': 'Mul'}

    def __init__(self, op=None, operands=None):
        """
        Constructor for Expr.

        op: (char) The operation.  Must be one listed in OPS.
        operands: (symbol / number or list of symbols and numbers) The
            operands of this expression.
        """
        if not operands:
            self._operands = []
        elif isinstance(operands, list):
            self._operands = operands
        else:
            self._operands = [operands]
        if op and op not in self.OPS:
            raise SetOperationException('Invalid operation')
        self._op = op

    def __eq__(self, other):
        if isinstance(other, self.__class__) and self._op == other._op:
            for operand, other_operand in zip(self._operands, other._operands):
                if operand != other_operand:
                    return False
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        if self._op:
            string = '%s(' % self.OP_NAMES[self._op]
        else:
            string = '('
        for index, operand in enumerate(self._operands):
            if index == len(self._operands) - 1:
                string += repr(operand)
            else:
                string += '%s, ' % repr(operand)
        string += ')'
        return string

    def is_op_set(self):
        """Returns True if the operation is set."""
        return bool(self._op)

    def set_op(self, op):
        """
        Sets the operation of this expression if previously unset.

        Throws:
            SetOperationException when the operation is already set or is invalid
        """
        if self._op:
            raise SetOperationException('Operation already set on expression')
        if op not in self.OPS:
            raise SetOperationException('Invalid operation')
        if op == '-':
            self._op = '+'
        self._op = op

    def get_op(self):
        return self._op

    def add_operand(self, operand):
        self._operands.append(operand)

    def add_operands(self, operands):
        """
        Convenience method for adding multiple operands at once.

        operands: (list) list of operands
        """
        self._operands.extend(operands)

    @property
    def num_operands(self):
        return len(self._operands)


class SetOperationException(Exception):
    """Thrown when an error occurs when setting the op of an expression."""
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


class ParseExpressionException(Exception):
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
                raise ParseExpressionException('Invalid number %s' % num_string)
        elif expr_str[index] == '(':
            close_paren_index = find_close_paren_index(expr_str, 0)
            # check if * should be added before
            expr.add_operand(parse_str_helper(
                expr_str[(index+1):close_paren_index]))
            # check if * should be added after
            index = close_paren_index + 1
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
            raise ParseExpressionException('Malformed paranthesees')
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
        for index, operand in enumerate(expr._operands):
            if not isinstance(operand, Expr):
                continue
            elif not operand.is_op_set() and operand.num_operands == 1:
                # Flatten numbers and symbols
                expr._operands[index] = flatten_expr(operand._operands[0])
            elif expr.get_op() == operand.get_op():
                expr._operands.remove(operand)
                operand = flatten_expr(operand)
                expr.add_operands(operand._operands)
            else:
                flatten_expr(operand)
    return expr
