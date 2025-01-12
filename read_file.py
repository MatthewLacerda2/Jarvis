import pandas as pd

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
    return df_string

def read_csv_as_table(file_path: str) -> dict:
    df = pd.read_csv(file_path, header=0, encoding='utf-8')
    columns = df.columns.tolist()
    rows = ['|'.join(map(str, row)) for row in df.values]
    return {
        'columns': columns,
        'rows': rows
    }
