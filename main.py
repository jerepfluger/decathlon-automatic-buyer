import argparse
import time

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

parser = argparse.ArgumentParser()
parser.add_argument('--link', type=str, help='Link al producto que desea comprar')
parser.add_argument('--size', type=str, help='Tamaño de la bicicleta que desea comprar. Ej: "L - 175-184CM"')
parser.add_argument('--email', type=str, help='El mail con el cual se va loguear en su cuenta')
parser.add_argument('--password', type=str, help='El password de su cuenta')
parser.add_argument('--region', type=str, help='La region donde desear retirar su producto. Ej: "Comunidad de Madrid", "Euskadi"')
parser.add_argument('--city', type=str, help='La ciudad donde retirará su producto. Ej: "City Vitoria (centro ciudad)"')
parser.add_argument('--card_number', type=str, help='Numero de la tarjeta con la que va pagar')
parser.add_argument('--card_expiration_month', type=str, help='El mes de expiracion de la tarjeta. Ej: "02", "07", "10"')
parser.add_argument('--card_expiration_year', type=str, help='El año de expiracion de la tarjeta. Ej: "2022", "2026", "2030"')
parser.add_argument('--card_secure_code', type=str, help='El codigo de seguridad de la tarjeta (tiene 3 digitos')

args = parser.parse_args()

LINK = args.link
BIKE_SIZE = args.size
EMAIL = args.email
PASSWORD = args.password
REGION = args.region
CITY = args.city
CARD_NUMBER = args.card_number
CARD_EXPIRATION_MONTH = args.card_expiration_month
CARD_EXPIRATION_YEAR = args.card_expiration_year
CARD_SECURE_CODE = args.card_secure_code


def start_browser():
    options = FirefoxOptions()
    options.binary_location = '/Applications/Firefox.app/Contents/MacOS/firefox-bin'
    options.add_argument('--new_instance')

    firefox_profile = webdriver.FirefoxProfile()
    #  https://developer.mozilla.org/en-US/docs/Mozilla/Preferences/Mozilla_networking_preferences
    firefox_profile.set_preference('browser.cache.disk.enable', 'true')
    firefox_profile.set_preference('browser.cache.memory.enable', 'true')
    # https://github.com/mozilla/geckodriver/issues/517#issuecomment-286701282
    firefox_profile.set_preference("browser.tabs.remote.autostart", "false")
    firefox_profile.set_preference("browser.tabs.remote.autostart.1", "false")
    firefox_profile.set_preference("browser.tabs.remote.autostart.2", "false")
    firefox_profile.set_preference("browser.tabs.remote.force-enable", "false")
    # more settings
    firefox_profile.set_preference("dom.ipc.processCount", "1")
    firefox_profile.set_preference("browser.sessionstore.interval", "50000000")
    firefox_profile.set_preference("browser.sessionstore.max_resumed_crashes", "0")
    firefox_profile.set_preference("browser.sessionstore.max_tabs_undo", "0")
    firefox_profile.set_preference("browser.sessionstore.max_windows_undo", "0")
    firefox_profile.set_preference("dom.popup_maximum", 0)
    firefox_profile.set_preference("privacy.popups.showBrowserMessage", False)
    firefox_profile.set_preference("privacy.popups.disable_from_plugins", 3)

    return webdriver.Firefox(firefox_profile=firefox_profile, options=options)


while True:
    try:
        driver = start_browser()
        driver.maximize_window()
        driver.get(LINK)
        # Waiting for login page to be fully loaded
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'didomi-continue-without-agreeing')))
            cookies_popup = driver.find_element(By.CLASS_NAME, 'didomi-continue-without-agreeing')
            driver.execute_script("arguments[0].click();", cookies_popup)
        except TimeoutException:
            # In case pop up is not present lets check for other element
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'app')))

        driver.execute_script('window.scrollTo(0, 100);')
        size_selector = driver.find_element(By.XPATH, './/span[text()="Elegir talla"]')
        driver.execute_script("arguments[0].click();", size_selector)
        select_size = driver.find_element(By.XPATH, './/span[contains(text(),"{}")]'.format(BIKE_SIZE))
        driver.execute_script("arguments[0].click();", select_size)

        # Check availability
        try:
            availability_check = driver.find_element(By.XPATH, './/button[@class="cta cta--block CheckStoreStock"]')
            # If we pass this then there is no availability
            if availability_check.text == 'VER DISPONIBILIDAD EN TIENDA':
                print('No availability. We\'ll start again')
                raise Exception('No availability')
        except NoSuchElementException:
            pass
        try:
            driver.find_element(By.XPATH, './/button[text()="Añadir a la cesta"]')
        except NoSuchElementException:
            print('Unable to locate "Add to cart" button')
            raise Exception('Unable to locate "Add to cart" button')

        add_to_cart_button = driver.find_element(By.XPATH, './/button[text()="Añadir a la cesta"]')
        driver.execute_script("arguments[0].click();", add_to_cart_button)
        time.sleep(5)

        # Redirect driver to cart page
        driver.get('https://www.decathlon.es/es/checkout/cart')
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'mounting-component')))

        # Click buy
        accept_button = driver.find_element(By.XPATH, './/button[text()="Comenzar pedido"]')
        driver.execute_script("arguments[0].click();", accept_button)

        # Wait for email element to be loaded
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'input-email')))
        email_input = driver.find_element(By.ID, 'input-email')
        email_input.send_keys(EMAIL)
        # Click next button
        next_button = driver.find_element(By.ID, 'lookup-btn')
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(5)

        # Insert password
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'input-password')))
        password_input = driver.find_element(By.ID, 'input-password')
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.ENTER)
        time.sleep(5)

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, './/h2[text()="Recogida en tienda"]')))

        store_pick_up_menu = driver.find_element(By.XPATH, './/h2[text()="Recogida en tienda"]')
        driver.execute_script("arguments[0].click();", store_pick_up_menu)

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, './/span[contains(@class, "icon-container")]')))
        regions_selector = driver.find_element(By.XPATH, './/span[contains(@class, "icon-container")]')
        driver.execute_script("arguments[0].click();", regions_selector)
        time.sleep(5)
        region_select = driver.find_element(By.XPATH, './/li[text()="{}"]'.format(REGION))
        driver.execute_script("arguments[0].click();", region_select)

        time.sleep(5)
        city_selector = driver.find_element(By.XPATH, './/div[text()="{}"]'.format(CITY))
        driver.execute_script("arguments[0].click();", city_selector)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        continue_to_payment_button = driver.find_element(By.XPATH, './/button[text()="Continuar con el pago"]')
        continue_to_payment_button.click()

        time.sleep(5)
        driver.refresh()
        time.sleep(5)
        pay_button = driver.find_element(By.XPATH, './/button[text()="Realizar pago"]')
        driver.execute_script("arguments[0].click();", pay_button)

        # Insert card data
        time.sleep(5)
        card_number_input = driver.find_element(By.ID, 'hidCardNumber')
        card_number_input.send_keys(CARD_NUMBER)

        expiry_month_selector = Select(driver.find_element(By.ID, 'hidMonth'))
        expiry_month_selector.select_by_visible_text(CARD_EXPIRATION_MONTH)
        expiry_year_selector = Select(driver.find_element(By.ID, 'hidYear'))
        expiry_year_selector.select_by_visible_text(CARD_EXPIRATION_YEAR)

        cvv_input = driver.find_element(By.ID, 'hidCvv')
        cvv_input.send_keys(CARD_SECURE_CODE)

        accept_button = driver.find_element(By.ID, 'hidAccept')
        driver.execute_script("arguments[0].click();", accept_button)

        break
    except Exception as ex:
        print(ex.__str__())
        try:
            driver.close()
            driver.quit()
        except NameError:
            pass
        if ex.__str__() == 'No availability':
            time.sleep(60)

time.sleep(30)
print("Hemos llegado al final del proceso. En este momento le debería llegar una notificación de que la compra "
      "ha sido exitosa")
print("Por favor confirme desde la aplicación de N26 y luego que la compra se ha completado exitosamente desde "
      "su cuenta Decathlon")
end = input("Luego de la confirmación de esto, puede usted cerrar este programa. Muchas gracias")
