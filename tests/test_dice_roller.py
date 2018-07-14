from unittest import TestCase
import dice_roller as dr


class TestGet_response_to_formula(TestCase):
    def test_if_result_is_string(self):
        formula = "3d10+5+6d4+d3"
        result = dr.get_response_to_formula(formula)
        print(result)
        self.assertTrue(isinstance(result, type("string")))


class TestApply_complex_dice_rolls_formula(TestCase):

    def test_result_list_length_should_equal_formula_items(self):
        argument = "3d10+5+6d4+d3"
        formula_results = dr.apply_complex_dice_rolls_formula(argument)
        self.assertEqual(formula_results.__len__(), 4)

    def test_result_list_length_should_equal_formula_items_with_whitespaces(self):
        argument = "3d10+ 5 + 6d4 +d3"
        formula_results = dr.apply_complex_dice_rolls_formula(argument)
        self.assertEqual(formula_results.__len__(), 4)

    def test_result_list_should_raise_error_on_dice_with_minuses(self):
        argument = "3d10+5-6d4-d3"
        with self.assertRaises(expected_exception=ArithmeticError):
            dr.apply_complex_dice_rolls_formula(argument)

    def test_result_list_should_get_negative_values_on_fixed_values_with_minuses(self):
        argument = "3d4-9-10+2d4-10+d3+12-3-4-5"
        formula_results = dr.apply_complex_dice_rolls_formula(argument)
        self.assertEqual(formula_results[1], -9)
        self.assertEqual(formula_results[2], -10)
        self.assertEqual(formula_results[4], -10)
        self.assertEqual(formula_results[6], 12)
        self.assertEqual(formula_results[7], -3)
        self.assertEqual(formula_results[8], -4)
        self.assertEqual(formula_results[9], -5)


class TestApply_simple_dice_roll_formula(TestCase):
    def test_should_return_value_if_argument_is_int(self):
        coded_dice = "+10"
        value = dr.apply_simple_dice_roll_formula(coded_dice)
        self.assertEqual(value, 10)

    def test_should_return_negative_value_if_argument_is_negative_int(self):
        coded_dice = "-10"
        value = dr.apply_simple_dice_roll_formula(coded_dice)
        self.assertEqual(value, -10)

    def test_should_return_correct_list_of_results_length(self):
        coded_dice = "4D10"
        dice_list = dr.apply_simple_dice_roll_formula(coded_dice)
        self.assertEqual(dice_list.__len__(), 4)

    def test_should_return_list_with_one_element(self):
        coded_dice = "D10"
        dice_list = dr.apply_simple_dice_roll_formula(coded_dice)
        self.assertEqual(dice_list.__len__(), 1)

    def test_should_raise_exception_on_wrong_dice_number(self):
        coded_dice = "XD10"
        with self.assertRaises(expected_exception=ValueError):
            dr.apply_simple_dice_roll_formula(coded_dice)

    def test_should_raise_exception_on_wrong_sides(self):
        coded_dice = "DH"
        with self.assertRaises(expected_exception=ValueError):
            dr.apply_simple_dice_roll_formula(coded_dice)

    def test_should_raise_exception_on_too_many_d(self):
        coded_dice = "3d10d3"
        with self.assertRaises(expected_exception=SyntaxError):
            dr.apply_simple_dice_roll_formula(coded_dice)

    def test_with_whitespaces(self):
        coded_dice = "3 d 10"
        dice_list = dr.apply_simple_dice_roll_formula(coded_dice)
        self.assertEqual(dice_list.__len__(), 3)


class TestRoll_dice_n_times(TestCase):
    def test_should_be_n_results(self):
        num_of_dice = 3
        sides_of_dice = 10
        rolled_results = dr.roll_dice_n_times(num_of_dice, sides_of_dice)
        self.assertEqual(rolled_results.__len__(), num_of_dice)

    def test_should_raise_exception_if_wrong_number_of_dice(self):
        num_of_dice = 0
        sides_of_dice = 10
        with self.assertRaises(expected_exception=ValueError):
            dr.roll_dice_n_times(num_of_dice, sides_of_dice)


class TestRoll_dice(TestCase):
    def test_result_within_range(self):
        dice_sides = 4
        die_result = dr.roll_dice(dice_sides)
        self.assertGreater(die_result, 0)
        self.assertLessEqual(die_result, dice_sides)

    def test_should_throw_exception_on_wrong_number_of_sides(self):
        dice_sides = 1
        with self.assertRaises(expected_exception=ValueError):
            dr.roll_dice(dice_sides)

