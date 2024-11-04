from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import locators
import time

URL = "https://www.swiggy.com/"
OUTLET = "House of wok Vasant Kunj"
OUTLET_NAME = "House of wok"
restaurant_data = {}

service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

driver.get(URL)
time.sleep(3)

Location_element = driver.find_element(By.CLASS_NAME, locators.Location_class)
time.sleep(3)
Location_element.click()


element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, locators.Location_input_Xpath)))
element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, locators.Location_input_Xpath)))
Location_input_element = driver.find_element(By.XPATH, locators.Location_input_Xpath)
Location_input_element.send_keys(OUTLET)
restaurant_data["Outlet"] = OUTLET
time.sleep(3)

First_location_in_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, locators.First_location_in_list_Xpath)))
First_location_in_list.click()
time.sleep(3)

Search_element = driver.find_element(By.XPATH, locators.Search_Xpath)
Search_element.click()
time.sleep(3)

element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, locators.Search_input_Xpath)))
Search_input_element = driver.find_element(By.XPATH, locators.Search_input_Xpath)
Search_input_element.send_keys(OUTLET_NAME)
time.sleep(3)

First_restaurant_in_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, locators.First_restaurant_in_list_Xpath)))
First_restaurant_in_list.click()
time.sleep(3)


Resultant_restaurant_element = driver.find_element(By.XPATH, locators.Resultant_restaurant_Xpath)

# checking if desired restaurant
expected_name = OUTLET_NAME.strip().lower()
Resultant_restaurant_name = driver.find_element(By.XPATH, locators.Resultant_restaurant_name_Xpath).text.strip().lower()
if(Resultant_restaurant_name != expected_name):
    print("Restraunt name not matched")
    print(Resultant_restaurant_name)
    time.sleep(5)
    driver.quit()
else:
    print("Restaurant name matched!")

Resultant_restaurant_element.click()
time.sleep(3)

# Reached Restaurant Page

Resultant_rating_element = driver.find_element(By.XPATH, locators.Rating_div_Xpath)
restaurant_data["Rating"] = Resultant_rating_element.text
print("-" * 20)
print("Resultant_rating_element.text")
print(Resultant_rating_element.text)

print("-" * 20)
Resultant_cft_element = driver.find_element(By.XPATH, locators.CFT_div_Xpath)
restaurant_data["CFT"] = Resultant_cft_element.text
print("Resultant_cft_element.text")
print(Resultant_cft_element.text)

# TODO check if tags present
Cuisine_tag_div = driver.find_element(By.XPATH, locators.Cuisine_tag_div_Xpath)
a_tags = Cuisine_tag_div.find_elements(By.TAG_NAME, "a")
print("-" * 20)
print("Tags:")
tag_list = []
for a_tag in a_tags:
    nested_div = a_tag.find_element(By.TAG_NAME, "div")
    tag_list.append(nested_div.text)
    text = nested_div.text
    print(text)
restaurant_data["Tags"] = tag_list
print("-" * 20)

# TODO check if deals present
Discount_divs = driver.find_elements(By.XPATH, locators.Discount_div_Xpath)
discount_list = []
for discount_div in Discount_divs:
    # 1. src attribute of the img in the first div
    img_div = discount_div.find_elements(By.TAG_NAME, "div")[0] 
    img_src = img_div.find_element(By.TAG_NAME, "img").get_attribute("src")
    
    # 2. text of the nested divs in the second div
    text_div_container = discount_div.find_elements(By.TAG_NAME, "div")[1]
    inner_divs = text_div_container.find_elements(By.TAG_NAME, "div")
    
    text_1 = inner_divs[0].text if len(inner_divs) > 0 else ""
    text_2 = inner_divs[1].text if len(inner_divs) > 1 else ""
    discount_list.append([text_1, text_2, img_src])

    print("Image src:", img_src)
    print(text_1)
    print(text_2)
    print("-" * 20)

restaurant_data["Discounts"] = discount_list

print(restaurant_data)

time.sleep(3)

driver.quit()

