import unittest
from app.math_engine import parse_math_expression
from app.optimization import (
    find_critical_points,
    find_inflection_points,
    find_global_extrema,
)


class TestOptimization(unittest.TestCase):
    def test_cubic_extrema(self):
        expr = parse_math_expression("x^3 - 3x")
        cps = find_critical_points(expr)
        self.assertEqual(len(cps), 2)

        # Local Maximum at x = -1, y = 2
        self.assertAlmostEqual(cps[0]["x"], -1.0)
        self.assertAlmostEqual(cps[0]["y"], 2.0)
        self.assertEqual(cps[0]["nature"], "Local Maximum")

        # Local Minimum at x = 1, y = -2
        self.assertAlmostEqual(cps[1]["x"], 1.0)
        self.assertAlmostEqual(cps[1]["y"], -2.0)
        self.assertEqual(cps[1]["nature"], "Local Minimum")

    def test_parabola_minimum(self):
        expr = parse_math_expression("x^2 - 4x + 5")
        cps = find_critical_points(expr)
        self.assertEqual(len(cps), 1)
        self.assertAlmostEqual(cps[0]["x"], 2.0)
        self.assertAlmostEqual(cps[0]["y"], 1.0)
        self.assertEqual(cps[0]["nature"], "Local Minimum")

    def test_inflection_point(self):
        expr = parse_math_expression("x^3")
        inflections = find_inflection_points(expr)
        self.assertEqual(len(inflections), 1)
        self.assertAlmostEqual(inflections[0]["x"], 0.0)
        self.assertAlmostEqual(inflections[0]["y"], 0.0)

    def test_global_extrema_on_interval(self):
        expr = parse_math_expression("x^2")
        extrema = find_global_extrema(expr, -2.0, 3.0)
        self.assertAlmostEqual(extrema["global_min"]["y"], 0.0)
        self.assertAlmostEqual(extrema["global_max"]["y"], 9.0)


if __name__ == '__main__':
    unittest.main()
