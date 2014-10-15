import unittest

from py_algebra import *


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

class TestParse(unittest.TestCase):
    """Test parsing expression strings into Expr objects."""

    def test_parse(self):
        expr_str = '5'
        expr = Expr(5)
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '5.3 + 385'
        expr = Expr('+', [Expr(5.3), Expr(385)])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '.68 * 2.385'
        expr = Expr('*', [Expr(.68), Expr(2.385)])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '5 + x'
        expr = Expr('+', [Expr(5), Expr(Symbol('x'))])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = 'y + x'
        expr = Expr('+', [Expr(Symbol('y')), Expr(Symbol('x'))])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = 'y + x * 5'
        expr = Expr('+', [
            Expr(Symbol('y')),
            Expr('*', [
                Expr(Symbol('x')),
                Expr(5)
            ])
        ])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = 'y*x'
        expr = Expr('*', [Expr(Symbol('y')), Expr(Symbol('x'))])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = 'y * x'
        expr = Expr('*', [Expr(Symbol('y')), Expr(Symbol('x'))])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '5 + x + 3'
        expr = Expr('+', [Expr(5), Expr(Symbol('x')), Expr(3)])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '5 * x * 3'
        expr = Expr('*', [Expr(5), Expr(Symbol('x')), Expr(3)])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '5 * x * 3 + y'
        expr = Expr('+', [
            Expr(Symbol('y')),
            Expr('*', [
                Expr(5),
                Expr(Symbol('x')),
                Expr(3)
            ])
        ])
        expr = self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '(.63 + x) * 5'
        expr = Expr('*', [
            Expr('+', [Expr(.63), Expr(Symbol('x'))]),
            Expr(5)
        ])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '(.63 + x) + 5'
        expr = Expr('+', [Expr(.63), Expr(Symbol('x')), Expr(5)])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '(.63 + x) * (7 + y)'
        expr = Expr('*', [
            Expr('+',[
                Expr(.63),
                Expr(Symbol('x'))
            ]),
            Expr('+', [
                Expr(7),
                Expr(Symbol('y'))
            ])
        ])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '5 * (.63 + x)'
        expr = Expr('*', [
            Expr(5),
            Expr('+',[
                Expr(.63),
                Expr(Symbol('x'))
            ])
        ])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '(5) * (.63 + x)'
        expr = Expr('*', [
            Expr(5),
            Expr('+',[
                Expr(.63),
                Expr(Symbol('x'))
            ])
        ])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '(.63 + x) * 5'
        expr = Expr('*', [
            Expr('+',[
                Expr(.63),
                Expr(Symbol('x'))
            ]),
            Expr(5)
        ])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '(.63 + x) * (5)'
        expr = Expr('*', [
            Expr('+',[Expr(.63), Expr(Symbol('x'))]),
            Expr(5)
        ])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = 'x * (.63 + x)'
        expr = Expr('*', [
            Expr(Symbol('x')),
            Expr('+',[
                Expr(.63),
                Expr(Symbol('x'))
            ])
        ])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '(x) * (.63 + x)'
        expr = Expr('*', [
            Expr(Symbol('x')),
            Expr('+', [Expr(.63), Expr(Symbol('x'))])
        ])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '(.63 + x) * x'
        expr = Expr('*', [
            Expr('+',[Expr(.63), Expr(Symbol('x'))]),
            Expr(Symbol('x'))
        ])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '(.63 + x) * (x)'
        expr = Expr('*', [
            Expr('+',[Expr(.63), Expr(Symbol('x'))]),
            Expr(Symbol('x'))
        ])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '(.63 + x) * x + y'
        expr = Expr('+', [
            Expr('*',
            [
                Expr('+',[Expr(.63), Expr(Symbol('x'))]),
                Expr(Symbol('x'))
            ]),
            Expr(Symbol('y'))
        ])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '5 * x + 2 * y'
        expr = Expr('+', [
            Expr('*',
                [Expr(5), Expr(Symbol('x'))]),
            Expr('*',
                [Expr(2), Expr(Symbol('y'))])
        ])
        self.assertEqual(Parser.parse(expr_str), expr)

        expr_str = '5 + x * y + 8'
        expr = Expr('+', [
            Expr(5),
            Expr('*',[Expr(Symbol('x')), Expr(Symbol('y'))]),
            Expr(8)
        ])
        self.assertEqual(Parser.parse(expr_str), expr)

    def test_flatten_expr(self):
        expr = Expr('+', [
            Expr('+', [Expr(Symbol('x')), Expr(3)]),
            Expr(Symbol('z'))
        ])
        flattened_expr = Expr('+', [
            Expr(Symbol('x')),
            Expr(3),
            Expr(Symbol('z'))
        ])
        self.assertEqual(flatten_expr(expr), flattened_expr)

        expr = Expr('*', [
            Expr('*', [Expr(Symbol('x')), Expr(3)]),
            Expr(Symbol('z'))
        ])
        flattened_expr = Expr('*', [
            Expr(Symbol('x')),
            Expr(3),
            Expr(Symbol('z'))
        ])
        self.assertEqual(flatten_expr(expr), flattened_expr)

        expr = Expr('*', [
            Expr('+', [Expr(Symbol('x')), Expr(3)]),
            Expr(Symbol('z'))
        ])
        self.assertEqual(flatten_expr(expr), expr)

        expr = Expr('+', [
            Expr('*', [Expr(Symbol('x')), Expr(3)]),
            Expr(Symbol('z'))
        ])
        self.assertEqual(flatten_expr(expr), expr)


class TestOperations(unittest.TestCase):

    def test_substitute(self):
        expr = Expr(Symbol('x'))
        substituted = substitute(expr, Symbol('x'), Symbol('y'))
        self.assertEqual(substituted, Expr(Symbol('y')))

        expr = Expr(Symbol('x'))
        substituted = substitute(expr, Symbol('x'), 'y')
        self.assertEqual(substituted, Expr(Symbol('y')))

        expr = Expr(Symbol('x'))
        substituted = substitute(expr, 'x', 'y')
        self.assertEqual(substituted, Expr(Symbol('y')))

        expr = Expr(Symbol('x'))
        substituted = substitute(expr, 'x', 2)
        self.assertEqual(substituted, Expr(2))

        expr = Expr(Symbol('x'))
        substituted = substitute(expr, 'y', 2)
        self.assertEqual(substituted, expr)

        expr = Expr('+', [
            Expr('*', [Expr(Symbol('x')), Expr(3)]),
            Expr(Symbol('z'))
        ])
        substituted = substitute(expr, Symbol('x'), 5)
        expected_substituted = Expr('+', [
            Expr('*', [Expr(5), Expr(3)]),
            Expr(Symbol('z'))
        ])
        self.assertEqual(substituted, expected_substituted)

        expr = Expr('+', [
            Expr('*', [Expr(Symbol('x')), Expr(3)]),
            Expr(Symbol('z'))
        ])
        substituted = substitute(expr, Symbol('x'), Expr(5))
        expected_substituted = Expr('+', [
            Expr('*', [Expr(5), Expr(3)]),
            Expr(Symbol('z'))
        ])
        self.assertEqual(substituted, expected_substituted)

        expr = Expr('*', [
            Expr(Symbol('x')),
            Expr(3),
            Expr(Symbol('z'))
        ])
        substituted = substitute(expr, '*', '+')
        self.assertEqual(substituted, expr)

        expr = Expr('*', [
            Expr(Symbol('x')),
            Expr(3),
            Expr(Symbol('z'))
        ])
        substituted = substitute(expr, 'z', Expr(Symbol('x')))
        expected_substituted = Expr('*', [
            Expr(Symbol('x')),
            Expr(3),
            Expr(Symbol('x'))
        ])
        self.assertEqual(substituted, expected_substituted)


if __name__ == '__main__':
    unittest.main()
