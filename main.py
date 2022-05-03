import argparse
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

parser = argparse.ArgumentParser()
parser.add_argument('--size', type=str, help='Tamaño de la bicicleta que desea comprar. Ej: "L - 175-184CM"')
parser.add_argument('--email', type=str, help='El mail con el cual se va loguear en su cuenta')
parser.add_argument('--password', type=str, help='El password de su cuenta')
parser.add_argument('--ciudad', type=str, help='Nombre de la ciudad en la cual desea obtener una cita. Ej: "MALLORCA"')
parser.add_argument('--tipo_cita', type=str, help='El tipo de Cita que desea obtener. Ej: "INFORMACION GENERAL - IBIZA", "POLICIA-CERTIFICADOS Y ASIGNACION NIE"')
parser.add_argument('--tipo_documento', type=str, choices=['NIE', 'DNI', 'PASAPORTE'], help='El tipo de documento con el que realizara el pedido de cita. NIE, DNI o PASAPORTE')
parser.add_argument('--documento', type=str, help='El numero de documento en cuestion con el que realizara el tramite')
parser.add_argument('--nacimiento', type=str, help='El año de su nacimiento en formato de 4 números. Ej: 1987, 1993')
parser.add_argument('--nacionalidad', type=str, help='El país de nacionalidad de su documento')
parser.add_argument('--nombre', type=str, help='El nombre completo de la persona que va realizar el tramite')
parser.add_argument('--telefono', type=str, help='Su numero de telefono. Solo se aceptan telefonos españoles. NO anteponga el prefijo "+34"')
parser.add_argument('--elegir_cita_automaticamente', type=str, choices=['SI', 'NO'], help='En caso que elija "SI" el sistema automáticamente le elegira la primer cita disponible. En caso de elegir "NO" usted podrá elegir la cita de su mayor conveniencia')
args = parser.parse_args()

BIKE_SIZE = args.size
EMAIL = args.email
PASSWORD = args.password
CITY = args.ciudad
APPOINTMENT_TYPE = args.tipo_cita
DOCUMENT_TYPE = args.tipo_documento
DOCUMENT = args.documento
BIRTH_YEAR = args.nacimiento
NATIONALITY = args.nacionalidad
NAME = args.nombre
PHONE = args.telefono
POLICE_APPOINTMENTS = {'POLICIA', 'POLICÍA', 'CERTIFICADO', 'AUTORIZACIÓN', 'ASILO'}

driver = webdriver.Chrome()
appointment_available = False


def get_appointment_type_id(appointment_type):
    if appointment_type.split()[0].split('-')[0].upper() in POLICE_APPOINTMENTS:
        return 'tramiteGrupo[1]'

    return 'tramiteGrupo[0]'


def print_choosing_appointment_message():
    print('NO CIERRE EL PROGRAMA AÚN!')
    print('Debe seleccionar en este punto la cita deseada y luego completar con los datos faltantes')
    print('Una vez que tenga confirmada su cita ya podrá cerrar el programa')


def get_city_text(city_options):
    for city in city_options:
        if CITY.upper() in city:
            return city
    return ''


while True:
    try:
        driver.maximize_window()
        # driver.get('https://www.decathlon.es/es/p/bicicleta-montana-allmountain-am-100-hardtail/_/R-p-331946')
        driver.get("https://www.decathlon.es/es/p/bicicleta-electrica-de-montana-rockrider-ebike-st-100-27-5-azul/_/R-p-309736?mc=8560739")
        # Waiting for login page to be fully loaded
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'didomi-continue-without-agreeing')))
            cookies_popup = driver.find_element(By.CLASS_NAME, 'didomi-continue-without-agreeing')
            driver.execute_script("arguments[0].click();", cookies_popup)
        except TimeoutException:
            # In case pop up is not present lets check for other element
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'app')))

        driver.execute_script('window.scrollTo(0, 100);')
        actions = ActionChains(driver)
        size_selector = driver.find_element(By.ID, 'product-size-selection')
        actions.move_to_element(size_selector).perform()
        size_selector = Select(size_selector)
        size_selector.select_by_visible_text(BIKE_SIZE)
        # driver.execute_script("arguments[0].scrollIntoView();", )
        # size_selector = driver.find_element(By.XPATH, './/div[@class="select svelte-1gsxlqt"]/button')
        # size_selector.click()
        driver.find_element(By.ID, 'option-product-size-selection-2').click()

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
            driver.find_element(By.XPATH, './/button[@class="cta cta--block cta-noicon"]')
        except NoSuchElementException:
            print('Unable to locate "Add to cart" button')
            raise Exception('Unable to locate "Add to cart" button')

        add_to_cart_button = driver.find_element(By.XPATH, './/button[@class="cta cta--block cta-noicon"]')
        driver.execute_script("arguments[0].click();", add_to_cart_button)
        time.sleep(5)

        # Redirect driver to cart page
        driver.get('https://www.decathlon.es/es/checkout/cart')
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'mounting-component')))

        # Click buy
        accept_button = driver.find_element(By.XPATH, './/button[@class="vtmn-btn vtmn-btn_variant--conversion vtmn-btn_size--medium vtmn-btn_size--stretched"]')
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

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, './/h1[@class="svelte-19f8svx"]')))

        store_pick_up_menu = driver.find_element(By.XPATH, './/div[@class="drawer-button svelte-bjp9q1"]')
        store_pick_up_menu.click()

        euskadi_select = driver.find_element(By.ID, 'option-9fb29edb-a486-43b5-a8ca-2622175698fd-11')
        euskadi_select.click()

        driver.find_element(By.XPATH, './/label[@for="0070188601886"]').click()

        pay_button = driver.find_element(By.XPATH, './/button[@class="vtmn-btn vtmn-btn_variant--conversion vtmn-btn_size--medium vtmn-btn_size--stretched"]')
        pay_button.click()

        availability_selector = driver.find_element()

    except Exception as ex:
        print(ex.__str__())
        driver.close()
        driver.quit()
        if ex.__str__() == 'No availability':
            time.sleep(60)
        driver = webdriver.Chrome()
