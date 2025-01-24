import sys
import argparse
import ollama
from pathlib import Path
from llava_llama3 import send_image_to_llava
from read_file import read_txt_file, read_csv_file
from function_calling.read_csv import csv_summary, csv_filtered

def main() -> None:
    parser = argparse.ArgumentParser(description='Chat with an AI model')
    parser.add_argument('prompt', type=str, help='Your prompt/question for the AI')
    parser.add_argument('file_path', nargs='?', help='Optional path to a file')
    parser.add_argument('--model', type=str, default='llama3.1', help='Model to use (default: llama3.1)')
    
    args = parser.parse_args()
    prompt: str = args.prompt
    file_path: str = args.file_path
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
    
    system_prompt = (
        "You are AI personal assistant\n"
        "Match the user's language and tone style in your responses\n"
        "Answer questions objectively and briefly\n"
        f"{file_to_string}"
    )

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    
    print()

    stream = ollama.chat(
        model=args.model,
        messages=messages,
        stream=True,
        temperature=0.5,
        system_prompt=system_prompt
    )
    
    for chunk in stream:
        if chunk.get('message', {}).get('content'):
            print(chunk['message']['content'], end='', flush=True)
    
    print("\n")

if __name__ == "__main__":
    main()
