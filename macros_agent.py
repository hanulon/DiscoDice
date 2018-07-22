
class MacrosAgent:
    def __init__(self):
        self.macros_in_memory = []

    def add_macro(self, commands, alias):
        if alias is None or commands is None:
            raise ValueError("Command/alias cannot be None")
        if alias.__len__() == 0 or commands.__len__() == 0:
            raise ValueError("Command/alias cannot be zero-length strings.")

        new_macro = {'alias': alias, 'command': commands}

        if new_macro['alias'] in [element['alias'] for element in self.macros_in_memory]:
            raise ValueError("There already exists macro with that alias.")

        self.macros_in_memory.append(new_macro)

    def forget_all_macros(self):
        self.macros_in_memory = []

    def forget_macro(self, macro_alias):
        macro_to_forget = self.find_macro(macro_alias)
        if macro_to_forget is not None:
            self.macros_in_memory.remove(macro_to_forget)

    def find_macro(self, macro_alias):
        list_of_aliases_in_memory = [element['alias'] for element in self.macros_in_memory]
        if macro_alias not in list_of_aliases_in_memory:
            return None
        return self.macros_in_memory[list_of_aliases_in_memory.index(macro_alias)]

    def redefine_macro(self, alias, commands):
        return None

    def get_macro_command(self, macro_alias):
        return None

    def load_macros_from_file(self, path):
        return None

    def save_macros_to_file(self, path):
        return None
