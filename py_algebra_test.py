import unittest

from py_algebra import *


class ExprTest(unittest.TestCase):
    """Tests for Expr class"""

    def test_expr_creation(self):
        """Test the init method of Expr"""
        # Values can only be terminals or operators
        self.assertRaises(ExprException, Expr, '5')
        self.assertRaises(ExprException, Expr, 'a')
        # Operator must have operands
        for op in Expr.OPS:
            self.assertRaises(ExprException, Expr, op)
        # A node with terminal value must be a leaf node
        self.assertRaises(ExprException, Expr, 5, [Expr(8), Expr(9)])

        expr = Expr(6)
        self.assertEqual(expr.value, 6)
        self.assertEqual(expr.operands, [])

        expr = Expr('+', [Expr(6), Expr(Symbol('y'))])
        self.assertEqual(expr.value, '+')
        self.assertEqual(expr.operands, [Expr(6), Expr(Symbol('y'))])

    def test_add_operand(self):
        # An expression w/o an operator as value cannot have operands
        expr = Expr(6)
        self.assertRaises(ExprException, expr.add_operand, Expr(6))
        self.assertRaises(ExprException, expr.add_operand, Expr(Symbol('x')))

        # Operands must be expressions
        expr = Expr('+', [Expr(6)])
        with self.assertRaises(ExprException,
                msg='Operand must be an expression'):
            expr.add_operand(5)
        with self.assertRaises(ExprException,
                msg='Operand must be an expression'):
            expr.add_operand(5)
            expr.add_operand(Symbol('x'))
        expr.add_operand(Expr(5))
        expr.add_operand(Expr(Symbol('x')))
        self.assertEqual(expr.num_operands, 3)

    def test_add_operands(self):
        # An expression w/o an operator as value cannot have operands
        expr = Expr(6)
        self.assertRaises(ExprException, expr.add_operand,
                [Expr(6), Expr(Symbol('x'))])

        # Operands must be expressions
        expr = Expr('*', [Expr(7)])
        with self.assertRaises(ExprException,
                msg='Operands must be expressions'):
            expr.add_operands([Expr(7), 5, Symbol('x')])
        expr.add_operands([Expr(7), Expr(Symbol('x'))])
        self.assertEqual(expr.num_operands, 3)

    def test_equality_checking(self):
        expr1 = Expr('+', [
            Expr(5), Expr('*', [Expr(1), Expr(2)]), Expr(Symbol('z'))])
        expr2 = Expr('+', [
            Expr(5), Expr('*', [Expr(1), Expr(2)]), Expr(Symbol('z'))])
        self.assertEqual(expr1, expr2)

        expr1 = Expr('+', [
            Expr(5), Expr('*', [Expr(1), Expr(2)]), Expr(Symbol('z'))])
        expr2 = Expr('+', [
            Expr(5), Expr('*', [Expr(1), Expr(2)])])
        self.assertNotEqual(expr1, expr2)

    def test_expr_to_string(self):
        expr = Expr('+', [5, Symbol('yz')])
        self.assertEqual('5 + yz', str(expr))

        expr = Expr('*', [Symbol('x'), 8])
        self.assertEqual('x * 8', str(expr))

        expr = Expr('+', [5, Expr('*', [1, 2]), Symbol('z')])
        self.assertEqual('5 + 1 * 2 + z', str(expr))

class ParseExpressionTest(unittest.TestCase):
    """Test parsing expression strings into Expr objects."""

    def test_parse_str(self):
        expr_str = '5'
        expr = Expr(None, 5)
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '5.3 + 385'
        expr = Expr('+', [5.3, 385])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '.68 * 2.385'
        expr = Expr('*', [.68, 2.385])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '5 + x'
        expr = Expr('+', [5, Symbol('x')])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = 'y + x'
        expr = Expr('+', [Symbol('y'), Symbol('x')])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = 'y + x * 5'
        expr = Expr('+', [Symbol('y'), Expr('*', [Symbol('x'), 5])])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = 'y*x'
        expr = Expr('*', [Symbol('y'), Symbol('x')])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = 'y * x'
        expr = Expr('*', [Symbol('y'), Symbol('x')])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '5 + x + 3'
        expr = Expr('+', [5, Symbol('x'), 3])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '5 * x * 3'
        expr = Expr('*', [5, Symbol('x'), 3])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '5 * x * 3 + y'
        expr = Expr('*', [5, Symbol('x'), Expr('+', [3, Symbol('y')])])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '(.63 + x) * 5'
        expr = Expr('*', [Expr('+', [.63, Symbol('x')]), 5])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '(.63 + x) + 5'
        expr = Expr('+', [Expr('+', [.63, Symbol('x')]), 5])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '(.63 + x)(7 + y)'
        expr = Expr('*', [Expr('+',[.63, Symbol('x')]), Expr('+', [7, Symbol('y')])])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '5(.63 + x)'
        expr = Expr('*', [5, Expr('+',[.63, Symbol('x')])])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '(5)(.63 + x)'
        expr = Expr('*', [5, Expr('+',[.63, Symbol('x')])])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '(.63 + x)5'
        expr = Expr('*', [Expr('+',[.63, Symbol('x')]), 5])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '(.63 + x)(5)'
        expr = Expr('*', [Expr('+',[.63, Symbol('x')]), 5])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = 'x(.63 + x)'
        expr = Expr('*', [Symbol('x'), Expr('+',[.63, Symbol('x')])])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '(x)(.63 + x)'
        expr = Expr('*', [Symbol('x'), Expr('+',[.63, Symbol('x')])])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '(.63 + x)x'
        expr = Expr('*', [Expr('+',[.63, Symbol('x')]), Symbol('x')])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '(.63 + x)(x)'
        expr = Expr('*', [Expr('+',[.63, Symbol('x')]), Symbol('x')])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '(.63 + x)x + y'
        expr = Expr('+',
                [
                    Expr('*',
                    [
                        Expr('+',[.63, Symbol('x')]),
                        Symbol('x')
                    ]),
                    Symbol('y')
                ])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '5 * x + 2 * y'
        expr = Expr('+',
                [
                    Expr('*',
                        [5, Symbol('x')]),
                    Expr('*',
                        [2, Symbol('y')])
                ])
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '5 + x * y + 8'
        expr = Expr('+',
                [   5,
                    Expr('*',
                        [Symbol('x'), Symbol('y')]),
                    8
                ])
        self.assertEqual(parse_str(expr_str), expr)

    def test_flatten_expr(self):
        expr = Expr('+', [Expr(None, 5), Expr(None, 3)])
        flattened_expr = Expr('+', [5, 3])
        self.assertEqual(flatten_expr(expr), flattened_expr)

        expr = Expr('+', [Expr(None, Symbol('x')), Expr(None, Symbol('y'))])
        flattened_expr = Expr('+', [Symbol('x'), Symbol('y')])
        self.assertEqual(flatten_expr(expr), flattened_expr)

        expr = Expr('*', [
            Expr('+', [Expr(None, .63), Expr(None, Symbol('x'))]), 5])
        flattened_expr = Expr('*', [Expr('+', [.63, Symbol('x')]), 5])
        self.assertEqual(flatten_expr(expr), flattened_expr)

    def test_find_close_paren_index(self):
        expr_str = '5 * (4 + 6)'
        self.assertEqual(find_close_paren_index(expr_str, 4), 10)

        expr_str = '(((h)))'
        self.assertEqual(find_close_paren_index(expr_str, 0), 6)
        self.assertEqual(find_close_paren_index(expr_str, 1), 5)
        self.assertEqual(find_close_paren_index(expr_str, 2), 4)


if __name__ == '__main__':
    unittest.main()
