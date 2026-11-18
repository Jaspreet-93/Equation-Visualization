"""
Plotter Module
Provides numerical curve evaluation with singularity handling,
and Matplotlib plotting with roots, extrema, and tangent line overlays.
"""

from typing import Tuple, Optional
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

from app.math_engine import find_roots, parse_math_expression
from app.calculus import compute_tangent_line
from app.optimization import find_critical_points

x = sp.Symbol('x')


def generate_plot_data(
    expr: sp.Expr,
    xmin: float = -10.0,
    xmax: float = 10.0,
    num: int = 1000,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Safely converts a SymPy expression to NumPy points over [xmin, xmax].
    Replaces undefined points, divide-by-zero, complex numbers, and asymptotes with NaN.
    """
    f = sp.lambdify(x, expr, modules=['numpy'])
    X = np.linspace(xmin, xmax, num)
    Y = np.empty_like(X, dtype=float)
    Y[:] = np.nan

    for i, t in enumerate(X):
        try:
            val = f(t)
            # Check for scalar finite float
            if np.isreal(val) and np.isfinite(val):
                # Filter out huge asymptote jump values
                if abs(val) < 1e6:
                    Y[i] = float(val)
        except Exception:
            pass

    return X, Y


def render_plot_on_axes(
    ax: plt.Axes,
    expr: sp.Expr,
    xmin: float = -10.0,
    xmax: float = 10.0,
    show_roots: bool = True,
    show_extrema: bool = True,
    show_tangent: bool = False,
    x0: Optional[float] = None,
    grid: bool = True,
) -> None:
    """
    Renders the complete mathematical graph onto a Matplotlib Axes object.
    Includes axis lines, curve, roots, extrema, and tangent overlays.
    """
    ax.clear()

    # Generate and plot primary curve
    X, Y = generate_plot_data(expr, xmin=xmin, xmax=xmax)
    ax.plot(X, Y, label=f"f(x) = {expr}", color="#1f77b4", linewidth=2.0)

    # Roots Overlay
    if show_roots:
        roots = find_roots(expr, domain="reals")
        root_xs = [r[1] for r in roots if r[1] is not None and xmin <= r[1] <= xmax]
        if root_xs:
            ax.scatter(
                root_xs,
                [0.0] * len(root_xs),
                color="#d62728",
                s=60,
                zorder=5,
                label=f"Roots ({len(root_xs)})",
            )
            for rx in root_xs:
                ax.annotate(
                    f"({rx:.2f}, 0)",
                    (rx, 0),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha="center",
                    fontsize=8,
                    color="#d62728",
                    fontweight="bold",
                )

    # Extrema Overlay
    if show_extrema:
        cps = find_critical_points(expr)
        for cp in cps:
            cx, cy = cp["x"], cp["y"]
            if xmin <= cx <= xmax and np.isfinite(cy):
                color = "#2ca02c" if "Min" in cp["nature"] else "#ff7f0e"
                ax.scatter([cx], [cy], color=color, s=70, zorder=6, label=cp["nature"])
                ax.annotate(
                    f"{cp['nature']}\n({cx:.2f}, {cy:.2f})",
                    (cx, cy),
                    textcoords="offset points",
                    xytext=(0, -20 if "Min" in cp["nature"] else 15),
                    ha="center",
                    fontsize=8,
                    color=color,
                    fontweight="bold",
                )

    # Tangent Line Overlay
    if show_tangent and x0 is not None and xmin <= x0 <= xmax:
        try:
            tinfo = compute_tangent_line(expr, x0)
            m = tinfo["slope"]
            y0 = tinfo["y0"]
            span = max(2.0, (xmax - xmin) * 0.2)
            t_x = np.linspace(max(xmin, x0 - span), min(xmax, x0 + span), 100)
            t_y = m * (t_x - x0) + y0

            ax.plot(
                t_x,
                t_y,
                linestyle="--",
                color="#9467bd",
                linewidth=1.8,
                label=f"Tangent at x={x0:.2f} (m={m:.2f})",
            )
            ax.scatter([x0], [y0], color="#9467bd", s=50, zorder=7)
        except Exception:
            pass

    # Zero axes and styling
    ax.axhline(0, color="#333333", linewidth=1.0, linestyle="-", alpha=0.7)
    ax.axvline(0, color="#333333", linewidth=1.0, linestyle="-", alpha=0.7)
    if grid:
        ax.grid(True, linestyle=":", alpha=0.6)

    ax.set_xlim(xmin, xmax)
    # Auto-limit y to reasonable bounds to avoid extreme asymptote scaling
    valid_y = Y[np.isfinite(Y)]
    if len(valid_y) > 0:
        p_low = np.percentile(valid_y, 2)
        p_high = np.percentile(valid_y, 98)
        margin = max(1.0, (p_high - p_low) * 0.15)
        ax.set_ylim(p_low - margin, p_high + margin)

    ax.set_xlabel("x", fontsize=11)
    ax.set_ylabel("f(x)", fontsize=11)
    ax.set_title(f"Graph of f(x) = {expr}", fontsize=12, fontweight="bold")

    # Deduplicate legend labels
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    if by_label:
        ax.legend(by_label.values(), by_label.keys(), loc="upper right", fontsize=9)


def plot_standalone(expr_str: str, xmin: float = -10.0, xmax: float = 10.0) -> None:
    """Convenience function to plot in a standalone Matplotlib window."""
    expr = parse_math_expression(expr_str)
    fig, ax = plt.subplots(figsize=(9, 6))
    render_plot_on_axes(ax, expr, xmin=xmin, xmax=xmax, show_roots=True, show_extrema=True)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    eq = input("Enter equation (e.g. x^3 - 3x): ") or "x^3 - 3x"
    plot_standalone(eq)
