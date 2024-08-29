# import dependencies
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv, dotenv_values 

load_dotenv() 

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
driver = webdriver.Firefox(options=options)
url = os.environ['GROCER_URL_BASE']
wait = WebDriverWait(driver, timeout=10)


# make the request
driver.get(f"{url}classic-potato-chips/p/21241032_EA")

# ensure page is loaded
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product-details-page-nutrition-info')))


soup = BeautifulSoup(driver.page_source, features="html.parser")


# # At this point we can parse with BeautifulSoup
product_details_page = soup.find("div", class_="product-details-page")
product_details_container = product_details_page.find("div", class_="product-details-page-details")
brand = product_details_container.find("span", class_="product-name__item--brand")
name = product_details_container.find("h1", class_="product-name__item--name")
nutrition_info_container = product_details_page.find("div", class_="product-details-page-nutrition-info")
ingredients = nutrition_info_container.find("div", class_="product-details-page-info-layout--ingredients")

print(brand.text)
print(name.text)
print(ingredients.text)



driver.quit()