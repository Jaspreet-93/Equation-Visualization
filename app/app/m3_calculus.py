import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify, solveset, S, diff

x = symbols('x')
ALLOWED = {
    'x': x,
    'sin': __import__('sympy').sin,
    'cos': __import__('sympy').cos,
    'tan': __import__('sympy').tan,
    'exp': __import__('sympy').exp,
    'log': __import__('sympy').log,
    'sqrt': __import__('sympy').sqrt,
    'Abs': __import__('sympy').Abs
}

def parse_expr(s):
    return sympify(s, locals=ALLOWED)

def safe_eval(expr, X):
    f = lambdify(x, expr, 'numpy')
    Y = np.empty_like(X, dtype=float)
    Y[:] = np.nan
    for i, t in enumerate(X):
        try:
            val = f(t)
            if np.isfinite(val):
                Y[i] = val
        except Exception:
            pass
    return Y





def plot_with_features(expr, x0=None, xmin=-10, xmax=10, num=1000):
    X = np.linspace(xmin, xmax, num)
    Y = safe_eval(expr, X)

    # Roots (real)
    roots = list(solveset(expr, x, domain=S.Reals))

    # Derivative & tangent line at x0
    m = None
    y0 = None
    if x0 is not None:
        dexpr = diff(expr, x)
        f = lambdify(x, expr, 'numpy')
        df = lambdify(x, dexpr, 'numpy')
        try:
            y0 = float(f(x0))
            m = float(df(x0))
        except Exception:
            x0 = None  # invalid point

    plt.figure(figsize=(8, 5))
    plt.plot(X, Y, label=f'f(x)={expr}')

    # Mark roots
    for r in roots:
        try:
            rv = float(r)
            plt.scatter([rv], [0], marker='o')
        except Exception:
            pass

    # Tangent
    if x0 is not None and m is not None and y0 is not None:
        T = np.linspace(x0-3, x0+3, 100)
        tangent = m*(T - x0) + y0
        plt.plot(T, tangent, linestyle='--', label=f'Tangent at x0={x0}')
        plt.scatter([x0], [y0])

    plt.axhline(0, linewidth=1)
    plt.axvline(0, linewidth=1)
    plt.grid(True)
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Graph with Roots & Tangent')
    plt.show()





if __name__ == '__main__':
s = input("Enter f(x): ")
expr = parse_expr(s)
try:
x0 = float(input("Enter x0 for tangent (or blank to skip): ") or 'nan')
except Exception:
x0 = float('nan')
plot_with_features(expr, x0 if np.isfinite(x0) else None)