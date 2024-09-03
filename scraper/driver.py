from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from env_setup import get_grocer_base_url
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def get_driver_with_wait():
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, timeout=10)
    return driver, wait


def go_to_page(path, driver, wait, wait_element_class):
    driver.get(get_grocer_base_url() + path)
    if wait_element_class:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, wait_element_class)))

    return driver
