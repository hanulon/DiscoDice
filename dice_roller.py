from random import randint


def get_response_to_formula(formula):
    dice_results = apply_complex_dice_rolls_formula(formula)
    results_string = []
    result_sum = 0
    for rolls in dice_results:
        string_result, int_result = extract_formula_response_from_results_list(rolls)
        results_string.append(string_result)
        result_sum += int_result
    shown_each_dice_response = " + ".join(results_string)
    response = "rolled %s :\n%s = %d" % (formula.lower(), shown_each_dice_response, result_sum)
    return response


def extract_formula_response_from_results_list(results):
    if isinstance(results, list):
        subformula = " + ".join([str(die_result) for die_result in results])
        return "(%s)" % subformula, sum(results)
    return "%s" % results, results


def apply_complex_dice_rolls_formula(argument):
    dice_plus_separated = argument.split("+")
    dice_set = []
    for dp in dice_plus_separated:
        dice_set += separate_dice_formulas_containing_minus(dp)
    dice_results = []
    for dice in dice_set:
        out_d = apply_simple_dice_roll_formula(dice)
        dice_results.append(out_d)
    return dice_results


def separate_dice_formulas_containing_minus(roll_formula):
    dice_after_minus = roll_formula.split("-")
    dice_minus_separated = [dice_after_minus[0]]
    for i in range(1, dice_after_minus.__len__()):
        if 'd' in dice_after_minus[i]:
            raise ArithmeticError("Dice roll result cannot be treated as a negative value.")
        else:
            dice_minus_separated.append("-%s" % dice_after_minus[i])
    return dice_minus_separated


def apply_simple_dice_roll_formula(dice_coded):
    dice_coded = dice_coded.lower()
    if 'd' in dice_coded:
        ddd = dice_coded.split("d")
        if ddd.__len__() > 2:
            raise SyntaxError("Too many d's in dice_coded: %s" % dice_coded)
        sides_of_die = int(ddd[1])
        if ddd[0].__len__() == 0:
            number_of_dies = 1
        else:
            number_of_dies = int(ddd[0])
        return roll_dice_n_times(number_of_dies, sides_of_die)
    else:
        return int(dice_coded)


def roll_dice_n_times(n, sides_number):
    if n < 1:
        raise ValueError("There must be at least one dice to throw")
    rolls_results = []
    for i in range(n):
        out_one_d = roll_dice(sides_number)
        rolls_results.append(out_one_d)
    return rolls_results


def roll_dice(sides_number):
    if sides_number < 2:
        raise ValueError("Dice must have at least 2 sides. Given sides_number: %d" % sides_number)
    return randint(1, sides_number)