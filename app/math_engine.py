"""
Math Engine Module
Provides safe expression parsing with implicit multiplication,
root finding (real and complex), and expression evaluation.
"""

from typing import List, Tuple, Any, Dict
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

x = sp.Symbol('x')

# Standard allowed functions and symbols for safe parsing
ALLOWED_SYMBOLS: Dict[str, Any] = {
    'x': x,
    # Trigonometric & Hyperbolic
    'sin': sp.sin,
    'cos': sp.cos,
    'tan': sp.tan,
    'asin': sp.asin,
    'acos': sp.acos,
    'atan': sp.atan,
    'sinh': sp.sinh,
    'cosh': sp.cosh,
    'tanh': sp.tanh,
    # Exponential & Logarithmic
    'exp': sp.exp,
    'log': sp.log,
    'ln': sp.log,
    # Algebraic & Specials
    'sqrt': sp.sqrt,
    'cbrt': sp.cbrt,
    'Abs': sp.Abs,
    'abs': sp.Abs,
    # Constants
    'pi': sp.pi,
    'E': sp.E,
    'e': sp.E,
    'oo': sp.oo,
}

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


def parse_math_expression(expr_str: str) -> sp.Expr:
    """
    Parses a user equation or expression string into a SymPy expression safely.
    Supports implicit multiplication (e.g., '2x', '3(x+1)'),
    caret exponentiation ('x^2'), and equation strings ('x^2 = 4').
    """
    if not expr_str or not expr_str.strip():
        raise ValueError("Expression cannot be empty.")

    clean_str = expr_str.strip()

    # Handle equation format (e.g. 'x^2 - 4 = 0' or 'x^2 = 4')
    if '=' in clean_str:
        parts = clean_str.split('=', 1)
        lhs = parse_expr(
            parts[0].strip(),
            local_dict=ALLOWED_SYMBOLS,
            transformations=TRANSFORMATIONS,
        )
        rhs = parse_expr(
            parts[1].strip(),
            local_dict=ALLOWED_SYMBOLS,
            transformations=TRANSFORMATIONS,
        )
        return sp.simplify(lhs - rhs)

    return parse_expr(
        clean_str,
        local_dict=ALLOWED_SYMBOLS,
        transformations=TRANSFORMATIONS,
    )


def find_roots(expr: sp.Expr, domain: str = "reals") -> List[Tuple[Any, float]]:
    """
    Solves for roots of expr = 0.
    Returns a list of tuples: (symbolic_root, numerical_value_or_none).
    """
    roots_result = []

    if domain == "reals":
        try:
            sol_set = sp.solveset(expr, x, domain=sp.S.Reals)
            if isinstance(sol_set, sp.FiniteSet):
                for r in sol_set:
                    try:
                        num_val = float(sp.N(r))
                    except Exception:
                        num_val = None
                    roots_result.append((r, num_val))
            elif isinstance(sol_set, (sp.Union, sp.Intersection)):
                for r in sol_set:
                    try:
                        num_val = float(sp.N(r))
                    except Exception:
                        num_val = None
                    roots_result.append((r, num_val))
            else:
                raw_roots = sp.solve(expr, x)
                for r in raw_roots:
                    try:
                        val = complex(sp.N(r))
                        if abs(val.imag) < 1e-9:
                            roots_result.append((r, val.real))
                    except Exception:
                        pass
        except Exception:
            raw_roots = sp.solve(expr, x)
            for r in raw_roots:
                try:
                    num_val = float(sp.N(r))
                    roots_result.append((r, num_val))
                except Exception:
                    pass
    else:
        raw_roots = sp.solve(expr, x)
        for r in raw_roots:
            try:
                num_val = complex(sp.N(r))
            except Exception:
                num_val = None
            roots_result.append((r, num_val))

    # Sort roots by numerical value if available
    roots_result.sort(key=lambda t: (t[1] is None, t[1] if t[1] is not None else 0))
    return roots_result


def evaluate_at(expr: sp.Expr, x_val: float) -> float:
    """Evaluates the expression numerically at x = x_val."""
    res = expr.subs(x, x_val)
    return float(sp.N(res))


if __name__ == '__main__':
    user_input = input("Enter f(x) or equation (e.g. 2x^2 - 5x + 6 = 0): ")
    try:
        f = parse_math_expression(user_input)
        print("Parsed Expression f(x):", f)
        roots = find_roots(f)
        print("Real Roots:")
        for sym_root, val in roots:
            print(f"  Exact: {sym_root}  ~  {val}")
    except Exception as exc:
        print("Error:", exc)
