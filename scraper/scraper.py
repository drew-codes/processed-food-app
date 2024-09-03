from scraper.driver import go_to_page
from scraper.parser import get_parsed_html


def get_categories():
    # scrape categories:
    driver = go_to_page("/food/c/27985", wait_element_class="")

    parsed_html = get_parsed_html(driver.page_source)
    # 1. Go to food page (https://www.loblaws.ca/food/c/27985)
    # 2. Grab each category name and url
    # 3. return the category names and urls
    return


def get_sub_categories():
    # scrape subcategories:
    # 1. Go to each category
    # 2. From the Sidebar, Get every sub-category name and its corresponding all page url
    # 3. return the category names and urls
    pass


def get_products():
    # scrape products:
    # 1. check the scraped products - if already there, skip otherwise step 2
    # 2. get product info (id, name, ingredients)
    pass


def main():
    categories = get_categories()
    # save them here once db is ready

    sub_categories = get_sub_categories()
    # save them here once db is ready

    products = get_products()
    # save them here once db is ready


# driver.quit()

if __name__ == "main":
    main()
