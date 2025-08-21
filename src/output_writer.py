"""
Writes the output messages to a JSON file.
"""
import json
from typing import List, Dict


def write_output_json(messages: List[Dict[str, str]], output_path: str) -> None:
    """
    Writes the list of messages to the specified output file as JSON.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
