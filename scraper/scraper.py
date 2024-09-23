from data_models.service import save_categories, save_sub_categories
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
        cat_name, url_path = cat.name, cat.vendor_url
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
                (cat, sidebar.find_all("div", attrs={"data-testid": "accordion-item"}))
            )

        except Exception as error:
            print(
                f"[Sub Categories]: Could not load and/or parse {cat_name} page", error
            )
            continue

    sub_category_tuples = []

    for cat, sub_cat_container in sub_categories_containers:

        for item in sub_cat_container:
            name = item.find("p", attrs={"data-testid": "accordion-title"})
            url = item.find("a", string="See All")
            sub_category_tuples.append((name.text, url.attrs["href"], cat))

    return sub_category_tuples


def has_next_page(parsed_html, current_page):
    pagination_links = parsed_html.css.select("nav[data-testid='pagination'] a")

    for link in pagination_links:
        if link.text == str(current_page + 1):
            return True

    return False


def get_product_links(
    url_path,
    driver,
    wait,
    links=[],
    current_page=1,
):
    PRODUCT_ITEM_SELECTOR = "div[data-testid='product-grid'] a.css-1hnz6hu"

    url_path_with_page = url_path + f"?page={current_page}"

    go_to_page_container(
        url_path_with_page,
        driver=driver,
        wait=wait,
        wait_css_selector=PRODUCT_ITEM_SELECTOR,
        retries=2,
    )

    parsed_html = get_parsed_html(driver.page_source)

    links.extend(parsed_html.css.select(PRODUCT_ITEM_SELECTOR))

    if has_next_page(parsed_html, current_page):
        return get_product_links(
            url_path,
            driver,
            wait,
            links,
            current_page + 1,
        )

    return links


def get_product_name_with_url(sub_categories, driver, wait):
    product_links = []
    for sub_cat in select_count(sub_categories, 1):
        sub_cat_name, url_path = sub_cat.name, sub_cat.vendor_url

        try:
            product_links.extend(
                get_product_links(
                    url_path,
                    driver,
                    wait,
                )
            )

        except Exception as error:
            print(f"[Products]: Could not load and/or parse {sub_cat_name}", error)
            continue

    product_names_with_urls = []

    for link in product_links:
        name = link.find("h3").text
        product_names_with_urls.append((name, link.attrs["href"]))

    return product_names_with_urls


def get_product_details(products, driver, wait):
    product_details = []

    for product in select_count(products, 1):
        product_name, url_path = product.name, product.vendor_url
        PRODUCT_DETAILS_SELECTOR = "div[data-testid='product-details']"

        try:
            go_to_page_container(
                url_path,
                driver=driver,
                wait=wait,
                wait_css_selector=PRODUCT_DETAILS_SELECTOR,
                retries=2,
            )

            parsed_html = get_parsed_html(driver.page_source)

            product_details.append(parsed_html.css.select(PRODUCT_DETAILS_SELECTOR))

        except Exception as error:
            print(
                f"[Product Details]: Could not load and/or parse {product_name} page",
                error,
            )
            continue

    return product_details


def run_scraper():
    driver, wait = get_driver_with_wait()
    categories = get_categories(driver, wait)

    saved_categories = save_categories(categories)
    # save them here once db is ready
    print("Categories Loaded \n\n\n")
    print("====================================")
    print(categories)
    print("====================================")
    print("\n\n\n")
    sub_categories = get_sub_categories(saved_categories, driver=driver, wait=wait)

    saved_sub_categories = save_sub_categories(sub_categories)
    print("Sub Categories Loaded \n\n\n")
    print("====================================")
    print(sub_categories)
    print("====================================")

    products_names_with_url = get_product_name_with_url(
        sub_categories=saved_sub_categories, driver=driver, wait=wait
    )

    # TODO: Get product details and save them
    # TODO: Get ingredients and save them

    print("Products Loaded \n\n\n")
    print("====================================")
    print(products_names_with_url)
    print("====================================")

    # save them here once db is ready
    driver.quit()
