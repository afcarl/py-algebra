import unittest
from ..expr import *


class TestExpr(unittest.TestCase):
    """Tests for Expr class"""

    def test_expr_creation(self):
        """Test the init method of Expr"""
        # Node must have a value
        self.assertRaises(ExprException, Expr, None)
        self.assertRaises(ExprException, Expr, None, Expr(5))
        # Values can only be terminals or operators
        self.assertRaises(ExprException, Expr, '5')
        self.assertRaises(ExprException, Expr, 'a')
        # Operator must have operands
        for op in ['+', '*', '/', '^']:
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
        expr = Expr('+', [Expr(5), Expr(Symbol('yz'))])
        self.assertEqual('5 + yz', str(expr))

        expr = Expr('*', [Expr(Symbol('x')), Expr(8)])
        self.assertEqual('x * 8', str(expr))

        expr = Expr('+',
                [
                    Expr(5), Expr('*', [Expr(1), Expr(2)]),
                    Expr(Symbol('z'))
                ])
        self.assertEqual('5 + 1 * 2 + z', str(expr))


if __name__ == '__main__':
    unittest.main()
