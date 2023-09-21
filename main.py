import requests
import json
from datetime import datetime
import pandas as pd

session = requests.Session()

def get_data(suffix, filters):
    url = f"https://api.apps1.nsw.gov.au/eplanning/data/v0/Online{suffix}" 
    headers = {
        "PageSize": "300",
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



def create_csv(name, filters):
    print(f"Getting data for {name} with filters {filters}")
    tmp_list = []
    for page in get_data(name, filters):
        tmp_list += page["Application"]
    print(f"Creating dataframe with {len(tmp_list)} rows")
    df = pd.DataFrame(tmp_list)
    print(f"Writing dataframe to CSV")
    df.to_csv(f"{name}.csv")
    print(f"Wrote CSV")
    del df
    del tmp_list

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
