"""
Parses messages from extracted Slack channel JSON files.
"""
import json
from typing import List, Dict


from src.user_utils import load_user_map, replace_pings


def parse_messages(json_files: List[str], users_json_path: str) -> List[Dict[str, str]]:
    """
    Parses all messages from the given list of JSON files.
    Replaces <@USERID> pings with display names using users.json.
    Returns a list of dicts: {u: display_name, t: text}
    """
    user_map = load_user_map(users_json_path)
    output = []
    for file_path in json_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for msg in data:
                user_profile = msg.get('user_profile')
                text = msg.get('text')
                if user_profile and text:
                    display_name = user_profile.get('display_name') or user_profile.get(
                        'real_name') or user_profile.get('name')
                    if display_name and text:
                        clean_text = replace_pings(text, user_map)
                        output.append({'u': display_name, 't': clean_text})
    return output
