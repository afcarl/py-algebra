import unittest

from py_algebra import *

class ParseExpressionTest(unittest.TestCase):
    """Test parsing expression strings into Expr objects."""

    def test_parse_str(self):
        expr_str = '5'
        expr = Expr(None, 5)
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '5 + 3'
        expr.set_op('+')
        expr.add_operand(3)
        self.assertEqual(parse_str(expr_str), expr)

        expr_str = '5 + x'
        expr = Expr('+', [5, Symbol('x')])
        self.assertEqual(parse_str(expr_str), expr)

    def test_flatten(self):
        expr = Expr('+', [Expr(None, 5), Expr(None, 3)])
        flattened_expr = Expr('+', [5, 3])
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
