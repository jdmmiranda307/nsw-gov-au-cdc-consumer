import glob
import pathlib

from datetime import datetime
import pandas as pd
import csv

import os
# idealmente, deveria ler todos os csv para uma lista, ai sim 
base_path = str(pathlib.Path(__file__).parent.resolve())
def agglutinate_files(suffix):
    csv_files = [f"{base_path}/assets/{suffix}_small_files/{f}" for f in os.listdir(f"{base_path}/assets/{suffix}_small_files/") if f.endswith(".csv")]
    full_csv = pd.read_csv(csv_files.pop())
    for csv_file in csv_files:
        tmp_df = pd.read_csv(csv_file)
        full_csv = full_csv.append(tmp_df)

    return full_csv
