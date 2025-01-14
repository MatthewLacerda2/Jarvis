import os
import pandas as pd
import json
import math
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(100000))
    return result['encoding']

def csv_summary(file_path):
    """
    Returns a JSON explaining the CSV+.

    Parameters:
        file_path (str): The path to the CSV file.

    Returns:
        str: A JSON-formatted string containing columns, row count, file size, and sample rows.
    """
    # Check if the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Get the file size in bytes
    file_size = os.path.getsize(file_path)

    # Read the CSV file using pandas with specified encoding
    try:
        encoding = detect_encoding(file_path)
        df = pd.read_csv(file_path, encoding=encoding)
    except UnicodeDecodeError as e:
        raise ValueError(f"Encoding error reading CSV file: {e}")
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

    # Extract columns and row count
    columns = df.columns.tolist()
    num_rows = len(df)

    sample_size = min(8, num_rows)

    if sample_size == num_rows:
        # If rows are less than or equal to 8, take all
        sample_rows = df.to_dict(orient='records')
    else:
        # Calculate interval to evenly sample rows
        interval = math.floor(num_rows / sample_size)
        sample_indices = [i * interval for i in range(sample_size)]
        sample_rows = df.iloc[sample_indices].to_dict(orient='records')

    # Create the JSON object
    result = {
        "columns": columns,
        "row_count": num_rows,
        "file_size_bytes": file_size,
        "sample_rows": sample_rows
    }

    return json.dumps(result, indent=4)

def csv_filtered(file_path, columns, num_rows):
    df = pd.read_csv(file_path, header=0, encoding='utf-8')
    df_string = df.to_dict(orient='records')

    #return a json with only the columns, and with the number of rows specified
    return json.dumps(df_string, orient='records', columns=columns, num_rows=num_rows)
