"""Operations that can be used on expressions."""

from .expr import *


def simplify(expr):
    """
    Simplifies an expression by combining operands of the same type.

    Does not modify the expression passed in.
    Returns a new expression instead.

    Parameters:
    expr: (Expr object) - the expression to simplify

    Returns:
    new_expr: (Expr object) - the simplified expression
    """
    pass


def substitute(expr, var, new_var):
    """
    Substitutes a new number, variable, or expr in the expression.

    This does not simplify the expression.  It simply replaces all occurences
    of var with new_var.  It returns a new expression and does not modify expr.

    Parameters:
    expr: (Expr object) - the expression to substitute new_var in 
    var: (Symbol object or string) - either the string name of the symbol to
        replace or a Symbol object with that string name.  I.e. passing in
        Symbol('x') is equivalent to passing in 'x'.
    new_var:
        (a number, Symbol object, string name for Symbol, Expr object)
        - what to replace var with in the expression

    Returns:
    new_expr: (Expr object) - a new expression that is the result of performing
        the substitution on the given expr
    """
    if not isinstance(var, Symbol):
        var = Symbol(var)
    if not isinstance(new_var, (Number, Symbol, Expr)):
        new_var = Symbol(new_var)
    if not isinstance(new_var, Expr):
        new_var = Expr(new_var)
    return _substitute_helper(expr, var, new_var)


def _substitute_helper(expr, var, new_var_expr):
    """
    Helper method for substitute.

    Parameters:
    expr: (Expr object) - the expression to subtitute new_expr in
    var: (Symbol object or string) - the string name or symbol to replace
    new_var_expr: (Expr object) - the expression that will replace ones
        that have var as the value
    """
    if not expr.operands and expr.value == var:
        return new_var_expr
    operands = [_substitute_helper(operand, var, new_var_expr)
        for operand in expr.operands]
    return Expr(expr.value, operands)


def evalute(expr, var, new_var):
    """
    Evaluates the expression by replacing the given variable with the new value.

    This is equivalent to using substitute and then simplify.

    Parameters:
    expr: (Expr object) - the expression to simplify
    var: (Symbol object or string) - either the string name of the symbol to
        replace or a Symbol object with that string name.  I.e. passing in
        Symbol('x') is equivalent to passing in 'x'.
    new_var:
        -Type: Anything valid to place in an expression -- a number,
        Symbol object, string name for Symbol, Expr object, etc
        -Description: What to replace var with in the expression

    Returns:
    new_expr: (Expr object) - a new expression that is the result of evaluating
        the given expr
    """
    pass
