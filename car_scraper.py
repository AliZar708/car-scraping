import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

class ChromeDriver(object):
    """
    Manage Chrome Driver by this class
    """

    def __init__(self) -> None:
        self.driver = None

    def start(self, options=None) -> WebDriver:
        service = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        return self.driver

    def close(self) -> None:
        self.driver.close()


class CarsScraping:

    def __init__(self):
        self.driver = None
        self.chrome_obj = None

    def split_string(self, input_str):
        parts = input_str.split(' ', 2)  # Split only on the first two spaces
        if len(parts) == 3:
            part1 = parts[0]  # First word (year)
            part2 = parts[1]  # Second word (brand)
            part3 = parts[2]  # Remaining words (model)
            return part1, part2, part3
        else:
            return None

    def close_notable_highlights(self):
        try:
            close_notable_highlights_btn_xpath = '//div[@class="vehicle-card"]'
            close_notable_highlights_btn = WebDriverWait(self.driver, 5).until(
                ec.presence_of_element_located((By.XPATH, close_notable_highlights_btn_xpath))
            )
        except:
            pass

    def start_scraping(self):
        self.chrome_obj = ChromeDriver()
        self.driver = self.chrome_obj.start()
        self.driver.maximize_window()
        self.driver.get("https://www.cars.com/shopping/results/?dealer_id=&include_shippable=false&keyword=&list_price_max=&list_price_min=&maximum_distance=30&mileage_max=&monthly_payment=&page_size=20&sort=best_match_desc&stock_type=all&year_max=&year_min=&zip=60606")
        time.sleep(2)
        try:
            accept_all_cookies_xpath = '//button[@id="onetrust-accept-btn-handler"]'
            accept_all_cookies = WebDriverWait(self.driver, 5).until(
                ec.presence_of_element_located((By.XPATH, accept_all_cookies_xpath))
            )
            accept_all_cookies.click()
        except Exception as e:
            print("Cookies could not be opened", e)

        file_path = "cars_data.xlsx"
        if os.path.exists(file_path):
            # Try reading the existing Excel file
            try:
                df = pd.read_excel(file_path)
            except ValueError:
                # If the Excel file is empty, initialize an empty DataFrame with columns
                df = pd.DataFrame(columns=["car_make", "model", "year", "price", "dealer_phone_number"])
        else:
            # If the file doesn't exist, create a DataFrame with the necessary columns
            df = pd.DataFrame(columns=["car_make", "model", "year", "price", "dealer_phone_number"])

        for i in range(500):
            car_page_list_xpath = '//div[@class="vehicle-card"]/a'
            car_page_list = WebDriverWait(self.driver, 5).until(
                ec.presence_of_all_elements_located((By.XPATH, car_page_list_xpath))
            )
            for i in range(0, len(car_page_list)):
                self.driver.get(car_page_list[i].get_attribute('href'))

                time.sleep(3)
                car_title_xpath = '//h1[@class="listing-title"]'
                car_title = WebDriverWait(self.driver, 5).until(
                    ec.presence_of_element_located((By.XPATH, car_title_xpath))
                )
                year, car_make, model = self.split_string(car_title.text)

                price_xpath = '//div[@class="price-section "]'
                price = WebDriverWait(self.driver, 5).until(
                    ec.presence_of_element_located((By.XPATH, price_xpath))
                )
                price_text = price.text

                dealer_phone_number_xpath = '//div[@class="dealer-phone"]'
                dealer_phone_number = WebDriverWait(self.driver, 5).until(
                    ec.presence_of_element_located((By.XPATH, dealer_phone_number_xpath))
                )

                dealer_phone_number_text = dealer_phone_number.text.replace("Call ", "")
                new_data = pd.DataFrame({
                    "car_make": [car_make],
                    "model": [model],
                    "year": [year],
                    "price": [price_text],
                    "dealer_phone_number": [dealer_phone_number_text]
                })
                df = pd.concat([df, new_data], ignore_index=True)
                with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)

                self.driver.back()
                if i == 19:
                    next_btn_xpath = '//spark-button[@aria-label="Next page"]'
                    next_btn = WebDriverWait(self.driver, 5).until(
                        ec.presence_of_element_located((By.XPATH, next_btn_xpath))
                    )
                    next_btn.click()
                else:
                    car_page_list_xpath = '//div[@class="vehicle-card"]/a'
                    car_page_list = WebDriverWait(self.driver, 5).until(
                        ec.presence_of_all_elements_located((By.XPATH, car_page_list_xpath))
                    )


if __name__ == '__main__':
    cars_scraping = CarsScraping()
    cars_scraping.start_scraping()