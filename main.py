import requests
import json

session = requests.Session()

def get_data():
    url = "https://api.apps1.nsw.gov.au/eplanning/data/v0/OnlineDA" 
    headers = {
        "PageSize": "100",
        "PageNumber": "1",
        "filters": json.dumps({'filters': {} })
    }
    first_page = session.get(url, headers=headers).json()
    yield first_page
    num_pages = first_page['TotalPages']

    for page in range(2, num_pages + 1):
        headers["PageNumber"] = str(page)
        next_page = session.get(url, headers=headers).json()
        yield next_page

for page in get_data():
    print(page["PageNumber"])