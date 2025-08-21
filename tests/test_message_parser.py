import unittest
import os
import json
from src.message_parser import parse_messages


class TestMessageParser(unittest.TestCase):
    def setUp(self):
        # Create dummy JSON files
        self.json_file = 'test_msg.json'
        self.users_file = 'test_users.json'
        with open(self.json_file, 'w') as f:
            json.dump([
                {"user_profile": {"display_name": "Test User"},
                    "text": "Hello <@U123>"}
            ], f)
        with open(self.users_file, 'w') as f:
            json.dump([
                {"id": "U123", "profile": {"display_name": "Pinged User"}}
            ], f)

    def tearDown(self):
        os.remove(self.json_file)
        os.remove(self.users_file)

    def test_parse_messages(self):
        msgs = parse_messages([self.json_file], self.users_file)
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0]['u'], 'Test User')
        self.assertIn('Pinged User', msgs[0]['t'])


if __name__ == '__main__':
    unittest.main()
