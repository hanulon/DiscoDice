from unittest import TestCase
import macros_agent as macros


class TestMacrosAgent(TestCase):
    def test_add_macro_should_add_element_to_macro_list(self):
        agent = macros.MacrosAgent()
        new_macro = ["stamina_roll", "/roll 4d10"]

        agent.add_macro(new_macro[1], new_macro[0])

        self.assertEqual({'alias': new_macro[0], 'command': new_macro[1]}, agent.macros_in_memory[0])

    def test_add_macro_should_raise_exception_on_missing_alias_or_commands(self):
        agent = macros.MacrosAgent()
        new_macro = ["stamina_roll", "/roll 4d10"]

        with self.assertRaises(expected_exception=ValueError):
            agent.add_macro(None, new_macro[0])
        with self.assertRaises(expected_exception=ValueError):
            agent.add_macro("", new_macro[0])
        with self.assertRaises(expected_exception=ValueError):
            agent.add_macro(new_macro[1], "")

    def test_add_macro_should_element_be_dictionary(self):
        agent = macros.MacrosAgent()
        new_macro = ["stamina_roll", "/roll 4d10"]

        agent.add_macro(new_macro[1], new_macro[0])

        self.assertEqual("stamina_roll", agent.macros_in_memory[0]['alias'])
        self.assertEqual("/roll 4d10", agent.macros_in_memory[0]['command'])

    def test_add_macro_should_raise_exception_on_duplicating_aliases(self):
        agent = macros.MacrosAgent()
        new_macro = ["stamina_roll", "/roll 4d10"]

        agent.add_macro(new_macro[1], new_macro[0])

        with self.assertRaises(expected_exception=ValueError):
            agent.add_macro("whatever", new_macro[0])

    def test_forget_all_macros(self):
        agent = macros.MacrosAgent()
        new_macro1 = ["stamina_roll", "/roll 4d10"]
        new_macro2 = ["stamina_rolls", "/roll 4d10"]

        agent.add_macro(new_macro1[1], new_macro1[0])
        agent.add_macro(new_macro2[1], new_macro2[0])
        size_pre_purge = agent.macros_in_memory.__len__()
        agent.forget_all_macros()

        self.assertEqual(2, size_pre_purge)
        self.assertEqual([], agent.macros_in_memory)

    def test_forget_macro(self):
        agent = macros.MacrosAgent()
        new_macro1 = ["stamina_roll", "/roll 4d10"]
        new_macro2 = ["strength_roll", "/roll 4d10"]
        macro_alias_to_forget = "stamina_roll"

        agent.add_macro(new_macro1[1], new_macro1[0])
        agent.add_macro(new_macro2[1], new_macro2[0])
        agent.forget_macro(macro_alias_to_forget)

        self.assertEqual(1, agent.macros_in_memory.__len__())
        self.assertEqual("strength_roll", agent.macros_in_memory[0]['alias'])

    def test_find_macro(self):
        agent = macros.MacrosAgent()
        new_macro1 = ["stamina_roll", "/roll 4d10"]
        new_macro2 = ["strength_roll", "/roll 4d10"]
        macro_alias_to_find = "strength_roll"

        agent.add_macro(new_macro1[1], new_macro1[0])
        agent.add_macro(new_macro2[1], new_macro2[0])
        macro = agent.find_macro(macro_alias_to_find)

        self.assertEqual({'alias': "strength_roll", 'command': "/roll 4d10"}, macro)
