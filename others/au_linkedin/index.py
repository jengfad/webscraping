from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys

import time
import csv
from bs4 import BeautifulSoup
import re
import pandas as pd
import random


CHROME_DRIVER_PATH = "C://Repos//chromedriver_win32//chromedriver.exe"
chromeOptions = Options()
# chromeOptions.add_argument("--headless")
# chromeOptions.add_argument('--disable-gpu')
chromeOptions.add_argument('--kiosk')
chromeOptions.add_argument('--kiosk')
EMAIL_REGEX = "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
GOOGLE_URL = "https://www.google.com/"
LINKEDIN_URL = "https://www.linkedin.com/"
LINKEDIN_USERNAME = '--'
LINKEDIN_PASSWORD = '--'

FIVE_SECONDS = 5

OUTPUT_PATH = 'output/data.csv'

class PersonDetails:  
    def __init__(self, full_name, location, position): 
        self.location = location

        suffix_index = position.index(' at ')
        self.position = position[:suffix_index]
        
        name_parts = full_name.split()
        self.last_name = name_parts.pop()
        self.first_name = ' '.join(name_parts)

def append_to_csv(data, file_name, is_header):
    # Add contents of list as last row in the csv file
    
    with open(file_name, 'a+', newline='') as write_obj:
        item_row = []

        for attr in dir(data):
            if attr[:2] == '__':
                continue

            if (is_header is False):
                item_row.append(getattr(data,attr))
            else:
                item_row.append(attr)

        writer = csv.writer(write_obj)
        writer.writerow(item_row)

def extract_linkedin():

    try:
        header = WebDriverWait(driver, FIVE_SECONDS).until(
            EC.presence_of_element_located((By.XPATH, ".//div[@class='ph5 pb5']/div[@class='display-flex mt2']/div[@class='flex-1 mr5']"))
        )
        full_name = header.find_element(By.XPATH, "./ul[1]/li[1]").text
        position = header.find_element(By.XPATH, "./h2").text
        location = header.find_element(By.XPATH, "./ul[2]/li[1]").text

        time.sleep(2)

        details = PersonDetails(full_name, location, position)
        append_to_csv(details, OUTPUT_PATH, False)

    except:
        print('NO DATA FOUND')

def get_profile_data():

    index = 0
    total = 1

    while index < total:

        profiles = driver.find_elements(By.XPATH, "//div[@class='g']")
        total = len(profiles)

        current_profile = profiles[index]
        current_profile.find_element(By.XPATH, ".//h3").click()
        extract_linkedin()
        driver.execute_script("window.history.go(-1)") #go back to google page
        time.sleep(2)
        index = index + 1

def login_to_linkedin():
    driver.get(LINKEDIN_URL)

    WebDriverWait(driver, FIVE_SECONDS).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input'))
    )

    driver.find_element(By.XPATH, '//input[@autocomplete="username"]').send_keys(LINKEDIN_USERNAME)
    driver.find_element(By.XPATH, '//input[@autocomplete="current-password"]').send_keys(LINKEDIN_PASSWORD)
    driver.find_element(By.XPATH, '//button[@class="sign-in-form__submit-button"]').click()

    time.sleep(1)

def google_search():

    driver.get(GOOGLE_URL)

    WebDriverWait(driver, FIVE_SECONDS).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input'))
    )

    search_text = 'site:au.linkedin.com AND intitle:rio tinto AND "field services"'
    # search_text = 'site:ph.linkedin.com AND intitle:joane marie llamera'
    search_input_el = driver.find_element_by_xpath("//input[@title='Search']")
    search_input_el.send_keys(search_text)
    search_input_el.send_keys(Keys.RETURN)

    while True:
        page_num = 0
        try:
            WebDriverWait(driver, FIVE_SECONDS).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#search'))
            )
            page_num = page_num + 1
            print (f'On page {page_num}')
            get_profile_data()

            next_button = driver.find_element(By.XPATH, "//td[@role='heading']//span[text()='Next']")

            random_timeout = random.randint(1,5)
            time.sleep(random_timeout)
            next_button.click()
    
        except NoSuchElementException:
            break
        except TimeoutException:
            break

try:

    start_time = time.time()
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)

    login_to_linkedin()
    google_search()


    elapsed_time = time.time() - start_time
    print(f'TIME ELAPSED: {elapsed_time}')

finally:
    print('done')
    driver.quit()

