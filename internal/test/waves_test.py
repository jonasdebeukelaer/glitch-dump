from internal.filters.waves import on_concentric_circle

import unittest


class TestStringMethods(unittest.TestCase):

    def test_on_concentric_circle_centre(self):
        self.assertTrue(on_concentric_circle(20, 20, 20, 20, 10, 1), "result fails at centre")

    def test_on_concentric_circle_symmetrical(self):
        a = [on_concentric_circle(x, 10, 20, 20, 10, 1) for x in range(1, 21)]
        b = [on_concentric_circle(x, 10, 20, 20, 10, 1) for x in range(20, 40)]
        b.reverse()
        self.assertEqual(a, b, "results not symmetric")

    def test_on_concentric_circle_normal(self):
        self.assertTrue(on_concentric_circle(6, 7, 10, 10, 5, 2))

    def test_on_concentric_circle_edge(self):
        self.assertTrue(on_concentric_circle(0, 20, 10, 20, 5, 2))

    def test_on_concentric_circle_odd_values(self):
        self.assertFalse(on_concentric_circle(1, 19, 91, 53, 110, 1))

    def test_on_concentric_circle_big_thickness(self):
        self.assertTrue(on_concentric_circle(1, 19, 91, 53, 11, 100))


if __name__ == '__main__':
    unittest.main()