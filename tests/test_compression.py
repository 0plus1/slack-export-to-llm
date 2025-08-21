import unittest
import os
import json
from src.message_parser import parse_messages

class TestCompression(unittest.TestCase):
    def setUp(self):
        self.json_file = 'test_compress.json'
        self.users_file = 'test_users.json'
        # Message includes a common Slack system message
        with open(self.json_file, 'w') as f:
            json.dump([
                {"user_profile": {"display_name": "User One"}, "text": "User One has joined the channel"},
                {"user_profile": {"display_name": "User Two"}, "text": "Hello world"}
            ], f)
        with open(self.users_file, 'w') as f:
            json.dump([
                {"id": "U00000001", "profile": {"display_name": "User One"}},
                {"id": "U00000002", "profile": {"display_name": "User Two"}}
            ], f)

    def tearDown(self):
        os.remove(self.json_file)
        os.remove(self.users_file)

    def test_compression_removes_common_messages(self):
        msgs = parse_messages([self.json_file], self.users_file, compress=True)
        texts = [m['t'] for m in msgs]
        self.assertNotIn('User One has joined the channel', texts)
        self.assertIn('Hello world', texts)

if __name__ == '__main__':
    unittest.main()
