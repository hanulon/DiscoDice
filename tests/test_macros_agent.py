from unittest import TestCase
import macros_agent as macros


class TestMacrosAgent(TestCase):
    def test_add_macro_should_add_element_to_macro_list(self):
        agent = macros.MacrosAgent()
        new_macro = ["stamina_roll", "/roll 4d10"]

        agent.add_macro(new_macro[1], new_macro[0])

        self.assertEqual(agent.macros_in_memory[0], {'alias': new_macro[0], 'command': new_macro[1]})

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

        self.assertEqual(agent.macros_in_memory[0]['alias'], "stamina_roll")
        self.assertEqual(agent.macros_in_memory[0]['command'], "/roll 4d10")

    def test_add_macro_should_raise_exception_on_duplicating_aliases(self):
        agent = macros.MacrosAgent()
        new_macro = ["stamina_roll", "/roll 4d10"]

        agent.add_macro(new_macro[1], new_macro[0])

        with self.assertRaises(expected_exception=ValueError):
            agent.add_macro("whatever", new_macro[0])
