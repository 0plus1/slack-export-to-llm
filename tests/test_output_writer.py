import unittest
import os
import json
from src.output_writer import write_output_json


class TestOutputWriter(unittest.TestCase):
    def setUp(self):
        self.output_file = 'test_output.json'
        self.data = [{"u": "Test User", "t": "Hello"}]

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_write_output_json(self):
        write_output_json(self.data, self.output_file)
        self.assertTrue(os.path.exists(self.output_file))
        with open(self.output_file, 'r') as f:
            loaded = json.load(f)
        self.assertEqual(loaded, self.data)


if __name__ == '__main__':
    unittest.main()
