from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import csv
from random import randint
from property import Property
import utilities

CHROME_DRIVER_PATH = "C://Repos//chromedriver_win32//chromedriver.exe"
chromeOptions = Options()
chromeOptions.add_argument("--kiosk")

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)

FIVE_SECONDS = 5
MAIN_URL = 'https://www.property24.com.ph/property-for-sale?ToPrice=1500000'
OUTPUT_PATH = 'output/listing-details.csv'

def get_nullable_data(selector):
    el = driver.find_element(By.XPATH, selector)
    if (el is not None):
        return el.text
    else:
        return "---"


def get_data():
    listing_name = driver.find_element(By.XPATH, '//div[contains(@class, "sc_listingAddress")]/h1').text
    total_price = driver.find_element(By.XPATH, '//div[contains(@class, "p24_price")]').text
    listing_address = driver.find_element(By.XPATH, '//div[contains(@class, "p24_listingCard p24_listingFeaturesWrapper")]/div[contains(@class, "p24_") and position() = 3]/p').text
    listing_title = driver.find_element(By.XPATH, '//div[contains(@class, "p24_listingCard")]/h5').text
    listing_write_up = driver.find_element(By.XPATH, '//div[contains(@class, "sc_listingDetailsText")]').text

    bedrooms = get_nullable_data('//div[contains(@class, "p24_keyFeaturesContainer")]//div[contains(@class, "p24_listingFeatures")]//img[contains(@src, "bed")]/../../span[contains(@class, "p24_featureAmount")]')    
    # bathrooms = driver.find_element(By.XPATH, '//div[contains(@class, "p24_keyFeaturesContainer")]//div[contains(@class, "p24_listingFeatures")]//img[contains(@src, "bath")]/../../span[contains(@class, "p24_featureAmount")]').text
    # garages = driver.find_element(By.XPATH, '//div[contains(@class, "p24_keyFeaturesContainer")]//div[contains(@class, "p24_listingFeatures")]//img[contains(@src, "garage")]/../../span[contains(@class, "p24_featureAmount")]').text
    
    print(f'bedrooms {bedrooms}')

def get_property_page(property_url):

    driver.get(property_url)
    
    try:
        WebDriverWait(driver, FIVE_SECONDS).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.p24_listingFeaturesWrapper"))
        )
        utilities.time_delay()
        get_data()

    except Exception as e:
        print(e)
        print('NO DATA FOUND')


try:
    urls = [
        'https://www.property24.com.ph/3-bedroom-house-and-lot-for-sale-in-quezon-city-116480188',
        'https://www.property24.com.ph/lot-for-sale-in-alfonso-cavite-116471156'
    ]
    start_time = time.time()
    for url in urls:
        get_property_page(url)

    elapsed_time = time.time() - start_time
    print(f'TIME ELAPSED: {elapsed_time}')

finally:
    print('done')
    driver.quit()