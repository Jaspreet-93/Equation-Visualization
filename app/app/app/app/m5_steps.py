"""
Legacy Module Wrapper: m5_steps.py
Redirects to app.step_explainer.
"""

from app.math_engine import x, ALLOWED_SYMBOLS as ALLOWED, parse_math_expression as parse_expr
from app.step_explainer import explain_roots, explain_derivative, explain_integration, explain_optimization

if __name__ == '__main__':
    s = input("Enter f(x): ") or "x**2 - 5*x + 6"
    e = parse_expr(s)
    print("-- Roots Explanation --")
    print(explain_roots(e))
    print("\n-- Derivative Explanation --")
    print(explain_derivative(e))
