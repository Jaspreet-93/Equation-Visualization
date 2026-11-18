"""
Smart Equation Visualizer and Solver Package
"""

from app.math_engine import parse_math_expression, find_roots, evaluate_at
from app.calculus import compute_derivative, compute_integral, compute_tangent_line, compute_limit
from app.optimization import find_critical_points, find_inflection_points, find_global_extrema
from app.step_explainer import explain_roots, explain_derivative, explain_integration, explain_optimization
from app.plotter import generate_plot_data, render_plot_on_axes

__all__ = [
    "parse_math_expression",
    "find_roots",
    "evaluate_at",
    "compute_derivative",
    "compute_integral",
    "compute_tangent_line",
    "compute_limit",
    "find_critical_points",
    "find_inflection_points",
    "find_global_extrema",
    "explain_roots",
    "explain_derivative",
    "explain_integration",
    "explain_optimization",
    "generate_plot_data",
    "render_plot_on_axes",
]
