import os
import pandas as pd
import json
import math
import chardet
from typing import Any, Dict, List, Union

def detect_encoding(file_path: str) -> str:
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(100000))
    return result['encoding']

def csv_summary(file_path: str) -> str:
    """
    Returns a JSON explaining the CSV.

    Parameters:
        file_path (str): The path to the CSV file.

    Returns:
        str: A JSON-formatted string containing columns, row count, file size, and sample rows.
    """
    # Check if the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Get the file size in bytes
    file_size: int = os.path.getsize(file_path)

    # Read the CSV file using pandas with specified encoding
    try:
        encoding: str = detect_encoding(file_path)
        df: pd.DataFrame = pd.read_csv(file_path, encoding=encoding)
    except UnicodeDecodeError as e:
        raise ValueError(f"Encoding error reading CSV file: {e}")
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

    # Extract columns and row count
    columns: List[str] = df.columns.tolist()
    num_rows: int = len(df)

    sample_size: int = min(8, num_rows)

    if sample_size == num_rows:
        # If rows are less than or equal to 8, take all
        sample_rows: List[Dict[str, Any]] = df.to_dict(orient='records')
    else:
        # Calculate interval to evenly sample rows
        interval: int = math.floor(num_rows / sample_size)
        sample_indices: List[int] = [i * interval for i in range(sample_size)]
        sample_rows: List[Dict[str, Any]] = df.iloc[sample_indices].to_dict(orient='records')

    # Create the JSON object
    result: Dict[str, Union[List[str], int, List[Dict[str, Any]]]] = {
        "columns": columns,
        "row_count": num_rows,
        "file_size_bytes": file_size,
        "sample_rows": sample_rows
    }

    return json.dumps(result, indent=4)

def csv_filtered(file_path: str, columns: List[str], num_rows: int) -> str:
    """
    Reads a CSV file and returns a JSON string containing filtered data based on specified columns, with a row limit.

    Parameters:
        file_path (str): Relative path to the CSV file (e.g., 'data/example.csv')
        columns (list[str]): List of column names to include in the output (e.g., ['name', 'age'])
        num_rows (int): Maximum number of rows to return

    Returns:
        str: A JSON-formatted string containing the filtered data

    Raises:
        FileNotFoundError: If the specified file does not exist
        ValueError: If there's an error reading the CSV file or if specified columns don't exist
    """
    encoding: str = detect_encoding(file_path)
    df: pd.DataFrame = pd.read_csv(file_path, header=0, encoding=encoding)
    
    # Filter columns (select only requested columns)
    df = df[columns]
    
    # Limit number of rows
    df = df.head(num_rows)
    
    # Convert to dictionary format
    df_dict: List[Dict[str, Any]] = df.to_dict(orient='records')
    
    return json.dumps(df_dict)
