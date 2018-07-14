import discord
from discord.ext import commands
import dice_roller


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
            result = dice_roller.rollCommandReturnResponse(argument)
            await client.send_message(message.channel, result)
        if args[0] == '/HELP':
            await client.send_message(message.channel, "Type: /roll 3d20+3")


    client.run(bot_token)

