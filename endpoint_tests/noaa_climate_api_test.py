import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOAA_TOKEN = os.getenv("NOAA_TOKEN")

"""
    NOAA climate data format for requests
        Dataset: ex. "GHCND" ( which is daily summaries )
        Locationid: "FIPS:06" (California)
"""


def fetch_noaa_data(dataset: str = "GHCND", locationid: str = "FIPS:06"):
    #req
    url = f"https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid={dataset}&locationid={locationid}&limit=10"
    
    headers = {"token": NOAA_TOKEN}
    resp = requests.get(url, headers=headers)
    if not resp.ok:
        return {"error": f"NOAA API request failed: {resp.status_code}"}
    data = resp.json()
    return data

if __name__ == "__main__":
    from rich.pretty import pprint
    pprint(fetch_noaa_data())
