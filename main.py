from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as ch
import datetime
import sqlite3
import time


# link for the product to be monitored
ruta = "https://www.mercadolibre.com.mx/motocicleta-chopper-italika-tc-300-negra/up/MLMU3007051693"


def save_data(date: str, price: int):   # save the data in a database file
    connection = sqlite3.connect('datos.db')
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS motocicleta(fecha TEXT,precio INTEGER)")
    cursor.execute("INSERT INTO motocicleta (fecha, precio) VALUES (?, ?)", (date, price))
    connection.commit()
    connection.close()


def open_webpages():    # open the webpage to get the price of the product in MercadoLibre
    moment = datetime.datetime.now()
    date = str(moment).split('.')[0]
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--windows-size=1280,720")
    #options.add_argument("--headless")
    driver = ch.Chrome(options=options, version_main=144)
    driver.get(ruta)
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(ec.presence_of_element_located((By.CLASS_NAME, "ui-pdp-price__second-line")))
        element = driver.find_element(By.CLASS_NAME, "ui-pdp-price__second-line")
        price = element.text.split('\n')[1].replace(',', '')
        print(f"This is current price ${int(price)} at {date}")
        save_data(date, int(price))
    except TimeoutError:
        print(f"El tiempo de espera se excedio")
    finally:
        driver.quit()


if __name__ == '__main__':
    open_webpages()
