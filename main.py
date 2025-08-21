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
    compress = False
    args = sys.argv[1:]
    if '--compress' in args:
        compress = True
        args.remove('--compress')
    if len(args) != 2:
        print("Usage: uv run main.py <zipfile> <channel_name> [--compress]")
        sys.exit(1)

    zip_path = args[0]
    channel_name = args[1]

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
    messages = parse_messages(json_files, users_json_path, compress=compress)

    # Write output to disk with random 5 digits
    rand_digits = ''.join(random.choices(string.digits, k=5))
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    suffix = "-compressed" if compress else ""
    output_filename = os.path.join(
        output_dir, f"{channel_name}{rand_digits}{suffix}.json")
    write_output_json(messages, output_filename, minify=compress)
    print(f"Output written to {output_filename}")


if __name__ == "__main__":
    main()
