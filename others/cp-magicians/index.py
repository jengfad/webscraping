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
import re

CHROME_DRIVER_PATH = "C://Repos//chromedriver_win32//chromedriver.exe"
chromeOptions = Options()
chromeOptions.add_argument("--kiosk")

driver = webdriver.Chrome(
    executable_path=CHROME_DRIVER_PATH, options=chromeOptions)

FIVE_SECONDS = 5
MAIN_URL = 'https://www.property24.com.ph/property-for-sale?ToPrice=1500000'
LETTER_URL = 'http://www.magician-directory.com/Magician-<LETTER>.htm'
EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+'


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

        for link in driver.find_elements(By.XPATH, '//td[contains(@style, "width: 496")]//a[1]')[:3]:
            url = link.get_attribute('href')
            parse_magician_by_location_page(url)

    except Exception as e:
        error_message = str(e)
        print(error_message)


def get_email_from_mailto(div):
    try:
        email = div.find_element(
            By.XPATH, ".//tr[1]//td//a[contains(@href, 'mailto')]/font").text
        return email
    except:
        return ""


def get_email_from_description(div):
    try:
        description = div.find_element(By.XPATH, ".//tr[2]/td/font").text
        match = re.findall(EMAIL_REGEX, description)

        if (len(match) > 0):
            return match[0]

        return ""
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return ""


def get_email_from_site(div):
    try:
        link = div.find_element(
            By.XPATH, ".//tr[1]//td//a[contains(@href, 'http')]")
        url = link.get_attribute('href')
        return url

    except Exception as e:
        error_message = str(e)
        print(error_message)
        return ""


def parse_tr():
    for div in driver.find_elements(By.XPATH, "//div[contains(@align, 'center')]//table"):
        try:
            name_el = div.find_element(By.XPATH, ".//tr[1]//td[1]//a")
            name = name_el.get_attribute('name').replace("_", " ").strip()

            email = get_email_from_mailto(div)

            if email == '':
                email = get_email_from_description(div)

            if email == '':
                email = get_email_from_site(div)

            print(f"Name: {name}, Email: {email}")
        except:
            time.sleep(0)


def parse_magician_by_location_page(url):
    driver.get(url)

    try:
        WebDriverWait(driver, FIVE_SECONDS).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@align, 'center')]"))
        )

        parse_tr()

    except Exception as e:
        error_message = str(e)
        print(error_message)


try:
    main()

finally:
    print('done')
    driver.quit()
