import requests
import os
import sys
import json
from read_file import read_txt_file, read_csv_file  # Import the functions

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<your prompt>\" [<file_path>]")
        sys.exit(1)

    prompt: str = sys.argv[1]
    file_path: str = sys.argv[2] if len(sys.argv) > 2 else None  # Get the optional file path
    additional_content: str = ""

    if file_path:
        if file_path.endswith('.txt') or file_path.endswith('.py') or file_path.endswith('.cs'):
            additional_content = read_txt_file(file_path)  # Read text file
        elif file_path.endswith('.csv'):
            additional_content = read_csv_file(file_path)
        else:
            print("Unsupported file format. Please provide a .txt or .csv file.")
            sys.exit(1)

    if additional_content:
        file_to_string = f"\nHere's the data the user attached to the prompt, in a string format: {additional_content}"
    else:
        file_to_string = ""
    
    data: dict = {
        "model": "llama3.1",
        "stream": True,
        "system": (
            "You are an Jarvis, an AI personal assistant\n"
            "Answer questions objectively and briefly, unless a longer answer is required\n"
            "Only ask follow-up questions if the user's request lacked information to be properly responded\n"
            "Match the user's tone and language style in your responses"
            f"{file_to_string}"
        ),
        "prompt": prompt,
    }

    url: str = "http://localhost:11434/api/generate"
    headers: dict = {
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=data, headers=headers, stream=True)
    response.raise_for_status()
    
    for line in response.iter_lines(decode_unicode=True):
        if line.strip():
            json_line = json.loads(line)
            if "response" in json_line:
                response_text = json_line["response"]
                print(response_text, end="", flush=True)

if __name__ == "__main__":
    main()
