"""
Legacy Module Wrapper: m1_math_engine.py
Redirects to app.math_engine for modern parsing & root finding.
"""

from app.math_engine import x, ALLOWED_SYMBOLS as ALLOWED, parse_math_expression as parse_expr, find_roots

if __name__ == '__main__':
    expr_str = input("Enter f(x): ") or "x**2 - 5*x + 6"
    try:
        f = parse_expr(expr_str)
        print("Parsed:", f)
        roots = [r[0] for r in find_roots(f, domain="reals")]
        print("Roots:", roots)
    except Exception as exc:
        print("Error:", exc)
