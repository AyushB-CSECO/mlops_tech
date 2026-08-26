import pandas as pd
from pathlib import Path
import os

from .validation import check_empty_rows

# Reset to Base Folder
FILE_PATH = Path(__file__).resolve()
BASE_PATH = FILE_PATH.parent.parent.parent

# Create folder path to raw .csv files
FOLDER_PATH = BASE_PATH / "data" / "raw"

if __name__ == "__main__":
    list_csvfiles = os.listdir(FOLDER_PATH)
    for fname in list_csvfiles:
        fpath = FOLDER_PATH / fname 
        data = pd.read_csv(fpath)
        data = check_empty_rows(data)

