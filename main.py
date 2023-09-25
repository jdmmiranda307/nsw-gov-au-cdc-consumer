import requests
import json
import glob
import pathlib

from datetime import datetime
from agglutinate_csv import agglutinate_files
import pandas as pd

session = requests.Session()

base_path = str(pathlib.Path(__file__).parent.resolve())

def _get_data(suffix, filters):
    url = f"https://api.apps1.nsw.gov.au/eplanning/data/v0/Online{suffix}" 
    headers = {
        "PageSize": "2500",
        "PageNumber": "1",
        "filters": json.dumps({ "filters": filters})
    }
    first_page = session.get(url, headers=headers).json()
    yield first_page
    num_pages = first_page['TotalPages']

    for page in range(2, num_pages + 1):
        headers["PageNumber"] = str(page)
        next_page = session.get(url, headers=headers).json()
        yield next_page

def _small_files(name, data):
    print(f"Creating DataFrame small file ")
    df = pd.DataFrame(data)
    print(f"Writing data to CSV")
    df.to_csv(f"{base_path}/assets/{name.lower()}_small_files/{name.lower()}_{str(datetime.timestamp(datetime.now())).replace('.', '')}.csv")
    print(f"Wrote Small File")
    del df

def create_csv(name, filters):
    print(f"Getting data for {name} with filters {filters}")
    tmp_list = []
    for page in _get_data(name, filters):
        print(f"page {page['PageNumber']} of {page['TotalPages']}")
        _small_files(name, page["Application"])
    print(f"Wrote CSVs")
    print(f"Agglutinate")
    current_df = agglutinate_files(name.lower())
    current_df.to_csv(f"{base_path}/assets/{name.lower()}_{str(datetime.timestamp(datetime.now())).replace('.', '')}.csv") 
    print(f"Agglutinated")
    # criar trecho pra aglutinar

def main():
    print("Starting main")
    da_filters = {
                "ApplicationStatus": "Determined",
                "DeterminationDateFrom": "2018-01-01", 
                "DeterminationDateTo": datetime.now().strftime("%Y-%m-%d"), 
                "ApplicationType": "Development application"
            }

    cdc_filters = {
                    "ApplicationStatus": "Approved",
                    "DeterminationDateFrom": "2018-01-01", 
                    "DeterminationDateTo": datetime.now().strftime("%Y-%m-%d"), 
                    "ApplicationType": "Complying Development Certificate Application"
                }
    create_csv("DA", da_filters)
    create_csv("CDC", cdc_filters)


    print("Finished main")

if __name__ == '__main__':
    main()
