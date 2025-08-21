"""
Utility functions for user ID to display name mapping.
"""
import json
from typing import Dict


def load_user_map(users_json_path: str) -> Dict[str, str]:
    """
    Loads users.json and returns a dict mapping user ID to display name.
    """
    with open(users_json_path, 'r', encoding='utf-8') as f:
        users = json.load(f)
    user_map = {}
    for user in users:
        user_id = user.get('id')
        profile = user.get('profile', {})
        display_name = profile.get('display_name') or profile.get(
            'real_name') or user.get('name')
        if user_id and display_name:
            user_map[user_id] = display_name
    return user_map


def replace_pings(text: str, user_map: Dict[str, str]) -> str:
    """
    Replaces <@USERID> mentions in text with the corresponding display name.
    """
    import re

    def repl(match):
        user_id = match.group(1)
        return f"@{user_map.get(user_id, user_id)}"
    return re.sub(r"<@([A-Z0-9]+)>", repl, text)
