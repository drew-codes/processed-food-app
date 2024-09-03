from bs4 import BeautifulSoup


def get_parsed_html(page_source):
    return BeautifulSoup(page_source, features="html.parser")
