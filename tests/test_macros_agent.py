from unittest import TestCase
import macros_agent as macros


class TestMacrosAgent(TestCase):
    def test_test(self):
        agent = macros.MacrosAgent()
        self.assertEqual(agent.test(), "test")