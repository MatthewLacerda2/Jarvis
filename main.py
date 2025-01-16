import sys
import json
import requests
from pathlib import Path

from read_file import read_txt_file, read_csv_file
from function_calling.read_csv import csv_summary, csv_filtered
from llava_llama3 import send_image_to_llava

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<your prompt>\" [<file_path>]")
        sys.exit(1)

    prompt: str = sys.argv[1]
    file_path: str = sys.argv[2] if len(sys.argv) > 2 else None
    additional_content: str = ""

    if file_path:
        if file_path.endswith('.txt') or file_path.endswith('.py') or file_path.endswith('.cs') or file_path.endswith('.ts'):
            additional_content = read_txt_file(file_path)
        elif file_path.endswith('.csv'):
            additional_content = csv_summary(file_path)
        elif file_path.endswith('.png') or file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
            send_image_to_llava(prompt, Path(file_path))
            sys.exit(0)
        else:
            print("Unsupported file format. Please provide a .txt, .csv, or image file.")
            sys.exit(1)

    if additional_content:
        filename_with_extension = Path(file_path).name
        file_to_string = f"Here's the file {filename_with_extension} user attached to the prompt, in a string format: {additional_content}"
    else:
        file_to_string = ""
    
    data: dict = {
        "model": "llama3.1",
        "stream": True,
        "system": (
            "You are Jarvis, an AI personal assistant\n"
            "Match the user's language and tone style in your responses\n"
            "Answer questions objectively and briefly\n"
            f"{file_to_string}"
        ),
        "prompt": prompt,
    }

    url: str = "http://localhost:11434/api/generate"

    response = requests.post(url, json=data, stream=True)
    response.raise_for_status()
    
    for line in response.iter_lines(decode_unicode=True):
        if line.strip():
            json_line = json.loads(line)
            if "response" in json_line:
                response_text = json_line["response"]
                print(response_text, end="", flush=True)

if __name__ == "__main__":
    main()
