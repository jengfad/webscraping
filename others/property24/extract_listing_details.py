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

def get_nullable_text(selector):
    el = driver.find_elements(By.XPATH, selector)
    if (len(el) > 0):
        return el[0].text
    else:
        return "---"

def get_nullable_bool(selector):
    el = driver.find_elements(By.XPATH, selector)
    return len(el) > 0

def get_listing_address():
    address = driver.find_elements(By.XPATH, '//div[contains(@class, "p24_listingCard p24_listingFeaturesWrapper")]/div[contains(@class, "p24_") and position() = 3]/p')
    address_fallback = driver.find_elements(By.XPATH, '//a[contains(@class, "p24_addressPropOverview")]')
    if (len(address) > 0):
        return address[0].text
    elif (len(address_fallback) > 0):
        return address_fallback[0].text
    else:
        return "---"

def get_data():
    listing_name = get_nullable_text('//div[contains(@class, "sc_listingAddress")]/h1')
    total_price = get_nullable_text('//div[contains(@class, "p24_price")]')
    listing_address = get_listing_address()
    listing_title = get_nullable_text('//div[contains(@class, "p24_listingCard")]/h5')
    listing_write_up = get_nullable_text('//div[contains(@class, "sc_listingDetailsText")]')

    bedrooms = get_nullable_text('//div[contains(@class, "p24_keyFeaturesContainer")]//div[contains(@class, "p24_listingFeatures")]//img[contains(@src, "bed")]/../../span[contains(@class, "p24_featureAmount")]')    
    bathrooms = get_nullable_text('//div[contains(@class, "p24_keyFeaturesContainer")]//div[contains(@class, "p24_listingFeatures")]//img[contains(@src, "bath")]/../../span[contains(@class, "p24_featureAmount")]')
    garages = get_nullable_text('//div[contains(@class, "p24_keyFeaturesContainer")]//div[contains(@class, "p24_listingFeatures")]//img[contains(@src, "garage")]/../../span[contains(@class, "p24_featureAmount")]')
    garden = get_nullable_bool('//div[contains(@class, "p24_keyFeaturesContainer")]//div[contains(@class, "p24_listingFeatures")]//img[contains(@src, "garden")]')
    pet_friendly = get_nullable_bool('//div[contains(@class, "p24_keyFeaturesContainer")]//div[contains(@class, "p24_listingFeatures")]//img[contains(@src, "pet")]')

    listing_number = get_nullable_text('//div[contains(@class, "p24_propertyOverviewKey") and contains(text(), "Listing Number")]/../div/div[contains(@class, "info")]')
    property_type = get_nullable_text('//div[contains(@class, "p24_propertyOverviewKey") and contains(text(), "Type of Property")]/../div/div[contains(@class, "info")]')
    street_address = get_nullable_text('//div[contains(@class, "p24_propertyOverviewKey") and contains(text(), "Street Address")]/../div/div[contains(@class, "info")]')
    list_date = get_nullable_text('//div[contains(@class, "p24_propertyOverviewKey") and contains(text(), "List Date")]/../div/div[contains(@class, "info")]')
    lot_area = get_nullable_text('//div[contains(@class, "p24_propertyOverviewKey") and contains(text(), "Lot Area")]/../div/div[contains(@class, "info")]')
    floor_area = get_nullable_text('//div[contains(@class, "p24_propertyOverviewKey") and contains(text(), "Floor Area")]/../div/div[contains(@class, "info")]')

def get_property_page(property_url):

    driver.get(property_url)
    
    try:
        WebDriverWait(driver, FIVE_SECONDS).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'p24_listingCard')]"))
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