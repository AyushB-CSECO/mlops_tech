import pandas as pd
from pathlib import Path

# Reset to Base Folder
FILE_PATH = Path(__file__).resolve()
BASE_PATH = FILE_PATH.parent.parent.parent

# Create folder path to raw .csv files
FOLDER_PATH = BASE_PATH / "data" / "raw"

countries_df = pd.read_csv(FOLDER_PATH / "countries.csv")

def check_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    empty_row_flag = df.isna().all(axis=1)
    n_empty_rows = empty_row_flag.sum() 
    if n_empty_rows > 0:
        print(f"Removing {n_empty_rows} null row from the dataset")
    else:
        print("No null rows in dataset")
    return df[~empty_row_flag].reset_index(drop=True)

def colnames_lowercase(df: pd.DataFrame):
    colnames = [i.lower() for i in df.columns]
    df.columns = colnames
    return df

if __name__ == "__main__":
    print(BASE_PATH)

