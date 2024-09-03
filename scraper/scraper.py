from driver import get_driver_with_wait, go_to_page
from parser import get_parsed_html


def get_categories(driver, wait):
    # scrape categories:
    go_to_page("/food/c/27985", driver=driver, wait=wait, wait_element_class="")

    parsed_html = get_parsed_html(driver.page_source)
    # 1. Go to food page (https://www.loblaws.ca/food/c/27985)
    # 2. Grab each category name and url
    # 3. return the category names and urls
    print(parsed_html)
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
    print("executing...")
    driver, wait = get_driver_with_wait()
    categories = get_categories(driver, wait)
    # save them here once db is ready

    sub_categories = get_sub_categories()
    # save them here once db is ready

    products = get_products()
    # save them here once db is ready
    driver.quit()


if __name__ == "__main__":
    main()
