import unittest

from task1.solution import sum_int, sum_bool, sum_bool_int, sum_intchar_str, concat


class TestAddFunction(unittest.TestCase):
    def test_sum_two(self):
        self.assertEqual(sum_int(2, 3), 5)
        self.assertEqual(sum_int(2, b=3), 5)
        self.assertEqual(sum_int(a=2, b=3), 5)
        self.assertEqual(sum_int(b=2, a=3), 5)

        self.assertEqual(sum_intchar_str(1, "1"), 2)
        self.assertEqual(sum_intchar_str(1, b="1"), 2)
        self.assertEqual(sum_intchar_str(a=1, b="1"), 2)
        self.assertEqual(sum_intchar_str(b="1", a=1), 2)

        self.assertEqual(concat("1", "2"), "12")
        self.assertEqual(concat("1", b="2"), "12")
        self.assertEqual(concat(a="1", b="2"), "12")
        self.assertEqual(concat(b="2", a="1"), "12")

        with self.assertRaises(TypeError):
            sum_int("1", "2")
            sum_int("1", 0)
            sum_int(0, "2")
            sum_int(True, False)
            sum_int(b=1, a="1")
            sum_int(1.0, 1.2), 2.2