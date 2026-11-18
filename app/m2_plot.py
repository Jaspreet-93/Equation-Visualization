"""
Legacy Module Wrapper: m2_plot.py
Redirects to app.plotter for safe numeric evaluation & plotting.
"""

from app.math_engine import x, ALLOWED_SYMBOLS as ALLOWED, parse_math_expression as parse_expr
from app.plotter import generate_plot_data, plot_standalone as plot_function

if __name__ == '__main__':
    s = input("Enter f(x): ") or "x**2 - 5*x + 6"
    plot_function(s)
