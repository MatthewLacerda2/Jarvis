import requests
import sys
import json

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<your prompt>\"")
        sys.exit(1)

    prompt = sys.argv[1]
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model": "llama3.1",
        "prompt": prompt,
        "stream": True,
        "system": (
            "You are an Jarvis, an AI personal assistant\n"
            "Answer questions objectively and briefly, up to 400 characters, unless a longer answer is required\n"
            "If the user's request is too vague or lacks clarity of purpose, ask a question to further your precision\n"
            "Match the user's tone and language style in your responses"
        )
    }

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
