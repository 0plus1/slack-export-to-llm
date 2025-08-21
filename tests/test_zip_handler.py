import unittest
import zipfile
import os
from src.zip_handler import validate_zip_file, extract_users_json, extract_channel_json_files


class TestZipHandler(unittest.TestCase):
    def setUp(self):
        # Create a dummy zip file for testing
        self.zip_path = 'test_dummy.zip'
        with zipfile.ZipFile(self.zip_path, 'w') as z:
            z.writestr('users.json', '{}')
            z.writestr('testchannel/2025-01-01.json',
                       '[{"user_profile": {"display_name": "Test User"}, "text": "Hello"}]')

    def tearDown(self):
        if os.path.exists(self.zip_path):
            os.remove(self.zip_path)

    def test_validate_zip_file_valid(self):
        self.assertTrue(validate_zip_file(self.zip_path, 'testchannel'))

    def test_validate_zip_file_missing_users(self):
        # Create a zip file without users.json
        zip_path = 'test_no_users.zip'
        with zipfile.ZipFile(zip_path, 'w') as z:
            z.writestr('testchannel/2025-01-01.json',
                       '[{"user_profile": {"display_name": "User One"}, "text": "Hello"}]')
        self.assertFalse(validate_zip_file(zip_path, 'testchannel'))
        os.remove(zip_path)

    def test_extract_users_json(self):
        path = extract_users_json(self.zip_path)
        self.assertTrue(os.path.exists(path))

    def test_extract_channel_json_files(self):
        files = extract_channel_json_files(self.zip_path, 'testchannel')
        self.assertEqual(len(files), 1)
        self.assertTrue(os.path.exists(files[0]))


if __name__ == '__main__':
    unittest.main()
