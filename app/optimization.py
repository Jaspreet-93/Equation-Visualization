"""
Optimization Module
Provides critical point detection, first and second derivative tests,
classification of local maxima, minima, inflection points, and global extrema.
"""

from typing import List, Dict, Any, Optional
import sympy as sp

x = sp.Symbol('x')


def find_critical_points(expr: sp.Expr) -> List[Dict[str, Any]]:
    """
    Finds and classifies all real critical points of expr where f'(x) = 0.
    Uses the second derivative test f''(x):
      - f''(x) > 0  => Local Minimum
      - f''(x) < 0  => Local Maximum
      - f''(x) == 0 => Inconclusive / Saddle / Inflection candidate
    """
    d1 = sp.diff(expr, x)
    d2 = sp.diff(d1, x)

    critical_points = []

    # Solve d1 = 0
    try:
        solutions = sp.solve(d1, x)
    except Exception:
        solutions = []

    for sol in solutions:
        # Filter for real solutions
        try:
            num_x = complex(sp.N(sol))
            if abs(num_x.imag) > 1e-9:
                continue  # Skip non-real critical points
            rx = num_x.real

            # Evaluate y = f(x)
            y_val_sym = expr.subs(x, sol)
            ry = float(sp.N(y_val_sym))

            # Evaluate second derivative at critical point
            d2_val_sym = d2.subs(x, sol)
            rd2 = float(sp.N(d2_val_sym))

            if rd2 > 1e-9:
                nature = "Local Minimum"
            elif rd2 < -1e-9:
                nature = "Local Maximum"
            else:
                nature = "Inflection / Inconclusive"

            critical_points.append({
                "x_sym": sol,
                "x": rx,
                "y": ry,
                "d2": rd2,
                "nature": nature,
            })
        except Exception:
            continue

    # Sort by x coordinate
    critical_points.sort(key=lambda item: item["x"])
    return critical_points


def find_inflection_points(expr: sp.Expr) -> List[Dict[str, Any]]:
    """
    Finds real inflection points where f''(x) = 0.
    """
    d2 = sp.diff(expr, x, 2)
    inflections = []
    try:
        solutions = sp.solve(d2, x)
    except Exception:
        solutions = []

    for sol in solutions:
        try:
            num_x = complex(sp.N(sol))
            if abs(num_x.imag) > 1e-9:
                continue
            rx = num_x.real
            y_val = float(sp.N(expr.subs(x, sol)))
            inflections.append({
                "x_sym": sol,
                "x": rx,
                "y": y_val,
                "nature": "Inflection Point",
            })
        except Exception:
            continue

    inflections.sort(key=lambda item: item["x"])
    return inflections


def find_global_extrema(
    expr: sp.Expr,
    x_min: float,
    x_max: float,
) -> Dict[str, Optional[Dict[str, float]]]:
    """
    Finds global maximum and global minimum in the closed interval [x_min, x_max].
    Checks interior critical points and interval boundaries.
    """
    candidates = []

    # Evaluate boundaries
    for boundary in (x_min, x_max):
        try:
            yb = float(sp.N(expr.subs(x, boundary)))
            candidates.append({"x": boundary, "y": yb, "type": "Boundary"})
        except Exception:
            pass

    # Interior critical points
    cps = find_critical_points(expr)
    for cp in cps:
        if x_min <= cp["x"] <= x_max:
            candidates.append({"x": cp["x"], "y": cp["y"], "type": cp["nature"]})

    if not candidates:
        return {"global_min": None, "global_max": None}

    g_min = min(candidates, key=lambda c: c["y"])
    g_max = max(candidates, key=lambda c: c["y"])

    return {"global_min": g_min, "global_max": g_max}
