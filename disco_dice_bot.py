import discord
from discord.ext import commands
import dice_roller
import macros_agent


class DiscoDiceBot(discord.Client):
    def __init__(self, bot_credentials_file):
        super().__init__()
        self.bot_creds_file = bot_credentials_file
        self.macros_store_path = "my_macros.json"
        self.macros_agent = macros_agent.MacrosAgent()
        self.help_text = "Welcome to the DiscoDiceBot! Every command starts with forward slash ( / ).\n" \
                         "Possible commands:\n" \
                         "/roll - allows you to roll the dice, with formula format as in roll20\n" \
                         "\tExample: /roll 3d20+3\n" \
                         "/macro - allows to define, use, list, save and clear the macros.\n" \
                         "\tExamples: (1) /macro (2) /macro define roll20 /roll d20, then type: /macro roll20.\n" \
                         "\tSubcommands: save, load, define, redefine, clear, clear all\n" \
                         "/help - shows this text."

    def run(self):
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
        if command == '/DIE':
            self.close()
        return None

    def get_macros_command_response(self, args):
        if args.__len__() == 0:
            return self.get_macros_in_memory_listed()
        elif args.__len__() == 1:
            if args[0] == 'SAVE':
                self.macros_agent.save_macros_to_file(self.macros_store_path)
            elif args[0] == 'LOAD':
                self.macros_agent.load_macros_from_file(self.macros_store_path)
            else:
                return self.macros_agent.get_macro_command(args[0])
        else:
            if args[0] == 'DEFINE':
                self.macros_agent.define_macro(args[1], " ".join(args[2:]))
                return self.get_macros_in_memory_listed()
            if args[0] == 'REDEFINE':
                self.macros_agent.redefine_macro(args[1], " ".join(args[2:]))
                return "Redefined macro: {0} to '{1}'.\n\n{2}".format(
                    args[1].lower(), " ".join(args[2:]).lower(), self.get_macros_in_memory_listed())
            if args[0] == 'CLEAR':
                if args[1] == 'ALL':
                    self.macros_agent.forget_all_macros()
                    return "Purged all macros from the memory."
                else:
                    self.macros_agent.forget_macro(args[1])
                    return self.get_macros_in_memory_listed()

    def get_macros_in_memory_listed(self):
        return "Macros in memory:\n" + "\n".join(m.lower() for m in self.macros_agent.get_all_macros_aliases())

    def get_bot_token(self):
        file = open(self.bot_creds_file, "r")
        read_line = file.readline().replace("\n", "")
        file.close()
        return read_line


if __name__ == "__main__":
    disco_bot = DiscoDiceBot("bot_credentials.txt")
    disco_bot.run()
