import unittest
from ..expr import *
from ..operations import *


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
