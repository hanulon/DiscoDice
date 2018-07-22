from unittest import TestCase
import macros_agent as macros
import os


class TestMacrosAgent(TestCase):
    def test_define_macro_should_add_element_to_macro_list(self):
        agent = macros.MacrosAgent()
        new_macro = ["stamina_roll", "/roll 4d10"]

        agent.define_macro(new_macro[0], new_macro[1])

        self.assertEqual("/roll 4d10", agent.macros_in_memory["stamina_roll"])

    def test_define_macro_should_raise_exception_on_missing_alias_or_commands(self):
        agent = macros.MacrosAgent()
        new_macro = ["stamina_roll", "/roll 4d10"]

        with self.assertRaises(expected_exception=ValueError):
            agent.define_macro(None, new_macro[0])
        with self.assertRaises(expected_exception=ValueError):
            agent.define_macro("", new_macro[0])
        with self.assertRaises(expected_exception=ValueError):
            agent.define_macro(new_macro[1], "")

    def test_define_macro_should_raise_exception_on_duplicating_aliases(self):
        agent = macros.MacrosAgent()
        new_macro = ["stamina_roll", "/roll 4d10"]

        agent.define_macro(new_macro[0], new_macro[1])

        with self.assertRaises(expected_exception=ValueError):
            agent.define_macro(new_macro[0], "whatever")

    def test_forget_all_macros(self):
        agent = macros.MacrosAgent()
        new_macro1 = ["stamina_roll", "/roll 4d10"]
        new_macro2 = ["stamina_rolls", "/roll 4d10"]

        agent.define_macro(new_macro1[0], new_macro1[1])
        agent.define_macro(new_macro2[0], new_macro2[1])
        size_pre_purge = agent.macros_in_memory.__len__()
        agent.forget_all_macros()

        self.assertEqual(2, size_pre_purge)
        self.assertEqual({}, agent.macros_in_memory)

    def test_forget_macro(self):
        agent = macros.MacrosAgent()
        new_macro1 = ["stamina_roll", "/roll 4d10"]
        new_macro2 = ["strength_roll", "/roll 4d104"]
        macro_alias_to_forget = "stamina_roll"

        agent.define_macro(new_macro1[0], new_macro1[1])
        agent.define_macro(new_macro2[0], new_macro2[1])
        forgot_macro = agent.forget_macro(macro_alias_to_forget)

        self.assertEqual(1, agent.macros_in_memory.__len__())
        self.assertTrue(forgot_macro)
        with self.assertRaises(expected_exception=KeyError):
            agent.macros_in_memory[macro_alias_to_forget]

    def test_redefine_macro(self):
        agent = macros.MacrosAgent()
        new_macro1 = ["stamina_roll", "/roll 4d10"]
        new_macro2 = ["stamina_roll", "/roll 4d104"]

        agent.define_macro(new_macro1[0], new_macro1[1])
        is_redefined = agent.redefine_macro(new_macro2[0], new_macro2[1])

        self.assertTrue(is_redefined)
        self.assertEqual("/roll 4d104", agent.macros_in_memory["stamina_roll"])

    def test_get_macro_command(self):
        agent = macros.MacrosAgent()
        new_macro = ["stamina_roll", "/roll 4d10"]

        agent.define_macro(new_macro[0], new_macro[1])
        command = agent.get_macro_command(new_macro[0])

        self.assertEqual("/roll 4d10", command)

    def test_get_macro_command_should_return_none_if_not_found(self):
        agent = macros.MacrosAgent()
        new_macro = ["stamina_roll", "/roll 4d10"]

        command = agent.get_macro_command(new_macro[0])

        self.assertEqual(None, command)

    def test_save_macros_to_file(self):
        agent = macros.MacrosAgent()
        new_macro1 = ["stamina_roll", "/roll 4d10"]
        new_macro2 = ["sss", "/roll 10d4"]
        filename = "test_file.json"

        agent.define_macro(new_macro1[0], new_macro1[1])
        agent.define_macro(new_macro2[0], new_macro2[1])
        agent.save_macros_to_file(filename)

        f = open(filename, "r")
        result = f.readline()
        f.close()
        os.remove(filename)

        self.assertEqual('{"stamina_roll": "/roll 4d10", "sss": "/roll 10d4"}', result)

    def test_load_macros_from_file(self):
        agent = macros.MacrosAgent()
        new_macro1 = ["stamina_roll", "/roll 4d10"]
        new_macro2 = ["sss", "/roll 10d4"]
        filename = "test_file.json"

        agent.define_macro(new_macro1[0], new_macro1[1])
        agent.define_macro(new_macro2[0], new_macro2[1])
        expected_dict = agent.macros_in_memory

        agent.save_macros_to_file(filename)
        agent.load_macros_from_file(filename)
        os.remove(filename)

        self.assertEqual(expected_dict, agent.macros_in_memory)