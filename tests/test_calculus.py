import unittest
import sympy as sp
from app.math_engine import parse_math_expression
from app.calculus import (
    compute_derivative,
    compute_integral,
    compute_tangent_line,
    compute_normal_line,
    compute_limit,
)


class TestCalculusEngine(unittest.TestCase):
    def test_first_derivative(self):
        expr = parse_math_expression("x^3 - 4x^2 + 7")
        d1 = compute_derivative(expr, 1)
        self.assertEqual(sp.simplify(d1 - (3*sp.Symbol('x')**2 - 8*sp.Symbol('x'))), 0)

    def test_second_derivative(self):
        expr = parse_math_expression("x^3")
        d2 = compute_derivative(expr, 2)
        self.assertEqual(sp.simplify(d2 - 6*sp.Symbol('x')), 0)

    def test_indefinite_integral(self):
        expr = parse_math_expression("3x^2")
        antideriv = compute_integral(expr, definite=False)
        self.assertEqual(sp.simplify(antideriv - sp.Symbol('x')**3), 0)

    def test_definite_integral(self):
        expr = parse_math_expression("2x")
        val = compute_integral(expr, definite=True, a=0, b=3)
        self.assertAlmostEqual(float(val), 9.0)

    def test_tangent_line(self):
        expr = parse_math_expression("x^2")
        tinfo = compute_tangent_line(expr, x0=2.0)
        self.assertAlmostEqual(tinfo["slope"], 4.0)
        self.assertAlmostEqual(tinfo["y0"], 4.0)

    def test_normal_line(self):
        expr = parse_math_expression("x^2")
        ninfo = compute_normal_line(expr, x0=2.0)
        self.assertAlmostEqual(ninfo["slope"], -0.25)

    def test_limit(self):
        x = sp.Symbol('x')
        expr = sp.sin(x) / x
        lim_sym, num_val = compute_limit(expr, 0)
        self.assertAlmostEqual(num_val, 1.0)


if __name__ == '__main__':
    unittest.main()
