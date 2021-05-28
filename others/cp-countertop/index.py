from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse

import time
import csv
import re
from bs4 import BeautifulSoup
import random
import sql_connect
from random import randint

CHROME_DRIVER_PATH = "C://Repos//chromedriver_win32//chromedriver.exe"
chromeOptions = Options()

EMAIL_REGEX = "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
GOOGLE_URL = "https://www.google.com/"
SEARCH_TEXTS = [
    'countertop illinois',
    'countertop installation illinois',
    'countertop fabrication illinois',
]

IL_ZIPCODE = '604'
IL_ABBR = 'IL'

IL_AREA_CODES = [
    '217',
    '224',
    '309',
    '312',
    '331',
    '447',
    '618',
    '630',
    '708',
    '773',
    '779',
    '815',
    '847',
    '872'
]

EXCLUDE_SITES = [
    'www.facebook.com',
    'www.hgtv.com',
    'www.homeadvisor.com',
    'en.wikipedia.org',
    'www.homedepot.com',
    'www.linkedin.com',
    'www.nytimes.com',
    'www.pinterest.com',
    'www.yelp.com'
]

FIVE_SECONDS = 5
ONE_HOUR = 3600

OUTPUT_PATH = 'output/data.csv'

WEBSITES = [
    'lenovastone.com',
'www.marblesystems.com',
'www.cictops.com',
'tcfmidwest.com',
'graniteselection.com',
'jwcountertops.com',
'amfgranite.com',
'www.customcountertopcreations.com',
'www.builderswarehousepeoria.com',
'rayscountertopshopinc.com',
'forestcitycountertops.com',
'www.maxwellcounters.com',
'masterscountertops.com',
'www.granitemakeover.com',
'countertopsstl.com',
'www.precisionstonedesigns.com',
'www.archcitygranite.com',
'sprovieris.com',
'www.yelp.com',
'www.gemstonecountertops.com',
'www.owstone.com',
'countertopresource.com',
'usmarbleandgranite.com',
'heartlandgranite.net',
'www.surfacesolutionsil.com',
'stoneshopinc.com',
'www.tremontkitchentops.com',
'pyramidtops.com',
'www.olivasgranite.com',
'www.granitetransformations.com',
'www.msisurfaces.com',
'www.f-w-s.net',
'www.factoryplaza.com',
'www.buchecustomcounters.com',
'www.concretenetwork.com',
'www.rockcounter.com',
'signaturecountertopsil.com',
'eastsidemarblegranite.com',
'yourgraniteguy.com',
'www.deucedevelopment.net',
'www.glcountertops.com',
'topnotchcounters.com',
'bocacabinets.com',
'www.insigniastone.com',
'www.linkedin.com',
'cabinetland.net',
'www.decaturcountertop.com',
'masterskitchenbath.com',
'www.mikrondesign.com',
'chicagogranitecountertop.com',
'www.stonecrafters.com',
'selectsurfaces.net',
'www.miraclemethod.com',
'www.moderncountertops.com',
'www.marbleandgranitetech.com',
'aokcarpetcleaning.com',
'www.houzz.com',
'www.ttsgranite.com',
'www.granitecorp.com',
'www.thomasnet.com',
'www.ilgranitemarble.com',
'www.stoneedgechicago.com',
'www.silestoneusa.com',
'wlstoneworks.com',
'www.clwcountertops.com',
'cascadetops.com',
'www.shapessupply.com',
'www.wilsonart.com',
'urbancountertop.com',
'www.formica.com',
'www.hickorystreetcabinets.com',
'www.mazelumber.com',
'granitecrafter.com',
'nicegranite.com',
'www.masterbrand.com',
'yourgranitedesign.com',
'www.iscgranite.com',
'www.angi.com',
'tribecamarble.com',
'www.bluepearlstone.com',
'www.euromarblesupply.com',
'www.awardcustomtops.com',
'www.lennyscarpet.com',
'www.butcherblockchicago.com',
'www.djgraniteandmarble.com',
'lifestylekitchensbaths.com',
'www.glumber.com',
'artistic-countertops.com',
'granitefactory.net',
'timelessgraniteinc.com',
'www.kempercabinets.com',
'midwest-cabinet.com',
'bensonstone.com',
'www.midweststonesales.com',
'www.normsbargainbarn.com',
'lonniesstonecrafters.com',
'www.marble-granites.com',
'www.homedepot.com',
'ldkcountertops.com',
'web.extension.illinois.edu',
'www.mapquest.com',
'www.foxvalleybathtubrefinishing.com',
'designplusgranite.com',
'www.surfacesbypacific.com',
'www.stoneworld.com',
'www.bbb.org',
'granitecountertopschicago.com',
'www.metromarble.com',
'www.saukvalleygranite.com',
'www.craftedcountertops.com',
'www.midwestfabrication.com',
'www.nu-tub.net',
'www.caesarstoneus.com',
'www.hullscabinetshop.com',
'www.bbifinishes.com',
'mygranite.com',
'www.aetnabetterhealth.com',
'www.thekitchenmaster.com',
'rtgranite.com',
'cherrytreekitchens.com',
'www.thumbtack.com',
'www.chbuildersinc.com',
'www.midamericagranite.com',
'www.lutherfalls.com',
'vanguardtops.com',
'www.avenuemetal.com',
'sgsspringfield.com',
'www.onbroadwayflooringcabinets.com',
'aprefinishing.com',
'specialtymarbleandgranite.com',
'mega-stone.com',
'www.dnb.com',
'www.anggranite.com',
'www.menards.com',
'prairiesalescompany.com',
'www.bbformica.com',
'stone-emporium.com',
'www.arthurcountertop.com',
'www.housebeautiful.com',
'www.sirgroutchicago.com',
'en.wikipedia.org',
'www.stonetrendsllc.com',
'myaffordableinteriors.com',
'www.remodelersmart.com',
'thedesignstudiobreese.com',
'www.totalkitchenbath.com',
'www.jrcountertops.com',
'www.themidwestkitchendepot.com',
'www.daltile.com',
'www.quartzmasters.com',
'thehorizongroupinc.com',
'1soliddesigns.com',
'www.ccbrefinishing.com',
'www.kitchenaid.com',
'www.verifone.com',
'www.nytimes.com',
'www.shopstudio41.com',
'www.abt.com',
'www.lowes.com',
'www.florim.com',
'www.naperville.il.us',
'www.aamericanflooring.com',
'www.stonesource.com',
'www.kitchenandbathmart.net',
'www.baersupply.com',
'www.quikrete.com',
'gistone.com',
'www.locations.californiaclosets.com',
'lewisfloorandhome.com',
'www.richelieu.com',
'www.midwaydisplays.com',
'www.prosourcewholesale.com',
'bnqv.lenozzemagazine.it',
'patch.com',
'www.crestwoodcustomcabinets.com',
'kitchensolvers.com',
'www.roomandboard.com',
'www.apartments.com',
'www.elmwoodreclaimedtimber.com',
'newsotime.com',
'newageproducts.com',
'www.lennar.com',
'www.lg.com',
'www.gmlighting.net',
'www.closetfactory.com',
'www.schweighardtconcrete.com',
'www.flooranddecor.com',
'www.thespruce.com',
'www.northriverside-il.org',
'sieuweb.site',
'rh.com',
'www.neolith.com',
'www.pantagraph.com',
'icestoneusa.com',
'www.sj-r.com',
'www.pinterest.com',
'suphome.net',
'www.expertise.com',
'www.semocountertops.com',
'granitecountertopinstallerchicago.com',
'www.countertopexpertsusa.com',
'www.fixr.com',
'www.newcoriancounters.com',
'grayslake.kitchensolvers.com',
'www.galaxystonedesign.com',
'countertops.promatcher.com',
'newstonedesign.net',
'www2.illinois.gov',
'www.heartlandcabinetry.org',
'granitesolutionone.com',
'graniteamerica.com',
'allstonetops.com',
'graniteandstoneleaders.com',
'porch.com',
'graniteheroes.com',
'www.bestbuycarpets.com',
'www.stevesflooring-design.com',
'www.yellowpages.com',
'stoneexact.com',
'granite-mountain.com',
'mgstonesurface.com',
'cahillinc.com',
'countertopsmarionil.com',
'www.acornmarble.com',
'reviews.listen360.com',
'www.prairieprideinc.com',
'dtkstoneworks.com',
'www.psalaboratoryfurniture.com',
'www.kitchen-land.com',
'reviews.birdeye.com',
'www.valpak.com',
'www.indeed.com',
'www.diamondcutgranite.net',
'www.darkstarmarble.com',
'www.concordcabinetsinc.com',
'www.bosscarpetone.com',
'www.stoneillusionz.com',
'www.eashstoneworks.com',
'www.kitchenbathandcabinetco.com',
'chicagocustomkitchens.com',
'www.cambriausa.com',
'www.granitefabricatordirect.net',
's2ch.cnrs.fr',
'mcaj.paolodrigo.it',
'www.tileshop.com',
'www.carpetone.com',
'milwaukeemarble.com',
'www.mrhandyman.com',
'www.cosentino.com',
'mok.pasticceriadorina.it',
'laticrete.com',
'zzay.shoox.it',
'chicagostonecontractors.com',
'mvuk.flube.it',
'www.youtube.com',
'jdtouchcountertops.com',
'www.mortensonroofing.com',
'www.familyhandyman.com',
'marblegraniteslabs.com',
'www.chicagometrostone.com',
'mgmstonefabrication.com',
'www.naturalstoneinc.net',
'www.tithoftile.com',
'www.dmfcustomstoneworks.com',
'www.custommarbledesign.net',
'wolfstonedesign.com',
'www.stone-systems.com',
'www.hardrockfabricatorsinc.com',
'www.rockfordgranite.com',
'www.ziprecruiter.com',
'www.isfanow.org',
'www.stoneexperts.com',
'stonemasters99.com',
'www.stonetekdesign.com',
'www.marbleemporiumchicago.com',
'gmdchicago.us',
'www.alexgraniteandmarble.com',
'easystoneshop.com',
'custommetalhome.com',
'www.loopnet.com',
'chicagostonegallery.com',
'www.corian.com',
'www.chicagostainlesssteel.com',
'www.sfistone.com',
'chicagoconcretestudio.com',
'www.stonecogranite.com',
'classicgraniteandmarbleil.com',
'global-stoneinc.com',
'associationdatabase.com',
'www.nprillinois.org',
'idlccompany.com',
'marble-works.com',
'www.tristategranitetops.com',
'www.chicagograniteshop.com',
'understargranite.com',
'www.thecountertopfactory.com',
'sweethomeimp.wpengine.com',
'mirageaz.com',
'thedavanigroup.com',
'ivja.milanopark.it',
'www.himacscountertops.com',
'www.materials-marketing.com',
'ombz.kelvinled.it',
'dsqc.shoppingincitta.it',
'bpz.ristoranteilbettolino.it',
'www.bcstone.com',
'ytvg.pasticceriadolciidee.it',
'fyyd.tobiasrestaurant.it',
'www.amerhart.com',
'sgln.modica5stelle.it',
'www.gemathis.com',
'www.greatlakesgm.com',
'rissco.com',
'chicagofabrications.com',
'midwesttile.com'
]


class ExtractDetails:
    def __init__(self, url, email, phone, location):
        self.url = url
        self.email = email
        self.phone = phone
        self.location = location


def random_delay(min, max):
    seconds = randint(min, max)
    time.sleep(seconds)


def extract_email():
    soup = BeautifulSoup(driver.page_source, "lxml")

    results = ''
    for email in soup.find_all(text=re.compile(EMAIL_REGEX)):
        x = re.findall(EMAIL_REGEX, email)
        item = x[0].lower()
        if item not in results:
            results = results + ', ' + item

    # has email/s
    if results:
        return results[2:len(results)]

    return 'none'


def element_exists_by_xpath(selector):
    try:
        driver.find_element(By.XPATH, selector)
    except NoSuchElementException:
        return False
    return True


def extract_location():

    selectorAbbr = f".//*[contains(text(),'IL 6')]"
    selectorFull = f".//*[contains(text(),'Illinois')]"

    if element_exists_by_xpath(selectorAbbr):
        location = driver.find_element(By.XPATH, selectorAbbr).text
        return location

    if element_exists_by_xpath(selectorFull):
        location = driver.find_element(By.XPATH, selectorFull).text
        return location

    return ''


def extract_phone():

    for code in IL_AREA_CODES:
        selector = f".//*[contains(text(),'{code}')]"

        if element_exists_by_xpath(selector):
            phone = driver.find_element(By.XPATH, selector).text
            return phone

    return ""


def extract_details_from_page(contact_url, website):

    try:
        driver.get(contact_url)
    except:
        sql_connect.update_data(website, 'none', '', '')
        return

    WebDriverWait(driver, ONE_HOUR).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'html'))
    )

    phone = extract_phone()
    location = extract_location()
    email = extract_email()

    sql_connect.update_data(website, email, location, phone)

    random_delay(5, 10)


def is_site_valid(url):

    if url in EXCLUDE_SITES:
        return False

    existing_record = sql_connect.find_data(url)
    if existing_record is not None:
        return False

    return True


def get_contact_website(website):

    random_delay(5, 10)

    driver.get(GOOGLE_URL)

    WebDriverWait(driver, FIVE_SECONDS).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input'))
    )

    search_text = website + ' contact'

    search_input_el = driver.find_element_by_xpath("//input")
    search_input_el.send_keys(search_text)
    search_input_el.send_keys(Keys.RETURN)

    WebDriverWait(driver, ONE_HOUR).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.g a'))
    )

    link = driver.find_element_by_xpath(
        '//div[@class="g"]//a').get_attribute('href')

    extract_details_from_page(link, website)


def test_update():
    sql_connect.update_data('www.yelp.com', 'test@email.com',
                            'Illinois', '902-202-1233')


def update_website_data():
    results = sql_connect.get_all_data()
    count = len(results)
    for index, data in enumerate(results):
        website = data[4]
        get_contact_website(website)
        print(f'extracted {index} of {count} - {website}')


def get_website():

    index = 0
    total = 1

    while index < total:

        profiles = driver.find_elements(By.XPATH, "//div[@class='g']")
        total = len(profiles)

        current_profile = profiles[index]
        link = current_profile.find_element(
            By.XPATH, ".//a").get_attribute('href')

        link = urlparse(link).hostname

        if is_site_valid(link):
            sql_connect.insert_data("", "", "", link)

        random_delay(5, 10)
        index = index + 1

        # if (index == 5):
        #     break


def google_search(search_text):

    WebDriverWait(driver, FIVE_SECONDS).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input'))
    )

    search_input_el = driver.find_element_by_xpath("//input")
    search_input_el.send_keys(search_text)
    search_input_el.send_keys(Keys.RETURN)

    page_num = 0
    while True:
        try:
            WebDriverWait(driver, FIVE_SECONDS).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#search'))
            )
            page_num = page_num + 1
            print(f'On page {page_num} ' + search_text)

            get_website()

            # if page_num == 2:
            #     break

            next_button = driver.find_element(
                By.XPATH, "//td[@role='heading']//a[@id='pnnext']")

            random_delay(5, 10)
            next_button.click()

        except NoSuchElementException:
            break
        except TimeoutException:
            break

def insert_static_data():
    for site in WEBSITES:
        sql_connect.insert_data("", "", "", site)

try:

    start_time = time.time()
    driver = webdriver.Chrome(
        executable_path=CHROME_DRIVER_PATH, options=chromeOptions)

    driver.get(GOOGLE_URL)

    time.sleep(10)

    # DO NOT RUN STEP 1 AND 2 AT THE SAME TIME

    # STEP1 - Extract website links first
    # for search_text in SEARCH_TEXTS:
    #     google_search(search_text)

    # STEP2 - Extract website details
    update_website_data()


    elapsed_time = time.time() - start_time
    print(f'TIME ELAPSED: {elapsed_time}')

finally:
    print('done')
    # driver.quit()
