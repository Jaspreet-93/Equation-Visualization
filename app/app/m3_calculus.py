"""
Legacy Module Wrapper: m3_calculus.py
Redirects to app.calculus and app.plotter.
"""

import numpy as np
import matplotlib.pyplot as plt
from app.math_engine import x, ALLOWED_SYMBOLS as ALLOWED, parse_math_expression as parse_expr, find_roots
from app.calculus import compute_derivative, compute_tangent_line
from app.plotter import generate_plot_data, render_plot_on_axes

def safe_eval(expr, X):
    f_X, f_Y = generate_plot_data(expr, xmin=float(X[0]), xmax=float(X[-1]), num=len(X))
    return f_Y

def plot_with_features(expr, x0=None, xmin=-10, xmax=10, num=1000):
    fig, ax = plt.subplots(figsize=(8, 5))
    render_plot_on_axes(
        ax,
        expr,
        xmin=xmin,
        xmax=xmax,
        show_roots=True,
        show_extrema=False,
        show_tangent=(x0 is not None),
        x0=x0,
    )
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    s = input("Enter f(x): ") or "x**2 - 5*x + 6"
    expr = parse_expr(s)
    try:
        x0_str = input("Enter x0 for tangent (or blank to skip): ")
        x0 = float(x0_str) if x0_str.strip() else None
    except Exception:
        x0 = None
    plot_with_features(expr, x0=x0)
