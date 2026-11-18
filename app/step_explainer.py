"""
Step Explainer Module
Generates human-readable, step-by-step mathematical explanations
for root solving, differentiation, integration, and optimization.
"""

from typing import List
import sympy as sp

x = sp.Symbol('x')


def explain_roots(expr: sp.Expr) -> str:
    """
    Produces step-by-step reasoning for finding roots of f(x) = 0.
    """
    lines: List[str] = [f"Goal: Solve f(x) = 0 for expression: {expr}"]

    try:
        poly = sp.Poly(expr, x)
        deg = poly.degree()
        lines.append(f"1. Identified polynomial in x of degree {deg}.")

        if deg == 1:
            coeffs = poly.all_coeffs()
            a, b = coeffs[0], coeffs[1]
            lines.append(f"   Linear equation form: {a}*x + ({b}) = 0")
            lines.append(f"   Subtract constant: {a}*x = {-b}")
            lines.append(f"   Divide by coefficient: x = ({-b}) / ({a}) = {-b/a}")

        elif deg == 2:
            coeffs = poly.all_coeffs()
            a, b, c = coeffs[0], coeffs[1], coeffs[2]
            lines.append(f"   Standard quadratic form: ax^2 + bx + c = 0")
            lines.append(f"   Identified coefficients: a = {a}, b = {b}, c = {c}")
            disc = b**2 - 4 * a * c
            lines.append(f"2. Compute Discriminant Δ = b^2 - 4ac")
            lines.append(f"   Δ = ({b})^2 - 4*({a})*({c}) = {disc}")

            if disc > 0:
                lines.append("   Since Δ > 0, the equation has 2 distinct real roots.")
            elif disc == 0:
                lines.append("   Since Δ = 0, the equation has exactly 1 repeated real root.")
            else:
                lines.append("   Since Δ < 0, the equation has 2 complex conjugate roots.")

            lines.append("3. Apply Quadratic Formula: x = (-b ± √Δ) / (2a)")
            r1 = (-b + sp.sqrt(disc)) / (2 * a)
            r2 = (-b - sp.sqrt(disc)) / (2 * a)
            lines.append(f"   x1 = ({-b} + √({disc})) / (2*{a}) = {r1}")
            lines.append(f"   x2 = ({-b} - √({disc})) / (2*{a}) = {r2}")

        else:
            lines.append("2. High-degree polynomial: Attempting symbolic factorization.")
            factored = sp.factor(expr)
            if factored != expr:
                lines.append(f"   Factored form: {factored} = 0")
            sols = sp.solve(expr, x)
            lines.append(f"3. Exact roots found: {sols}")

    except Exception:
        lines.append("1. Expression is non-polynomial (transcendental/rational).")
        lines.append("2. Isolating roots via symbolic solvers or numerical methods.")
        sols = sp.solve(expr, x)
        lines.append(f"3. Solutions: {sols}")

    return "\n".join(lines)


def explain_derivative(expr: sp.Expr) -> str:
    """
    Produces step-by-step reasoning for calculating the first derivative.
    """
    lines: List[str] = [f"Goal: Differentiate f(x) = {expr} with respect to x"]
    lines.append("1. Core Differentiation Rules Reference:")
    lines.append("   • Power Rule:       d/dx [x^n] = n * x^(n-1)")
    lines.append("   • Constant Rule:    d/dx [c] = 0")
    lines.append("   • Trig Rules:       d/dx [sin(x)] = cos(x), d/dx [cos(x)] = -sin(x)")
    lines.append("   • Exponential Rule: d/dx [e^x] = e^x")
    lines.append("   • Logarithmic Rule: d/dx [ln(x)] = 1/x")
    lines.append("   • Product Rule:     d/dx [u*v] = u'v + uv'")
    lines.append("   • Chain Rule:       d/dx [f(g(x))] = f'(g(x)) * g'(x)")

    dexpr = sp.diff(expr, x)
    simplified_dexpr = sp.simplify(dexpr)

    lines.append(f"2. Applied rules term-by-term:")
    lines.append(f"   Raw derivative:  {dexpr}")
    lines.append(f"   Simplified:      f'(x) = {simplified_dexpr}")
    return "\n".join(lines)


def explain_integration(expr: sp.Expr) -> str:
    """
    Produces step-by-step reasoning for calculating the antiderivative.
    """
    lines: List[str] = [f"Goal: Integrate ∫ ({expr}) dx"]
    lines.append("1. Core Integration Rules Reference:")
    lines.append("   • Power Rule:       ∫ x^n dx = (x^(n+1))/(n+1) + C (for n ≠ -1)")
    lines.append("   • Reciprocal Rule:  ∫ (1/x) dx = ln|x| + C")
    lines.append("   • Exponential Rule: ∫ e^x dx = e^x + C")
    lines.append("   • Trig Rules:       ∫ sin(x) dx = -cos(x) + C,  ∫ cos(x) dx = sin(x) + C")

    integral = sp.integrate(expr, x)
    lines.append(f"2. Antiderivative:")
    lines.append(f"   F(x) = {integral} + C")
    return "\n".join(lines)


def explain_optimization(expr: sp.Expr) -> str:
    """
    Produces step-by-step reasoning for finding local extrema.
    """
    lines: List[str] = [f"Goal: Find local extrema of f(x) = {expr}"]
    d1 = sp.diff(expr, x)
    d2 = sp.diff(d1, x)

    lines.append(f"1. Compute First Derivative: f'(x) = {d1}")
    lines.append("2. Set f'(x) = 0 and solve for critical points:")
    try:
        cps = sp.solve(d1, x)
        lines.append(f"   Critical x-values: {cps}")
    except Exception as exc:
        lines.append(f"   Failed to solve f'(x) = 0: {exc}")
        return "\n".join(lines)

    lines.append(f"3. Compute Second Derivative for classification: f''(x) = {d2}")
    lines.append("   Classification Criteria:")
    lines.append("   • If f''(c) > 0  => Local Minimum at x = c")
    lines.append("   • If f''(c) < 0  => Local Maximum at x = c")
    lines.append("   • If f''(c) == 0 => Inconclusive / Inflection")

    for cp in cps:
        try:
            d2_val = d2.subs(x, cp)
            y_val = expr.subs(x, cp)
            lines.append(f"   At critical point x = {cp}:")
            lines.append(f"     f({cp}) = {y_val}")
            lines.append(f"     f''({cp}) = {d2_val}")
            if d2_val > 0:
                lines.append(f"     Conclusion: Local MINIMUM at ({cp}, {y_val})")
            elif d2_val < 0:
                lines.append(f"     Conclusion: Local MAXIMUM at ({cp}, {y_val})")
            else:
                lines.append(f"     Conclusion: Inflection Point or Inconclusive at ({cp}, {y_val})")
        except Exception:
            continue

    return "\n".join(lines)
