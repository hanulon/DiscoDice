import json


class MacrosAgent:
    def __init__(self):
        self.macros_in_memory = {}

    def define_macro(self, alias, commands):
        if alias is None or commands is None:
            raise ValueError("Command/alias cannot be None")
        if alias.__len__() == 0 or commands.__len__() == 0:
            raise ValueError("Command/alias cannot be zero-length strings.")
        if alias in self.get_all_macros_aliases():
            raise ValueError("There already exists macro with that alias.")

        self.macros_in_memory[alias] = commands

    def forget_all_macros(self):
        self.macros_in_memory = {}

    def get_all_macros_aliases(self):
        return list(self.macros_in_memory.keys())

    def forget_macro(self, macro_alias):
        if macro_alias in self.get_all_macros_aliases():
            self.macros_in_memory.pop(macro_alias)
            return True
        return False

    def redefine_macro(self, alias, commands):
        if alias in self.get_all_macros_aliases():
            self.macros_in_memory[alias] = commands
            return True
        return False

    def get_macro_command(self, macro_alias):
        if macro_alias in self.get_all_macros_aliases():
            return self.macros_in_memory[macro_alias]
        return None

    def save_macros_to_file(self, path):
        js = json.dumps(self.macros_in_memory)
        f_out = open(path, "w")
        f_out.write(js)
        f_out.close()

    def load_macros_from_file(self, path):
        f_in = open(path, "r")
        js = json.load(f_in)
        f_in.close()
        self.macros_in_memory = js

    def get_all_macros(self):
        return self.macros_in_memory
