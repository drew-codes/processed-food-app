from data_models.service import save_categories
from .driver import get_driver_with_wait, go_to_page_container
from .parser import get_parsed_html
from .utils.select_count import select_count

def get_categories(driver, wait):
    CATEGORY_LINK_SELECTOR = (
        "div[data-testid='plp-navigation'] a[data-testid='nav-list-link']"
    )

    FOOD_PAGE_PATH = "/food/c/27985"

    go_to_page_container(
        FOOD_PAGE_PATH,
        driver=driver,
        wait=wait,
        wait_css_selector=CATEGORY_LINK_SELECTOR,
        retries=2,
    )

    parsed_html = get_parsed_html(driver.page_source)

    links = parsed_html.css.select(CATEGORY_LINK_SELECTOR)

    category_tuples = []

    for elm in select_count(links, 2):
        if "See All" in elm.text:
            continue

        category_tuples.append((elm.text, elm.attrs["href"]))

    return category_tuples


def get_sub_categories(categories, driver, wait):
    sub_categories_containers = []
    for cat in categories:
        cat_name, url_path = cat
        CONTAINER_SELECTOR = "div.css-1kkjkbw"

        try:
            go_to_page_container(
                url_path,
                driver=driver,
                wait=wait,
                wait_css_selector=CONTAINER_SELECTOR,
                retries=2,
            )

            parsed_html = get_parsed_html(driver.page_source)

            sidebar = parsed_html.css.select(CONTAINER_SELECTOR)[0]

            sub_categories_containers.append(
                sidebar.find_all("div", attrs={"data-testid": "accordion-item"})
            )

        except Exception as error:
            print(
                f"[Sub Categories]: Could not load and/or parse {cat_name} page", error
            )
            continue

    sub_category_tuples = []

    for sub_cat_container in sub_categories_containers:

        for item in sub_cat_container:
            name = item.find("p", attrs={"data-testid": "accordion-title"})
            url = item.find("a", string="See All")
            sub_category_tuples.append((name.text, url.attrs["href"]))

    return sub_category_tuples


def get_products(sub_categories, driver, wait):
    product_links = []
    for sub_cat in select_count(sub_categories, 1):
        sub_cat_name, url_path = sub_cat
        PRODUCT_ITEM_SELECTOR = "div[data-testid='product-grid'] a.css-1hnz6hu"

        try:
            go_to_page_container(
                url_path,
                driver=driver,
                wait=wait,
                wait_css_selector=PRODUCT_ITEM_SELECTOR,
                retries=2,
            )

            parsed_html = get_parsed_html(driver.page_source)

            product_links.extend(parsed_html.css.select(PRODUCT_ITEM_SELECTOR))

        except Exception as error:
            print(f"[Products]: Could not load and/or parse {sub_cat_name} page", error)
            continue

    product_names_with_urls = []

    for link in product_links:
        name = link.find("h3").text
        product_names_with_urls.append((name, link.attrs["href"]))

    return product_names_with_urls


def run_scraper():
    driver, wait = get_driver_with_wait()
    categories = get_categories(driver, wait)

    save_categories(categories)
    # save them here once db is ready
    print("Categories Loaded \n\n\n")
    print("====================================")
    print(categories)
    print("====================================")
    print("\n\n\n")
    sub_categories = get_sub_categories(categories, driver=driver, wait=wait)
    print("Sub Categories Loaded \n\n\n")
    print("====================================")
    print(sub_categories)
    print("====================================")

    products = get_products(sub_categories=sub_categories, driver=driver, wait=wait)
    print("Products Loaded \n\n\n")
    print("====================================")
    print(products)
    print("====================================")

    # save them here once db is ready
    driver.quit()
