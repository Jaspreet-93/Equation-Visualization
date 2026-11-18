import unittest
import sympy as sp
from app.math_engine import parse_math_expression, find_roots, evaluate_at, x


class TestMathEngine(unittest.TestCase):
    def test_parse_simple_polynomial(self):
        expr = parse_math_expression("x^2 - 5x + 6")
        self.assertEqual(expr, x**2 - 5*x + 6)

    def test_parse_implicit_multiplication(self):
        expr = parse_math_expression("2x + 3(x - 1)")
        self.assertEqual(expr, 2*x + 3*(x - 1))

    def test_parse_equation_syntax(self):
        expr = parse_math_expression("x^2 = 9")
        self.assertEqual(expr, x**2 - 9)

    def test_parse_trig_functions(self):
        expr = parse_math_expression("sin(x) + cos(x)")
        self.assertEqual(expr, sp.sin(x) + sp.cos(x))

    def test_find_roots_quadratic(self):
        expr = parse_math_expression("x^2 - 5x + 6")
        roots = find_roots(expr, domain="reals")
        root_vals = [r[1] for r in roots]
        self.assertEqual(len(roots), 2)
        self.assertAlmostEqual(root_vals[0], 2.0)
        self.assertAlmostEqual(root_vals[1], 3.0)

    def test_find_roots_no_real_roots(self):
        expr = parse_math_expression("x^2 + 4")
        roots = find_roots(expr, domain="reals")
        self.assertEqual(len(roots), 0)

    def test_evaluate_at(self):
        expr = parse_math_expression("3x^2 - 2x + 1")
        val = evaluate_at(expr, 2.0)
        self.assertAlmostEqual(val, 9.0)

    def test_empty_expression_raises_value_error(self):
        with self.assertRaises(ValueError):
            parse_math_expression("   ")


if __name__ == '__main__':
    unittest.main()
