"""
Calculus Engine Module
Provides symbolic and numeric calculus operations:
derivatives, integrals, tangent & normal lines, and limits.
"""

from typing import Tuple, Optional, Any, Dict
import sympy as sp

x = sp.Symbol('x')


def compute_derivative(expr: sp.Expr, order: int = 1) -> sp.Expr:
    """Computes the n-th derivative of expr with respect to x."""
    if order < 1:
        raise ValueError("Derivative order must be at least 1.")
    return sp.diff(expr, x, order)


def compute_integral(
    expr: sp.Expr,
    definite: bool = False,
    a: Optional[float] = None,
    b: Optional[float] = None,
) -> sp.Expr:
    """
    Computes either the indefinite integral or definite integral between [a, b].
    """
    if definite:
        if a is None or b is None:
            raise ValueError("Limits 'a' and 'b' must be provided for definite integration.")
        return sp.integrate(expr, (x, a, b))
    return sp.integrate(expr, x)


def compute_tangent_line(expr: sp.Expr, x0: float) -> Dict[str, Any]:
    """
    Computes the tangent line equation at point x = x0.
    Returns slope m = f'(x0), point y0 = f(x0), and the tangent line equation string.
    """
    dexpr = compute_derivative(expr, order=1)
    try:
        y0_sym = expr.subs(x, x0)
        m_sym = dexpr.subs(x, x0)
        y0 = float(sp.N(y0_sym))
        m = float(sp.N(m_sym))
    except Exception as exc:
        raise ValueError(f"Function or derivative is not defined at x = {x0}: {exc}")

    # Tangent line equation: y = m*(x - x0) + y0
    tangent_expr = sp.simplify(m_sym * (x - x0) + y0_sym)

    return {
        "x0": x0,
        "y0": y0,
        "slope": m,
        "tangent_expr": tangent_expr,
        "equation_str": f"y = {m:.4f}*(x - {x0}) + {y0:.4f}",
    }


def compute_normal_line(expr: sp.Expr, x0: float) -> Dict[str, Any]:
    """
    Computes the normal line perpendicular to the tangent at x = x0.
    """
    tangent_info = compute_tangent_line(expr, x0)
    m = tangent_info["slope"]
    y0 = tangent_info["y0"]

    if abs(m) < 1e-12:
        return {
            "x0": x0,
            "y0": y0,
            "slope": float("inf"),
            "equation_str": f"x = {x0}",
        }

    normal_slope = -1.0 / m
    normal_expr = normal_slope * (x - x0) + y0
    return {
        "x0": x0,
        "y0": y0,
        "slope": normal_slope,
        "normal_expr": normal_expr,
        "equation_str": f"y = {normal_slope:.4f}*(x - {x0}) + {y0:.4f}",
    }


def compute_limit(
    expr: sp.Expr,
    point: float,
    direction: str = "+-",
) -> Tuple[sp.Expr, Optional[float]]:
    """
    Computes the limit of expr as x approaches point.
    direction can be '+', '-', or '+-' (two-sided).
    """
    if direction == "+-":
        lim = sp.limit(expr, x, point)
    else:
        lim = sp.limit(expr, x, point, dir=direction)

    try:
        num_val = float(sp.N(lim))
    except Exception:
        num_val = None

    return lim, num_val
