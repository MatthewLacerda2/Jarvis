from pathlib import Path

def save_text_to_file(filename: str, content: str) -> None:
    """
    Saves the provided string content to a text file on the desktop.
    
    Args:
        filename (str): Name of the file to create (without .txt extension)
        content (str): String content to write to the file
    
    Returns:
        None
        
    Raises:
        OSError: If there's an error creating or writing to the file
    """
    # Get desktop path in a cross-platform way
    desktop_path = Path.home() / "Desktop"
    
    # Create full file path with .txt extension
    file_path = desktop_path / f"{filename}.txt"
    
    try:
        # Write content to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except OSError as e:
        raise OSError(f"Error saving file to desktop: {e}")