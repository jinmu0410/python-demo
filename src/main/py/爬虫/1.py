import os

import requests
import json
import pandas as pd
import time

def is_sheet_exists(file_path, sheet_name):
    try:
        df = pd.read_excel(file_path, sheet_name)
        print(df.shape[0])
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    file_name = 'yes/云南省-1.xlsx'
    print(is_sheet_exists(file_name, '云南省-曲靖市-会泽县'))