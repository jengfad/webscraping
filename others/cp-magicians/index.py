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
# EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+'
EMAIL_REGEX = "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"


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
        return get_email_by_regex(description)
    except Exception as e:
        error_message = str(e)
        return ""


def get_email_by_regex(text):
    match = re.findall(EMAIL_REGEX, text)
    if (len(match) > 0):
        return match[0]

    return ""


def get_email_from_site(div):

    email = ""
    link = div.find_element(
        By.XPATH, ".//tr[1]//td//a[contains(@href, 'http')]")
    url = link.get_attribute('href')
    driver.execute_script("window.open('');")
    driver.switch_to.window(
        driver.window_handles[len(driver.window_handles) - 1])

    try:
        driver.get(url)
        WebDriverWait(driver, FIVE_SECONDS).until(
            EC.presence_of_element_located(
                (By.XPATH, "//body"))
        )

        mailto = driver.find_elements(
            By.XPATH, ".//a[contains(@href, 'mailto')]")

        if len(mailto) > 0:
            email = get_email_by_regex(mailto[0].text)
        else:
            email = get_email_by_regex(driver.page_source)

    except Exception as e:
        error_message = str(e)

    time.sleep(3)
    driver.close()
    driver.switch_to.window(
        driver.window_handles[len(driver.window_handles) - 1])

    return email


def parse_tr():
    location = get_location()
    for div in driver.find_elements(By.XPATH, "//div[contains(@align, 'center')]//table"):
        try:
            name_el = div.find_element(By.XPATH, ".//tr[1]//td[1]//a")
            name = name_el.get_attribute('name').replace("_", " ").strip()

            email = get_email_from_mailto(div)

            if email == '':
                email = get_email_from_description(div)

            if email == '':
                email = get_email_from_site(div)

            print(f"Name: {name}, Email: {email}, Location: {location}")
        except:
            time.sleep(0)


def get_location():
    current_url = driver.current_url
    prefix = '.com/Magicians-'
    suffix = '.htm#'
    start_index = current_url.find(prefix)
    end_index = current_url.find(suffix)
    return current_url[start_index + len(prefix):end_index]


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


try:
    main()

finally:
    print('done')
    driver.quit()
