from expr import *
from constants import *

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
            elif expr_str[index] in OPS:
                new_op = expr_str[index]
                while (op_stack and
                    OP_PRECEDENCES[new_op] <= OP_PRECEDENCES[op_stack[-1]]):
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


class ParseExprException(Exception):
    """Thrown when a string cannot be parsed into an expression."""
    pass


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
