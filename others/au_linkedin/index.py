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

FIVE_SECONDS = 5


def extract_linkedin():

    try:
        header_selector = ".//div[@class='ph5 pb5']/div[@class='display-flex mt2']/div[@class='flex-1 mr5']"
        header = WebDriverWait(driver, FIVE_SECONDS).until(
            EC.presence_of_element_located((By.XPATH, header_selector))
        )
        # header = driver.find_element(By.XPATH, header_selector)
        full_name = header.find_element(By.XPATH, "./ul[1]/li[1]").text #2nd text element
        position = header.find_element(By.XPATH, "./h2").text #2nd text element
        location = header.find_element(By.XPATH, "./ul[2]/li[1]").text #2nd text element

        time.sleep(3)

        print(full_name)
        print(position)
        print(location)
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

    driver.find_element(By.XPATH, '//input[@autocomplete="username"]').send_keys('jlfadriquela02@gmail.com')
    driver.find_element(By.XPATH, '//input[@autocomplete="current-password"]').send_keys('penny3x???')
    driver.find_element(By.XPATH, '//button[@class="sign-in-form__submit-button"]').click()

    time.sleep(1)

def google_search():

    driver.get(GOOGLE_URL)

    WebDriverWait(driver, FIVE_SECONDS).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input'))
    )

    # search_text = 'site:au.linkedin.com AND intitle:rio tinto AND "field services"'
    search_text = 'site:ph.linkedin.com AND intitle:joane marie llamera'
    search_input_el = driver.find_element_by_xpath("//input[@title='Search']")
    search_input_el.send_keys(search_text)
    search_input_el.send_keys(Keys.RETURN)

    while True:
        try:
            WebDriverWait(driver, FIVE_SECONDS).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#search'))
            )
            
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

