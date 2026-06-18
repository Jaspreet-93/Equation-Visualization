import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify

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

def plot_function(expr, xmin=-10, xmax=10, num=1000):
    f = lambdify(x, expr, 'numpy')
    X = np.linspace(xmin, xmax, num)
    # Safely evaluate (handle domain errors)
    Y = np.empty_like(X, dtype=float)
    Y[:] = np.nan
    for i, t in enumerate(X):
        try:
            val = f(t)
            if np.isfinite(val):
                Y[i] = val
        except Exception:
            pass
    plt.figure(figsize=(8, 5))
    plt.plot(X, Y)
    plt.axhline(0, linewidth=1)
    plt.axvline(0, linewidth=1)
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(f'f(x) = {expr}')
    plt.show()

if __name__ == '__main__':
    s = input("Enter f(x): ")
    expr = parse_expr(s)
    plot_function(expr)

