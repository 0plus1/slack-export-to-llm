import sys
from src.zip_handler import extract_channel_json_files, validate_zip_file, extract_users_json
from src.message_parser import parse_messages
from src.output_writer import write_output_json
from src.message_parser import parse_messages
from src.console import printError
import os
import random
import string


def main():
    """
    Entry point for the Slack export to LLM JSON converter.
    """
    if len(sys.argv) != 3:
        print("Usage: python main.py <zipfile> <channel_name>")
        sys.exit(1)

    zip_path = sys.argv[1]
    channel_name = sys.argv[2]

    if not validate_zip_file(zip_path, channel_name):
        printError("Invalid zip file or channel name.")
        sys.exit(1)
    # Extract users.json from the zip to a temp directory
    try:
        users_json_path = extract_users_json(zip_path)
    except FileNotFoundError as e:
        printError(str(e))
        sys.exit(1)
    # Extract JSON files for the channel from the zip
    json_files = extract_channel_json_files(zip_path, channel_name)
    # Parse messages from all JSON files, replacing pings
    messages = parse_messages(json_files, users_json_path)

    # Write output to disk with random 5 digits
    rand_digits = ''.join(random.choices(string.digits, k=5))
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(
        output_dir, f"{channel_name}{rand_digits}.json")
    write_output_json(messages, output_filename)
    print(f"Output written to {output_filename}")


if __name__ == "__main__":
    main()
