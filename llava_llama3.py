import base64
import json
import requests
from pathlib import Path
from typing import Iterator
import sys

def send_image_to_llava(prompt: str, image_path: Path) -> requests.Response:
    """Send the image to the LLaVa API and get a response.
    
    Args:
        prompt: User's question or prompt about the image
        image_path: Path object pointing to the image file
        
    Returns:
        Response object from the API request
    """
    base64_image: str = base64.b64encode(image_path.read_bytes()).decode('utf-8')
    
    payload: dict = {
        "model": "llava",
        "stream": True,
        "messages": [
            {
                "role": "system",
                "content": "You are an Jarvis, an AI personal assistant\n"
                "Answer questions objectively and briefly, unless a longer answer is required\n"
                "Only ask a follow-up question if the user's request lacked clarity of intention\n"
                "Match the user's language and tone style in your responses",
            },
            {
                "role": "user",
                "content": prompt,
                "images": [base64_image]
            }
        ]
    }
    
    response: requests.Response = requests.post("http://localhost:11434/api/chat", json=payload, stream=True)
    
    # Write the response to a file and print it simultaneously
    for line in response.iter_lines():
        if line.strip():
            json_line: dict = json.loads(line.decode('utf-8'))            
            if "message" in json_line:
                content: str = json_line["message"]["content"]
                print(content, end="", flush=True)
    
    return response

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python llava-llama3.py \"<your prompt>\" <image_path>")
        sys.exit(1)

    prompt: str = sys.argv[1]
    image_path = Path(sys.argv[2])
    
    result = send_image_to_llava(prompt, image_path)