import discord
from discord.ext import commands
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

def get_bot_credentials(bot_creds_file):
    file = open(bot_creds_file, "r")
    read_lines = [line.strip() for line in file.readlines()]
    file.close()
    return read_lines

if __name__ == "__main__":
    Client = discord.Client()
    client = commands.Bot(command_prefix="?")
    [bot_token, _] = get_bot_credentials("bot_credentials.txt")

    @client.event
    async def on_ready():
        print("Dice rolling bot is ready!")

    @client.event
    async def on_message(message):
        args = message.content.upper().split(" ")
        print(args)
        if args[0] == '/ROLL' or args[0] == '/R':
            argument = "".join(args[1:])
            result = rollCommandReturnResponse(argument)
            await client.send_message(message.channel, result)
        if args[0] == '/HELP':
            await client.send_message(message.channel, "Type: /roll 3d20+3")


    client.run(bot_token)
