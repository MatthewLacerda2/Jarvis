import pandas as pd
import json

def read_txt_file(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()

def read_csv_file(file_path: str) -> str:
    df = pd.read_csv(file_path, header=0, encoding='utf-8')
    df_string = df.to_dict(orient='records')
    return json.dumps(df_string)