from sympy import symbols, sympify, solveset, S

x = symbols('x')

# ---- Safe parsing: only allow x and selected functions ----
ALLOWED = {
    'x': x,
    # common functions
    'sin': __import__('sympy').sin,
    'cos': __import__('sympy').cos,
    'tan': __import__('sympy').tan,
    'exp': __import__('sympy').exp,
    'log': __import__('sympy').log,
    'sqrt': __import__('sympy').sqrt,
    'Abs': __import__('sympy').Abs
}

def parse_expr(expr_str: str):
    return sympify(expr_str, locals=ALLOWED)

if __name__ == '__main__':
    expr_str = input("Enter f(x): ")  # e.g., x**2 - 5*x + 6
    f = parse_expr(expr_str)
    print("Parsed:", f)

    # Solve f(x)=0 in Reals
    roots = list(solveset(f, x, domain=S.Reals))
    print("Roots:", roots)