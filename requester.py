import requests
import json

session = requests.Session()

def get_data(suffix, params):
    first_page = session.get(**params).json()
    yield first_page
    num_pages = first_page['TotalPages']

    for page in range(2, num_pages + 1):
        params["headers"]["PageNumber"] = str(page)
        print(f"got page {params['headers']['PageNumber']}")
        next_page = session.get(**params).json()
        yield next_page
