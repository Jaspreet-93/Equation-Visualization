"""
Legacy Module Wrapper: m4_optimization.py
Provides true optimization analysis (critical points, classification, and extrema plotting).
"""

import matplotlib.pyplot as plt
from app.math_engine import x, ALLOWED_SYMBOLS as ALLOWED, parse_math_expression as parse_expr
from app.optimization import find_critical_points, find_global_extrema
from app.plotter import render_plot_on_axes

def analyze_and_plot_extrema(expr, xmin=-10, xmax=10):
    print("Finding critical points...")
    cps = find_critical_points(expr)
    for cp in cps:
        print(f"  Critical point at x = {cp['x']:.4f}, y = {cp['y']:.4f} -> {cp['nature']}")

    extrema = find_global_extrema(expr, xmin, xmax)
    print(f"Global min on [{xmin}, {xmax}]: {extrema['global_min']}")
    print(f"Global max on [{xmin}, {xmax}]: {extrema['global_max']}")

    fig, ax = plt.subplots(figsize=(8, 5))
    render_plot_on_axes(ax, expr, xmin=xmin, xmax=xmax, show_roots=False, show_extrema=True)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    s = input("Enter f(x): ") or "x**3 - 3*x"
    expr = parse_expr(s)
    analyze_and_plot_extrema(expr)
