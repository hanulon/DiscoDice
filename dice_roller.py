from random import randint


def rollCommandReturnResponse(argument):
    dies = argument.split("+")
    dice_results = []
    try:
        for dice in dies:
            out_d = getRollSubresult(dice)
            dice_results.append(out_d)
        print(dice_results)
        result = "rolled  %s\n" % argument.lower()
        results_string = []
        result_int = []
        for rolls in dice_results:
            if isinstance(rolls, list):
                subroll = " + ".join([str(die_result) for die_result in rolls])
                subroll = "(%s)" % subroll
                results_string.append(subroll)
                result_int.append(sum(rolls))
            else:
                results_string.append(str(rolls))
                result_int.append(rolls)
        result += " + ".join(results_string)
        result += " = %d" % sum(result_int)
        return result
    except:
        return "There was an error with the command."

def getRollSubresult(dice_coded):
    if 'D' in dice_coded:
        ddd = dice_coded.split("D")
        try:
            sides_of_die = int(ddd[1])
            if sides_of_die < 2:
                raise ValueError('Dice cannot have sides: %d' % sides_of_die)
        except:
            raise ValueError('Dice cannot have sides: %s' % (ddd[1]))
        if ddd[0].__len__() == 0:
            number_of_dies = 1
        else:
            try:
                number_of_dies = int(ddd[0])
            except:
                raise ValueError('Forbidden number of dies: %s' % (ddd[0]))
        return rollNDies(number_of_dies, sides_of_die)
    else:
        return int(dice_coded)

def rollNDies(N, sides_number):
    rolls_results = []
    for i in range(N):
        out_one_d = rollDiceOnce(sides_number)
        rolls_results.append(out_one_d)
    return rolls_results

def rollDiceOnce(sides_number):
    return randint(1, sides_number)