import unittest
import numpy as np
from app.math_engine import parse_math_expression
from app.plotter import generate_plot_data


class TestPlotter(unittest.TestCase):
    def test_generate_plot_data_shape(self):
        expr = parse_math_expression("x^2")
        X, Y = generate_plot_data(expr, xmin=-5.0, xmax=5.0, num=100)
        self.assertEqual(len(X), 100)
        self.assertEqual(len(Y), 100)
        self.assertTrue(np.all(np.isfinite(Y)))

    def test_generate_plot_data_handles_division_by_zero(self):
        expr = parse_math_expression("1/x")
        X, Y = generate_plot_data(expr, xmin=-2.0, xmax=2.0, num=41)
        # 1/0 should be handled without raising exceptions
        self.assertEqual(len(X), 41)
        self.assertEqual(len(Y), 41)


if __name__ == '__main__':
    unittest.main()
