from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import csv
import string
from random import randint

CHROME_DRIVER_PATH = "C://Repos//chromedriver_win32//chromedriver.exe"
chromeOptions = Options()
chromeOptions.add_argument("--kiosk")

driver = webdriver.Chrome(
    executable_path=CHROME_DRIVER_PATH, options=chromeOptions)

FIVE_SECONDS = 5
MAIN_URL = 'https://www.property24.com.ph/property-for-sale?ToPrice=1500000'
LETTER_URL = 'http://www.magician-directory.com/Magician-<LETTER>.htm'


def main():
    for letter in string.ascii_uppercase[:1]:
        index_url = LETTER_URL.replace("<LETTER>", letter)
        parse_letter_index_page(index_url)


def random_delay(min, max):
    seconds = randint(min, max)
    time.sleep(seconds)


def parse_letter_index_page(url):
    driver.get(url)

    try:
        WebDriverWait(driver, FIVE_SECONDS).until(
            EC.presence_of_element_located(
                (By.XPATH, "//table[contains(@class, 'MsoNormalTable')]"))
        )

        for link in driver.find_elements(By.XPATH, '//td[contains(@style, "width: 496")]//a[1]')[:1]:
            url = link.get_attribute('href')
            parse_magician_by_location_page(url)

    except Exception as e:
        error_message = str(e)
        print(error_message)


def parse_magician_by_location_page(url):
    driver.get(url)

    try:
        WebDriverWait(driver, FIVE_SECONDS).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@align, 'center')]"))
        )

        for tr in driver.find_elements(By.XPATH, "//div[contains(@align, 'center')]//tr[1]"):
            name = tr.find_element(By.XPATH, ".//td[1]/font/a[1]").text
            print(f"Name: {name}")
            try:
                email = tr.find_element(
                    By.XPATH, ".//td[2]/a[contains(@href, 'mailto')]/font").text
                print(f"Email found: {email}")
            except Exception as e:
                time.sleep(0)

    except Exception as e:
        error_message = str(e)
        print(error_message)


try:
    main()

finally:
    print('done')
    driver.quit()
