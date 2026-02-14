from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as ch
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sqlite3
import time
import os
import sys
import numpy as np

# link for the product to be monitored
ruta = "https://www.mercadolibre.com.mx/motocicleta-chopper-italika-tc-300-negra/up/MLMU3007051693"
ruta2 = "https://www.amazon.com.mx/dp/B07G7CHRQY/?coliid=I3MMYSO5HGSFQM&colid=3AZBLI2SFHTWM&ref_=list_c_wl_lv_ov_lig_dp_it&th=1&psc=1"


def save_data(date: str, price: int):   # save the data in a database file
    data = os.path.join(os.path.dirname(__file__), 'datos.db')  # it is required to define absolute path
    connection = sqlite3.connect(data)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS motocicleta(fecha TEXT,precio INTEGER)")
    cursor.execute("INSERT INTO motocicleta (fecha, precio) VALUES (?, ?)", (date, price))
    connection.commit()
    connection.close()


def graph_data():
    data = os.path.join(os.path.dirname(__file__), 'datos.db')
    conn = sqlite3.connect(data)

    table = 'motocicleta'
    query = f"SELECT * FROM {table}"
    df = pd.read_sql_query(query, conn)
    conn.close()

    x_ax = []
    y_ax = []
    for f in range(len(df['fecha'])):
        if f == 0:
            x_ax.append(df['fecha'][f].split(' ')[0])
            y_ax.append(df['precio'][f])
        else:
            prev = df['fecha'][f-1].split(' ')[0]
            now = df['fecha'][f].split(' ')[0]
            if prev != now:
                x_ax.append(now)
                y_ax.append(df['precio'][f])

    plt.plot(x_ax, y_ax, label='Price data')
    plt.xlabel('date')
    plt.xticks(rotation=90)
    plt.ylabel('price')
    plt.title(f'Chart of price')
    plt.tight_layout()
    plt.show()


class BasePage:

    def __new__(cls, driver, liga):
        if 'mercadolibre.com' in liga:
            return super(BasePage, MercadoLibrePage).__new__(MercadoLibrePage)
        elif 'amazon.com' in liga:
            return super(BasePage, AmazonPage).__new__(AmazonPage)
        return super(BasePage, cls).__new__(cls)

    def __init__(self, driver, liga):
        self.__driver = driver
        self.__wait = WebDriverWait(driver, 3)
        self.link = liga
        self.open_page(liga)

    def open_page(self, link):
        self.__driver.get(link)

    def find_element(self, method, name):
        try:
            return self.__wait.until(EC.presence_of_element_located((method, name)))
        except TimeoutError:
            print(f"Element {name} is not found")

    def close_page(self):
        self.__driver.close()

    def close_browser(self):
        self.__driver.quit()


class MercadoLibrePage(BasePage):
    __locator = By.CLASS_NAME
    __name = "ui-pdp-price__second-line"

    def get_price(self):
        super().open_page(self.link)
        text_price = super().find_element(self.__locator, self.__name)
        return text_price.text.split('\n')[1].replace(',', '')


class AmazonPage(BasePage):
    __locator = By.CLASS_NAME
    __name = "a-price-whole"

    def get_price(self):
        super().open_page(self.link)
        super().find_element(By.CLASS_NAME, "a-button-text").click()
        text_price = super().find_element(self.__locator, self.__name)
        return text_price.text.replace(',', '')


if __name__ == '__main__':
    #open_webpages()
    #graph_data()
    options = webdriver.ChromeOptions()
    driver = ch.Chrome(options=options, version_main=144)
    driver.maximize_window()

    pag1 = BasePage(driver, ruta2)
    price = pag1.get_price()
    pag1.close_browser()

    moment = datetime.datetime.now()
    date = str(moment).split('.')[0]
    print(f"Para la fecha {date} el precio obtenido es {price}")
    #save_data(date, int(price))

