
class MacrosAgent:
    def __init__(self):
        self.macros_store_filename = 'macros_store.txt'
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
