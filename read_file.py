def read_txt_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()

def read_csv_file(file_path: str) -> str:
    import pandas as pd
    df = pd.read_csv(file_path)
    df_string = df.to_string(index=False)
    return df_string
