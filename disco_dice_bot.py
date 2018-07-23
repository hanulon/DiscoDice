import discord
from discord.ext import commands
import dice_roller
import macros_agent


class DiscoDiceBot:
    def __init__(self, bot_credentials_file):
        self.bot_creds_file = bot_credentials_file
        self.macros_store_path = "my_macros.json"
        self.macros_agent = macros_agent.MacrosAgent()
        self.help_text = "Type: /roll 3d20+3"

    def run(self):
        Client = discord.Client()
        client = commands.Bot(command_prefix="?")

        @client.event
        async def on_ready():
            print("Dice rolling bot is ready!")

        @client.event
        async def on_message(message):
            response = self.respond_to_command(message.content)
            if response is not None:
                await client.send_message(message.channel, response)

        client.run(self.get_bot_token())

    def respond_to_command(self, message):
        command, *args = message.upper().split(" ")
        print(command, args)
        if command in ['/ROLL', '/R']:
            argument = "".join(args)
            return dice_roller.get_response_to_formula(argument)
        if command in ['/MACRO', '/MACROS', '/M']:
            return self.get_macros_command_response(args)
        if command in ['/HELP', '/H']:
            return self.help_text
        return None

    def get_macros_command_response(self, args):
        if args.__len__() == 0:
            return self.macros_agent.get_all_macros_aliases()
        elif args.__len__() == 1:
            if args[0] == 'CLEAR_ALL':
                self.macros_agent.forget_all_macros()
            elif args[0] == 'SAVE':
                self.macros_agent.save_macros_to_file(self.macros_store_path)
            elif args[0] == 'LOAD':
                self.macros_agent.load_macros_from_file(self.macros_store_path)
            else:
                return self.macros_agent.get_macro_command(args[0])
        else:
            if args[0] == 'DEFINE':
                self.macros_agent.define_macro(args[1], " ".join(args[2:]))
                return self.macros_agent.get_all_macros_aliases()
            if args[0] == 'REDEFINE':
                self.macros_agent.redefine_macro(args[1], " ".join(args[2:]))
                return self.macros_agent.get_all_macros_aliases()
            if args[0] == 'CLEAR':
                self.macros_agent.forget_macro(args[1])

    def get_bot_token(self):
        file = open(self.bot_creds_file, "r")
        read_line = file.readline()
        file.close()
        return read_line


if __name__ == "__main__":
    disco_bot = DiscoDiceBot("bot_credentials.txt")
    disco_bot.run()
