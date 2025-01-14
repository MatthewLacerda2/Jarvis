import base64
import json
import requests
from pathlib import Path
from typing import Iterator

def send_image_to_llava(image_path: Path) -> requests.Response:
    """Send the image to the LLaVa API and get a response.
    
    Args:
        image_path: Path object pointing to the image file
        
    Returns:
        Response object from the API request
    """
    base64_image: str = base64.b64encode(image_path.read_bytes()).decode('utf-8')
    
    payload: dict = {
        "model": "llava-llama3",
        "stream": True,
        "messages": [
            {
                "role": "system",
                "content": "You are an Jarvis, an AI personal assistant\n"
                "Answer questions objectively and briefly, unless a longer answer is required\n"
                "Only ask a follow-up question if the user's request lacked clarity of intention\n"
                "Match the user's tone and language style in your responses"
            },
            {
                "role": "user",
                "content": "Briefly describe this image",
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

    # Use raw string or forward slashes for path
    image_path = Path(r"C:\Users\Matheus Lacerda\Downloads\profile.png")
    # Alternative: image_path = Path("C:/Users/Matheus Lacerda/Downloads/profile.png")
    
    result = send_image_to_llava(image_path)