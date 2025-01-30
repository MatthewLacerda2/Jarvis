import sys
import argparse
import ollama
from pathlib import Path
from datetime import datetime
from llava_llama3 import send_image_to_llava
from read_file import read_txt_file, read_csv_file
from function_calling.read_csv import csv_summary, csv_filtered
from function_calling.run_python_code import execute_python_function, execute_python_code
from function_calling.save_files import save_text_to_file

def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description='Chat with an AI model')
    parser.add_argument('prompt', type=str, help='Your prompt/question for the AI')
    parser.add_argument('file_path', nargs='?', help='Optional path to a file')
    parser.add_argument('--model', type=str, default='llama3.1', help='Model to use (default: llama3.1)')
    
    args: argparse.Namespace = parser.parse_args()
    prompt: str = args.prompt
    file_path: str | None = args.file_path
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
        file_to_string: str = f"Here is the file '{file_path}' that the user attached to the prompt, converted to json: {additional_content}"
    else:
        file_to_string: str = ""
    
    system_prompt: str = (
        "You are AI personal assistant'\n"
        "Match the user's language and tone style in your responses\n"
        "Answer the prompt objectively\n"
        "Be brief, unless the answer has to be long"
        "You were given access to several tools, but only use them when actually needed\n"
        "Do NOT use tool calling when there is no need for it\n"
    )

    prompt+=f"\n\n{file_to_string}"

    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    tools = [save_text_to_file, csv_filtered, read_csv_file, execute_python_function, execute_python_code]
    tools_dict = {tool.__name__: tool for tool in tools}

    if args.model not in ['llama3.1', 'llama3.2']:
        tools = []
        tools_dict = {}

    response = ollama.chat(
        model=args.model,
        messages=messages,
        tools=tools,
        stream=False
    )

    if response.message.tool_calls:
        for tool in response.message.tool_calls:
            print(f"Calling {tool.function.name}: {tool.function.arguments}")
        # Handle tool calls
        for tool in response.message.tool_calls:
            if function_to_call := tools_dict.get(tool.function.name):
                function_to_call(**tool.function.arguments)
                
                # Add the function response to messages
                messages.append(response.message)
                messages.append({
                    'role': 'tool',
                    'content': f"File saved successfully",
                    'name': tool.function.name
                })

                final_response = ollama.chat(
                    model=args.model,
                    messages=messages,
                    stream=True
                )
                
                for chunk in final_response:
                    if chunk.get('message', {}).get('content'):
                        print(chunk['message']['content'], end='', flush=True)
    else:
        stream = ollama.chat(
            model=args.model,
            messages=messages,
            stream=True
        )
        
        for chunk in stream:
            if chunk.get('message', {}).get('content'):
                print(chunk['message']['content'], end='', flush=True)
    print(f"\nCurrent time: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
