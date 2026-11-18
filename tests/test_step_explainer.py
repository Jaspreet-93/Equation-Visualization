import unittest
from app.math_engine import parse_math_expression
from app.step_explainer import (
    explain_roots,
    explain_derivative,
    explain_integration,
    explain_optimization,
)


class TestStepExplainer(unittest.TestCase):
    def test_explain_roots_quadratic(self):
        expr = parse_math_expression("x^2 - 5x + 6")
        text = explain_roots(expr)
        self.assertIn("Discriminant", text)
        self.assertIn("quadratic formula", text.lower())

    def test_explain_roots_linear(self):
        expr = parse_math_expression("2x - 8")
        text = explain_roots(expr)
        self.assertIn("Linear equation", text)

    def test_explain_derivative(self):
        expr = parse_math_expression("x^3 + sin(x)")
        text = explain_derivative(expr)
        self.assertIn("Power Rule", text)
        self.assertIn("f'(x)", text)

    def test_explain_integration(self):
        expr = parse_math_expression("x^2")
        text = explain_integration(expr)
        self.assertIn("Antiderivative", text)
        self.assertIn("Power Rule", text)

    def test_explain_optimization(self):
        expr = parse_math_expression("x^3 - 3x")
        text = explain_optimization(expr)
        self.assertIn("First Derivative", text)
        self.assertIn("Second Derivative", text)
        self.assertIn("Conclusion", text)


if __name__ == '__main__':
    unittest.main()
