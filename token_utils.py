from read_file import read_csv_file, read_txt_file  # Import functions to read CSV and TXT files

def count_tokens(input_string):
    """
    Counts the number of tokens (words) in the input string.

    :param input_string: The string to count tokens in.
    :return: The number of tokens.
    """
    # Split the string into tokens using whitespace as the delimiter
    tokens = input_string.split()
    return len(tokens)

if __name__ == "__main__":
    import sys  # Import sys to access command line arguments
    import os  # Import os to check file extensions

    if len(sys.argv) != 2:
        print("Usage: python token_utils.py <path_to_file>")
        sys.exit(1)

    file_path = sys.argv[1]  # Get the file path from command line arguments

    # Check the file extension and read the file accordingly
    if file_path.endswith('.csv'):
        content = read_csv_file(file_path)  # Read the CSV file
    elif file_path.endswith('.txt') or file_path.endswith('.py') or file_path.endswith('.cs'):
        content = read_txt_file(file_path)  # Read the TXT file
    else:
        print("Unsupported file type. Please provide a .csv or .txt file.")
        sys.exit(1)

    token_count = count_tokens(str(content))  # Count tokens in the file content
    print(f"Number of tokens: {token_count}")  # Print the token count
    

