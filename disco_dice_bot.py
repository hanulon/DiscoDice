import discord
from discord.ext import commands
import dice_roller


def get_bot_credentials(bot_creds_file):
    file = open(bot_creds_file, "r")
    read_lines = [line.strip() for line in file.readlines()]
    file.close()
    return read_lines


def respond_to_command(message):
    args = message.upper().split(" ")
    print(args)
    if args[0] == '/ROLL' or args[0] == '/R':
        argument = "".join(args[1:])
        return dice_roller.get_response_to_formula(argument)
    if args[0] == '/HELP':
        return "Type: /roll 3d20+3"
    return None


if __name__ == "__main__":
    Client = discord.Client()
    client = commands.Bot(command_prefix="?")
    [bot_token, _] = get_bot_credentials("bot_credentials.txt")

    @client.event
    async def on_ready():
        print("Dice rolling bot is ready!")

    @client.event
    async def on_message(message):
        response = respond_to_command(message.content)
        if response is not None:
            await client.send_message(message.channel, response)

    client.run(bot_token)

