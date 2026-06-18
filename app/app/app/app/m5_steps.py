from sympy import symbols, sympify, Poly, diff, simplify


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




def explain_roots(expr):
lines = []
try:
p = Poly(expr, x)
deg = p.degree()
lines.append(f"Treat f(x) as a polynomial of degree {deg}.")
if deg == 2:
a, b, c = p.all_coeffs()
lines.append(f"Coefficients: a={a}, b={b}, c={c}")
disc = b**2 - 4*a*c
lines.append(f"Discriminant: Δ = b^2 - 4ac = {disc}")
lines.append("Quadratic formula: x = (-b ± √Δ) / (2a)")
lines.append("Compute the two roots using the formula.")
else:
lines.append("Use symbolic methods: factorization / numerical methods if needed.")
except Exception:
lines.append("Expression is not a simple polynomial. Use solveset for general solving.")
return "\n".join(lines)




def explain_derivative(expr):
lines = ["Differentiate term by term using rules:"]
lines.append("- d/dx[x^n] = n*x^(n-1)")
lines.append("- d/dx[sin(x)] = cos(x), d/dx[cos(x)] = -sin(x)")
lines.append("- d/dx[exp(x)] = exp(x), d/dx[log(x)] = 1/x")
dexpr = diff(expr, x)
lines.append(f"Computed derivative: f'(x) = {simplify(dexpr)}")
return "\n".join(lines)




if __name__ == '__main__':
s = input("Enter f(x): ")
e = parse_expr(s)
print("-- Roots Explanation --")
print(explain_roots(e))
print("\n-- Derivative Explanation --")
print(explain_derivative(e))