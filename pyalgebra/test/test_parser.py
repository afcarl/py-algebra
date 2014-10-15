import unittest
from ..expr import *
from ..parser import *


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

if __name__ == '__main__':
    unittest.main()
