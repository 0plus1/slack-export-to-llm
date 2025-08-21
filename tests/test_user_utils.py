import unittest
from src.user_utils import load_user_map, replace_pings
import os
import json


class TestUserUtils(unittest.TestCase):
    def setUp(self):
        self.users_file = 'test_users.json'
        with open(self.users_file, 'w') as f:
            json.dump([
                {"id": "U123", "profile": {"display_name": "Pinged User"}},
                {"id": "U456", "profile": {"display_name": "Another User"}}
            ], f)

    def tearDown(self):
        os.remove(self.users_file)

    def test_load_user_map(self):
        user_map = load_user_map(self.users_file)
        self.assertEqual(user_map['U123'], 'Pinged User')
        self.assertEqual(user_map['U456'], 'Another User')

    def test_replace_pings(self):
        user_map = load_user_map(self.users_file)
        text = 'Hello <@U123> and <@U456>'
        replaced = replace_pings(text, user_map)
        self.assertIn('@Pinged User', replaced)
        self.assertIn('@Another User', replaced)


if __name__ == '__main__':
    unittest.main()
