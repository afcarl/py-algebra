import unittest

from py_algebra import *


class ExprTest(unittest.TestCase):
    """Test Expr class"""

    def test_set_op(self):
        expr = Expr()
        expr.set_op('+')
        self.assertEqual(expr.get_op(), '+')
        self.assertRaises(SetOperationException, expr.set_op, '*')

    def test_add_operand(self):
        expr = Expr()
        expr.add_operand(5)
        expr.add_operand(Symbol('x'))
        expr.add_operand(Expr())
        self.assertEqual(expr.num_operands, 3)

    def test_add_operands(self):
        expr = Expr()
        expr.add_operands([5, Symbol('x'), Expr()])
        self.assertEqual(expr.num_operands, 3)

    def test_equality_checking(self):
        expr1 = Expr('+', [5, Expr('*', [1, 2]), Symbol('z')])
        expr2 = Expr('+', [5, Expr('*', [1, 2]), Symbol('z')])
        self.assertEqual(expr1, expr2)

        expr1 = Expr('+', [5, Expr('*', [1, 2]), Symbol('z')])
        expr2 = Expr('+', [5, Expr('*', [1, 2])])
        self.assertNotEqual(expr1, expr2)

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
