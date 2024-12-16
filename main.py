from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import locators
import time
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

URL = "https://www.swiggy.com/"

# OUTLET = "House of wok : Vasant Kunj"
# OUTLET_NAME = "House of wok"
restaurants_data = []

service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

def open_and_login():
    driver.get(URL)
    time.sleep(3)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, locators.Sign_in_span)))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, locators.Sign_in_span)))

    Sign_in_element = driver.find_element(By.XPATH, locators.Sign_in_span)
    Sign_in_element.click()

    time.sleep(45)


def get_data_script(OUTLET, OUTLET_NAME):
    driver.get("https://www.swiggy.com/restaurants")
    time.sleep(8)
    restaurant_data = {}
    Location_element = driver.find_element(By.CLASS_NAME, locators.Location_class)
    time.sleep(3)
    Location_element.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, locators.Location_input_Xpath)))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, locators.Location_input_Xpath)))
    Location_input_element = driver.find_element(By.XPATH, locators.Location_input_Xpath)
    Location_input_element.send_keys(OUTLET)

    restaurant_data["Outlet Name"] = OUTLET_NAME
    restaurant_data["Outlet"] = OUTLET
    time.sleep(3)

    First_location_in_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, locators.First_location_in_list_Xpath)))
    First_location_in_list.click()
    time.sleep(3)

    Skip_and_add_later_element = driver.find_element(By.XPATH, locators.Skip_and_add_later_Xpath)
    Skip_and_add_later_element.click()
    time.sleep(3)

    Search_element = driver.find_element(By.XPATH, locators.Search_Xpath)
    Search_element.click()
    time.sleep(3)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, locators.Search_input_Xpath)))
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

    Cuisine_tag_span = driver.find_element(By.XPATH, locators.Cuisine_tag_span_Xpath)
    restaurant_data["Tags"] = Cuisine_tag_span.text

    Resultant_restaurant_element.click()
    time.sleep(5)

    # Reached Restaurant Page

    Resultant_rating_element = driver.find_element(By.XPATH, locators.Rating_div_Xpath)
    restaurant_data["Rating"] = Resultant_rating_element.text

    Resultant_cft_element = driver.find_element(By.XPATH, locators.CFT_div_Xpath)
    restaurant_data["CFT"] = Resultant_cft_element.text

    # TODO check if deals present -> nothing prints blank
    Discount_divs = driver.find_elements(By.XPATH, locators.Discount_div_Xpath)
    discount_list = []
    for discount_div in Discount_divs:
        # 1. src attribute of the img in the first div
        img_div = discount_div.find_elements(By.TAG_NAME, "div")[0] 
        img_src = img_div.find_element(By.TAG_NAME, "img").get_attribute("src")

        if img_src == "https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_96,h_96/offers/generic":
            # 2. text of the nested divs in the second div
            text_div_container = discount_div.find_elements(By.TAG_NAME, "div")[1]
            inner_divs = text_div_container.find_elements(By.TAG_NAME, "div")
            
            text_1 = inner_divs[0].text if len(inner_divs) > 0 else ""
            text_2 = inner_divs[1].text if len(inner_divs) > 1 else ""
            # discount_list.append([text_1, text_2, img_src])
            discount_list.append([text_1, text_2])

    restaurant_data["Discounts"] = discount_list

    discounts_str = "; ".join([f"{d[0]}: {d[1]}" for d in restaurant_data["Discounts"]])
    processed_data = {
            "Name": restaurant_data["Outlet Name"],
            "Location": restaurant_data["Outlet"],
            "Rating": restaurant_data["Rating"],
            "CFT": restaurant_data["CFT"],
            "Tags": restaurant_data["Tags"],
            "Discounts": discounts_str
    }
    print(processed_data)
    restaurants_data.append(processed_data)
    

def save_excel(restaurants_data):
    for entry in restaurants_data:
        entry["Discounts"] = entry["Discounts"].replace("; ", "\n")

    df = pd.DataFrame(restaurants_data)
    df.to_excel("restaurants_data.xlsx", index=False)
    print("Data has been saved to 'restaurants_data.xlsx'")

open_and_login()

# location, name
outlets = [    
    ["Cyber City", "Sushi Haus - By Haus Delivery"],
    ["Greater Kailash 2", "Amma's Haus - by Asian Haus"],
    ["Greater Kailash 2", "Asian Haus - By Haus Delivery"],
    ["Cyber City", "Asian Haus - By Haus Delivery"],
    ["Vasant Kunj", "Asian Haus - By Haus Delivery"],
    ["Greater Kailash 2", "Masala Haus - By Asian Haus"],
    ["Greater Kailash 2", "Sushi Haus - By Haus Delivery"],
    ["Vasant Kunj", "Sushi Haus - By Haus Delivery"]
]
for outlet in outlets:
    get_data_script(outlet[0], outlet[1])


save_excel(restaurants_data)

excel_file = "restaurants_data.xlsx"
wb = load_workbook(excel_file)
ws = wb.active

for col in ws.columns:
    max_length = 0
    column = col[0].column  # Get the column index (1-based)
    column_letter = get_column_letter(column)  # Convert to Excel letter (A, B, etc.)

    # Determine the maximum length of content in the column
    for cell in col:
        try:
            if cell.value:  # Check if the cell is not empty
                max_length = max(max_length, len(str(cell.value)))
        except:
            pass

    # Set the column width
    adjusted_width = max_length + 2  # Adding a little padding
    ws.column_dimensions[column_letter].width = adjusted_width

# Save the updated workbook
wb.save(excel_file)

print("Data saved to 'restaurants_data.xlsx' with adjusted column widths and multiline discounts.")

def close_driver():
    time.sleep(3)
    driver.quit()
