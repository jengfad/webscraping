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
import sql_connect

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
OUTPUT_PATH = 'output/data.csv'


class Contact:
    def __init__(self, name, email, location):
        self.name = name
        self.email = email
        self.location = location


def main():
    try:
        for letter in string.ascii_uppercase[:1]:
            index_url = LETTER_URL.replace("<LETTER>", letter)
            parse_letter_index_page(index_url)

    finally:
        print('done')
        driver.quit()


def random_delay(min, max):
    seconds = randint(min, max)
    time.sleep(seconds)


def parse_letter_index_page(index_letter_url):
    driver.get(index_letter_url)

    try:
        WebDriverWait(driver, FIVE_SECONDS).until(
            EC.presence_of_element_located(
                (By.XPATH, "//table[contains(@class, 'MsoNormalTable')]"))
        )

        for link in driver.find_elements(By.XPATH, '//td[contains(@style, "width: 496")]//a[1]')[:1]:
            url = link.get_attribute('href')
            parse_magician_by_location_page(url, index_letter_url)

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


def switch_to_latest_tab():
    driver.switch_to.window(
        driver.window_handles[len(driver.window_handles) - 1])


def get_website(div):
    link = div.find_elements(
        By.XPATH, ".//tr[1]//td//a[contains(@href, 'http')]")
    if (len(link) > 0):
        return link[0].text

    return ''


def get_email_from_site(url):

    email = ""
    driver.execute_script("window.open('');")
    switch_to_latest_tab()

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

    driver.close()
    switch_to_latest_tab()

    return email


def get_name(div):

    name_el = div.find_elements(By.XPATH, ".//tr[1]//td[1]//a")

    if (len(name_el) > 0):
        return name_el[0].text.strip()
    else:
        name_el = div.find_elements(By.XPATH, ".//tr[1]//td[1]//font")
        if (len(name_el) > 0):
            return name_el[0].text.strip()

    return ''


def parse_tr(index_letter_url):
    location = get_location()
    for div in driver.find_elements(By.XPATH, "//div[contains(@align, 'center')]//table"):
        name = ''
        site_url = ''
        try:
            name = get_name(div)
            if ('your name' in name.lower() or name == ''):
                continue

            existing_record = sql_connect.find_magician(name, location)

            if (existing_record is not None):
                continue

            site_url = get_website(div)
            email = get_email_from_mailto(div)

            if email == '':
                email = get_email_from_description(div)

            if email == '' and site_url != '':
                email = get_email_from_site(site_url)

            if (email != ''):
                # contact = Contact(name, email, location)
                sql_connect.insert_magician(
                    name, email, location, index_letter_url, driver.current_url, site_url)
                # append_to_csv(contact, OUTPUT_PATH, False)

        except Exception as e:
            notes = f"{name}, {site_url}, {driver.current_url}, {index_letter_url}"
            sql_connect.insert_error_logs(notes, str(e))


def get_location():
    current_url = driver.current_url
    prefix = '.com/Magicians-'
    suffix = '.htm#'
    start_index = current_url.find(prefix)
    end_index = current_url.find(suffix)
    return current_url[start_index + len(prefix):end_index]


def parse_magician_by_location_page(url, index_letter_url):

    try:
        driver.execute_script("window.open('');")
        switch_to_latest_tab()

        driver.get(url)
        WebDriverWait(driver, FIVE_SECONDS).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@align, 'center')]"))
        )

        parse_tr(index_letter_url)

    except Exception as e:
        error_message = str(e)

    driver.close()
    switch_to_latest_tab()


def append_to_csv(data, file_name, is_header):
    # Add contents of list as last row in the csv file

    with open(file_name, 'a+', newline='', encoding="utf-8") as write_obj:
        item_row = []

        for attr in dir(data):
            if attr[:2] == '__':
                continue

            if (is_header is False):
                item_row.append(getattr(data, attr))
            else:
                item_row.append(attr)

        writer = csv.writer(write_obj)
        writer.writerow(item_row)


def init_output_file(data, file_name):
    append_to_csv(data, file_name, True)


main()
