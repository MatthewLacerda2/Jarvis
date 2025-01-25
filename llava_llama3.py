import io
import json
import base64
import requests
from PIL import Image
from pathlib import Path
from typing import Iterator

def load_and_resize_image(image_path: Path, max_size: int = 1366) -> bytes:
    """Load and resize image if dimensions exceed max_size while preserving aspect ratio.
    
    Args:
        image_path: Path to the image file
        max_size: Maximum allowed dimension (width or height)
        
    Returns:
        Bytes of the processed image
    """
    with Image.open(image_path) as img:
        # Get original dimensions
        width, height = img.size
        
        # Check if resizing is needed
        if width > max_size or height > max_size:
            # Calculate scaling factor
            scale = max_size / max(width, height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            
            # Resize image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img.format or 'PNG')
        return img_byte_arr.getvalue()

def send_image_to_llava(prompt: str, image_path: Path) -> Iterator[str]:
    """Send the image to the LLaVa API and get a response.
    
    Args:
        prompt: User's question or prompt about the image
        image_path: Path object pointing to the image file
        
    Returns:
        Iterator of response content strings
    """
    image_bytes: bytes = load_and_resize_image(image_path)
    base64_image: str = base64.b64encode(image_bytes).decode('utf-8')
    
    payload: dict[str, object] = {
        "model": "llava",
        "stream": True,
        "messages": [
            {
                "role": "system",
                "content": "You are an AI personal assistant\n"
                "Match the user's language and tone style in your responses\n"
                "Answer questions objectively and briefly"
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
            json_line: dict[str, object] = json.loads(line.decode('utf-8'))            
            if "message" in json_line:
                content: str = json_line["message"]["content"]
                print(content, end="", flush=True)
                yield content
