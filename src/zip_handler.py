from src.console import printError
import zipfile
import os
import tempfile
from typing import List


def extract_users_json(zip_path: str) -> str:
    """
    Extracts users.json from the zip archive to a temporary directory.
    Returns the path to the extracted users.json file.
    Raises FileNotFoundError if users.json is not found.
    """
    with zipfile.ZipFile(zip_path, 'r') as z:
        user_json_candidates = [
            f for f in z.namelist() if f.endswith('users.json')]
        if not user_json_candidates:
            raise FileNotFoundError("users.json not found in zip archive.")
        temp_dir = tempfile.mkdtemp()
        out_path = os.path.join(temp_dir, 'users.json')
        with z.open(user_json_candidates[0]) as src, open(out_path, 'wb') as dst:
            dst.write(src.read())
        return out_path


"""
Handles extraction of channel JSON files from a Slack export zip.
"""


def validate_zip_file(zip_path: str, channel_name: str) -> bool:
    """
    Validates that users.json and the target channel folder exist in the zip archive.
    Returns True if both exist, False otherwise.
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            namelist = z.namelist()
            # Check for users.json
            has_users_json = any(f.endswith('users.json') for f in namelist)
            # Check for channel folder
            top_level_folders = set(f.split('/')[0]
                                    for f in namelist if '/' in f)
            has_channel = channel_name in top_level_folders
            if not has_users_json:
                printError("Error: users.json not found in zip archive.")
            if not has_channel:
                printError(
                    f"Error: Channel '{channel_name}' not found in zip. Available channels: {sorted(top_level_folders)}")
            return has_users_json and has_channel
    except zipfile.BadZipFile:
        printError("Error: Provided file is not a valid zip archive.")
        return False


def extract_channel_json_files(zip_path: str, channel_name: str) -> List[str]:
    """
    Extracts all JSON files for the given channel from the zip archive.
    Returns a list of file paths to the extracted JSON files.
    """
    extracted_files = []
    with zipfile.ZipFile(zip_path, 'r') as z:
        # List all top-level folders in the zip
        top_level_folders = set(f.split('/')[0]
                                for f in z.namelist() if '/' in f)
        if channel_name not in top_level_folders:
            printError(
                f"Error: Channel '{channel_name}' not found in zip. Available channels: {sorted(top_level_folders)}")
            return []
        # Find all files in the channel folder
        channel_prefix = f"{channel_name}/"
        json_names = [f for f in z.namelist() if f.startswith(
            channel_prefix) and f.endswith('.json')]
        if not json_names:
            print(
                f"Error: No JSON files found for channel '{channel_name}' in zip.")
            return []
        for name in json_names:
            temp_dir = tempfile.mkdtemp()
            out_path = os.path.join(temp_dir, os.path.basename(name))
            with z.open(name) as src, open(out_path, 'wb') as dst:
                dst.write(src.read())
            extracted_files.append(out_path)
    return extracted_files
