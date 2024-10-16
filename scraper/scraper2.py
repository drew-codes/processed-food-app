import requests
import json
from scraper.env_setup import get_categories_url, get_grocer_base_url


# get session


# get categories
# save categories
# get sub categories
# save sub categories
# get sub category products
# get products

with open("scraper/headers.json", "r") as file:
    headers = json.load(file)

with open("scraper/payload-data.json", "r") as file:
    data = json.load(file)


def get_session():
    session = requests.Session()
    session.get(get_grocer_base_url())
    return session


def run_scraper2(stdout, style):
    session = get_session()
    url = get_categories_url()
    response = session.post(url, headers=headers, json=data)

    print(response.json())
