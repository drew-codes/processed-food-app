from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from .env_setup import get_grocer_base_url
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def get_driver_with_wait():
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, timeout=5)
    return driver, wait


def go_to_page_container(path, driver, wait, wait_css_selector, retries=0):
    driver.get(get_grocer_base_url() + path)

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, wait_css_selector)))
    except Exception as error:
        if retries:
            print(
                f"[Retrying]: Could not find {wait_css_selector}, {retries} attempts left."
            )
            go_to_page_container(path, driver, wait, wait_css_selector, retries - 1)
        else:
            print(f"[Error]: Could not find {wait_css_selector}.")
            raise error
