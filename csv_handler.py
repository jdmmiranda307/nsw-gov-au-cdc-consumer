import glob
import pathlib
import os
from requester import get_data
from datetime import datetime
import pandas as pd
import csv


base_path = str(pathlib.Path(__file__).parent.resolve())

csv_path = lambda name: f"{base_path}/assets/{name.lower()}_small_files/{datetime.now().strftime('%Y-%m-%d')}"
# idealmente, deveria ler todos os csv para uma lista, ai sim transfgormar num df. Posteriormente deveria melhorar isso
def _agglutinate_files(suffix):
    csv_files = [f"{csv_path(suffix)}/{f}" for f in os.listdir(f"{csv_path(suffix)}/") if f.endswith(".csv")]
    full_csv = pd.read_csv(csv_files.pop())
    for csv_file in csv_files:
        tmp_df = pd.read_csv(csv_file)
        full_csv = full_csv.append(tmp_df)

    return full_csv

def _get_dataframe_info(df, name):
    print(f"Getting DF info")
    df_cols_unique = {}
    for col in df.columns:
        df_cols_unique[col]= df[col].unique()
    with open(f"{base_path}/assets/{name}_full_files/{datetime.now().strftime('%Y-%m-%d')}/info.txt", 'w') as f:
        f.write(str(df_cols_unique))

def _small_files(name, data):
    print(f"Creating DataFrame small file ")
    df = pd.DataFrame(data)
    print(f"Writing data to CSV")
    current_path = csv_path(name)
    if not os.path.exists(current_path):
        os.makedirs(current_path)
    df.to_csv(f"{current_path}/{name.lower()}_{str(datetime.timestamp(datetime.now())).replace('.', '')}.csv")
    print(f"Wrote Small File")
    del df


def create_csv(name, request_params):
    print(f"Getting data for {name} of request {request_params}")
    tmp_list = []
    current_path = f"{base_path}/assets/{name.lower()}_full_files/{datetime.now().strftime('%Y-%m-%d')}/"
    for page in get_data(name, request_params):
        print(f"page {page['PageNumber']} of {page['TotalPages']}")
        _small_files(name, page["Application"])
    print(f"Wrote CSVs")
    print(f"Agglutinate")
    current_df = agglutinate_files(name.lower())
    if not os.path.exists(current_path):
        os.makedirs(current_path)
    current_df.to_csv(f"{current_path}{name.lower()}_{str(datetime.timestamp(datetime.now())).replace('.', '')}.csv")
    print(f"Agglutinated")
    get_dataframe_info(current_df, name.lower())
    return current_df