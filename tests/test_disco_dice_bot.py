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