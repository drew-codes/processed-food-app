from data_models.service import save_categories, save_products, save_sub_categories
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
    links=None,
    current_page=1,
):
    if links is None:
        links = []

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


def get_product_urls(sub_categories, driver, wait):
    excluded_vendor_ids = [
        "28169",
        "28166",
        "28167",
        "28168",
        "28205",
    ]
    sub_cat_product_links = []
    for sub_cat in select_count(sub_categories, 8):

        if sub_cat.vendor_id in excluded_vendor_ids:
            continue

        (
            sub_cat_name,
            cat,
            url_path,
        ) = (
            sub_cat.name,
            sub_cat.category,
            sub_cat.vendor_url,
        )

        try:
            sub_cat_product_links.append(
                (
                    sub_cat,
                    cat,
                    get_product_links(
                        url_path,
                        driver,
                        wait,
                    ),
                )
            )

        except Exception as error:
            print(f"[Products]: Could not load and/or parse {sub_cat_name}", error)
            continue

    product_urls = []

    for link in sub_cat_product_links:
        sub_cat, cat, links = link

        for item in links:
            product_urls.append((item.attrs["href"], sub_cat, cat))

    return product_urls


def get_product_details(product_links, driver, wait):
    product_details = []

    for url_path, sub_cat, cat in select_count(product_links, 30):
        PRODUCT_DETAILS_WAIT_SELECTOR = (
            "div.product-details-page-info-layout--ingredients"
        )

        try:
            go_to_page_container(
                url_path,
                driver=driver,
                wait=wait,
                wait_css_selector=PRODUCT_DETAILS_WAIT_SELECTOR,
                retries=2,
            )

            parsed_html = get_parsed_html(driver.page_source)

            name = parsed_html.css.select("h1.product-name__item--name")[0].text
            brand = parsed_html.css.select("span.product-name__item--brand")[0].text
            product_description = parsed_html.css.select(
                "div.product-description-text__text"
            )[0].text
            ingredients = parsed_html.css.select(
                "div.product-details-page-info-layout--ingredients div.product-details-page-info-layout-content"
            )[0].text

            product_details.append(
                {
                    "name": name,
                    "brand": brand,
                    "product_description": product_description,
                    "vendor_id": url_path.split("?")[0].split("/")[-1],
                    "sub_category": sub_cat,
                    "category": cat,
                    "ingredients_text": ingredients,
                }
            )

        except Exception as error:
            print(
                f"[Product Details]: Could not load and/or parse {url_path}",
                error,
            )
            continue

    return product_details


def run_scraper(stdout, style):
    driver, wait = get_driver_with_wait()

    saved_categories = save_categories(get_categories(driver, wait))

    stdout.write(style.SUCCESS(f"Saved {len(saved_categories)} categories"))

    saved_sub_categories = save_sub_categories(
        get_sub_categories(saved_categories, driver=driver, wait=wait)
    )

    stdout.write(style.SUCCESS(f"Saved {len(saved_sub_categories)} sub categories"))

    product_urls = get_product_urls(
        sub_categories=saved_sub_categories, driver=driver, wait=wait
    )

    products_saved = save_products(
        get_product_details(product_urls, driver=driver, wait=wait)
    )

    stdout.write(style.SUCCESS(f"Saved {products_saved} products"))

    driver.quit()
