from driver import get_driver_with_wait, go_to_page
from parser import get_parsed_html


def get_categories(driver, wait):
    # scrape categories:
    go_to_page(
        "/food/c/27985", driver=driver, wait=wait, wait_element_class="link-list-maxH"
    )

    parsed_html = get_parsed_html(driver.page_source)

    categories_container = parsed_html.find("div", class_="link-list-maxH")
    category_tuples = []

    for elm in categories_container.select(".chakra-link"):
        if "See All" in elm.text:
            continue

        category_tuples.append((elm.text, elm.attrs["href"]))

    return category_tuples


def get_sub_categories(categories):
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
    driver, wait = get_driver_with_wait()
    categories = get_categories(driver, wait)
    # save them here once db is ready

    sub_categories = get_sub_categories(categories)
    # save them here once db is ready

    products = get_products()
    # save them here once db is ready
    driver.quit()


if __name__ == "__main__":
    main()
