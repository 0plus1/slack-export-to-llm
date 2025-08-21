"""
Parses messages from extracted Slack channel JSON files.
"""
import json
from typing import List, Dict


from src.user_utils import load_user_map, replace_pings


from src.common_slack_messages import COMMON_SLACK_MESSAGES


def parse_messages(json_files: List[str], users_json_path: str, compress: bool = False) -> List[Dict[str, str]]:
    """
    Parses all messages from the given list of JSON files.
    Replaces <@USERID> pings with display names using users.json.
    If compress=True, strips whitespace and removes common Slack system messages.
    Returns a list of dicts: {u: display_name, t: text}
    """
    user_map = load_user_map(users_json_path)
    output = []
    seen = set()
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
                        if compress:
                            # Remove leading/trailing whitespace and redundant spaces
                            clean_text = ' '.join(clean_text.split())
                            # Remove common Slack system messages
                            if any(phrase in clean_text for phrase in COMMON_SLACK_MESSAGES):
                                continue
                            # Deduplicate
                            key = (display_name, clean_text)
                            if key in seen:
                                continue
                            seen.add(key)
                        output.append({'u': display_name, 't': clean_text})
    return output
