import json
from csv_handler import create_csv
from datetime import datetime

BASE_URL = "https://api.apps1.nsw.gov.au/eplanning/data/v0"

request_url = lambda endpoint: f"{BASE_URL}/{endpoint}"

def main(ops):
    print("Starting main")
    for op in ops:
        print(f"running for op {op['name']}")
        dict_params = {
            "headers": {
                "PageSize": "2500",
                "PageNumber": "1",
            }
        }
        dict_params["url"] = request_url(f"Online{op['name']}")
        dict_params["headers"]["filters"] = json.dumps({ "filters": op["filters"]})
        df = create_csv(op['name'], dict_params)
    print("Finished main")


if __name__ == '__main__':
    # Alterar aqui seus filtros
    ops = [
        {
            "name": "DA",
            "filters": {}
        },
        {
            "name": "CC",
            "filters": {}
        },
        {
            "name": "CDC",
            "filters": {}
        }
    ]
    main(ops)

