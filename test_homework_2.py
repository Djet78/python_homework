import homework_2 as hw
import unittest


class TestTask1(unittest.TestCase):

    # ------- Task 1 --------
    def test_empty_iterable(self):
        self.assertEqual(hw.not_occur_number_in([]), 1)

    def test_len_1_iterable(self):
        self.assertEqual(hw.not_occur_number_in([2]), 3)

    def test_list_of_negatives(self):
        self.assertEqual(hw.not_occur_number_in([-1, -3]), 1)

    def test_right_sequence(self):
        self.assertEqual(hw.not_occur_number_in([1, 2, 3]), 4)

    def test_missed_item(self):
        self.assertEqual(hw.not_occur_number_in([1, 2, 3, 4, 7, 6]), 5)

    def test_big_diff(self):
        self.assertEqual(hw.not_occur_number_in([1, 20]), 2)


class TestTask6(unittest.TestCase):

    def test_empty_str(self):
        self.assertEqual(hw.is_nested(""), 0)

    def test_closing_parentheses(self):
        self.assertEqual(hw.is_nested("))))"), 0)

    def test_opening_parentheses(self):
        self.assertEqual(hw.is_nested("((("), 0)

    def test_closing_opening_parentheses(self):
        self.assertEqual(hw.is_nested("))))))((("), 0)

    def test_len_3_str(self):
        self.assertEqual(hw.is_nested("()("), 0)

    def test_incorrect_str(self):
        self.assertEqual(hw.is_nested("))))))))())"), 0)

    def test_correct_str_1(self):
        self.assertEqual(hw.is_nested("((()))"), 1)

    def test_correct_str_2(self):
        self.assertEqual(hw.is_nested("(((((((())"), 1)

    def test_correct_str_3(self):
        self.assertEqual(hw.is_nested("()()()"), 1)

    def test_type_err(self):
        with self.assertRaises(TypeError):
            hw.is_nested(22)

    def test_type_err2(self):
        self.assertRaises(TypeError, hw.is_nested, [])


if __name__ == "__main__":
    unittest.main()
