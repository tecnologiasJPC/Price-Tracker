import time
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as ch
import datetime
import sqlite3


# link for the product to be monitored
ruta = "https://www.mercadolibre.com.mx/motocicleta-chopper-italika-tc-300-negra/up/MLMU3007051693"


def guardar_datos(date: str, price: int):   # save the data in a database file
    conexion = sqlite3.connect('C:/Users/john_/Documents/TrackingPrices/datos.db')
    cursor = conexion.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS motocicleta(fecha TEXT,precio INTEGER)")
    cursor.execute("INSERT INTO motocicleta (fecha, precio) VALUES (?, ?)", (date, price))
    conexion.commit()
    conexion.close()


def open_webpages():    # open the webpage to get the price of the product in MercadoLibre
    tiempo = datetime.datetime.now()
    fecha = str(tiempo).split('.')[0]
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--windows-size=1280,720")
    driver = ch.Chrome(options=options)
    driver.get(ruta)
    time.sleep(2)
    elemento = driver.find_element(By.CLASS_NAME, "ui-pdp-price__second-line")
    precio = elemento.text.split('\n')[1].replace(',', '')
    print(f"This is current price {int(precio)} at {fecha}")
    guardar_datos(fecha, int(precio))
    driver.quit()


if __name__ == '__main__':
    open_webpages()
