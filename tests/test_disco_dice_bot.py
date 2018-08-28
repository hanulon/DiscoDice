from unittest import TestCase
import disco_dice_bot as disco
import os


class TestDiscoDiceBot(TestCase):
    def test_get_bot_token(self):
        bot_credentials_filename = "bot_credentials.txt"
        file_creds = open(bot_credentials_filename, "w")
        file_creds.write("testing_bot_token")
        file_creds.close()

        ddbot = disco.DiscoDiceBot(bot_credentials_filename)
        result = ddbot.get_bot_token()
        os.remove(bot_credentials_filename)

        self.assertEqual("testing_bot_token", result)

    def test_respond_to_command_roll(self):
        ddbot = disco.DiscoDiceBot("test_string")
        formula = "3d10+12+d4"
        command = "/roll " + formula

        response = ddbot.respond_to_command(command)

        self.assertTrue("rolled "+formula in response)

    def test_respond_to_command_macro_without_arguments(self):
        ddbot = disco.DiscoDiceBot("test_string")
        command = "/MACRO"
        expected = "Macros in memory:\nroll20 :\t/roll d20"

        ddbot.get_macros_command_response(["DEFINE", "ROLL20", "/roll d20"])
        response = ddbot.respond_to_command(command)

        self.assertEqual(expected, response)

    def test_get_macros_command_response_on_macro(self):
        ddbot = disco.DiscoDiceBot("test_string")
        arguments = ["ROLL20"]
        expected = "/roll d20"

        ddbot.get_macros_command_response(["DEFINE", "ROLL20", "/roll d20"])
        response = ddbot.get_macros_command_response(arguments)

        self.assertEqual(expected, response)

    def test_get_macros_command_response_on_clear_all(self):
        ddbot = disco.DiscoDiceBot("test_string")
        arguments = ["CLEAR", "ALL"]
        expected_response = "Purged all macros from the memory."
        expected_macros_listing = "Macros in memory:"

        ddbot.get_macros_command_response(["DEFINE", "ROLL20", "/roll d20"])
        actual_response = ddbot.get_macros_command_response(arguments)
        actual_macros_listing = ddbot.respond_to_command("/MACRO")

        self.assertEqual(expected_response, actual_response)
        self.assertEqual(expected_macros_listing, actual_macros_listing)

    # TODO
    #def test_get_macros_command_response_on_save_macros(self):
    #def test_get_macros_command_response_on_load_macros(self):

    def test_get_macros_command_response_on_define(self):
        ddbot = disco.DiscoDiceBot("test_string")
        arguments = ["DEFINE", "ROLL20", "/roll d20"]
        expected_response = "Macros in memory:\nroll20"

        actual_response = ddbot.get_macros_command_response(arguments)

        self.assertEqual(expected_response, actual_response)

    def test_get_macros_command_response_on_redefine(self):
        ddbot = disco.DiscoDiceBot("test_string")
        arguments = ["REDEFINE", "ROLL20", "/roll 2d4"]
        expected_response = "Redefined macro: roll20 to '/roll 2d4'.\n\nMacros in memory:\nroll20"

        ddbot.get_macros_command_response(["DEFINE", "ROLL20", "/roll d20"])
        actual_response = ddbot.get_macros_command_response(arguments)

        self.assertEqual(expected_response, actual_response)

    def test_get_macros_command_response_on_clear(self):
        ddbot = disco.DiscoDiceBot("test_string")
        arguments = ["CLEAR", "ROLL20"]
        expected_response = "Macros in memory:"

        ddbot.get_macros_command_response(["DEFINE", "ROLL20", "/roll d20"])
        actual_response = ddbot.get_macros_command_response(arguments)

        self.assertEqual(expected_response, actual_response)
