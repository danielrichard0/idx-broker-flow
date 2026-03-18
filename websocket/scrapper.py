from selenium import webdriver
from selenium.webdriver.chrome import webdriver as w_chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from dotenv import load_dotenv
import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, date

url = "https://stockbit.com/login"
load_dotenv()
email = os.getenv('STOCKBIT_EMAIL')
password = os.getenv('STOCKBIT_PASSWORD')
broker_url = 'https://www.idx.co.id/id/anggota-bursa-dan-partisipan/profil-anggota-bursa'
stock_url = 'https://www.idx.co.id/id/perusahaan-tercatat/profil-perusahaan-tercatat/'
_get_master = False


def _build_driver()-> webdriver.Chrome :
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    return driver 

def _login(driver: webdriver.Chrome):
    wait = WebDriverWait(driver, 15)
    print('email : ', email)
    driver.get(url)

    email_field = wait.until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    email_field.clear()
    email_field.send_keys(email)

    password_field = driver.find_element(By.ID, 'password')
    password_field.clear()
    password_field.send_keys(password)

    login_button = driver.find_element(By.ID, 'email-login-button')
    login_button.click()

    time.sleep(3)  


# data saham atau broker bisa diambil lewat sini
def get_data_from_idx(driver: webdriver.Chrome, url: str, filename: str):
    driver.get(url)

    wait = WebDriverWait(driver, 15)
    btn_selectall = wait.until(
        EC.presence_of_element_located((By.NAME, 'perPageSelect'))
    )
    select = Select(btn_selectall)
    select.select_by_value("-1")

    table = driver.find_element(By.TAG_NAME, 'tbody')
    html = table.get_attribute('outerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    datas = [[cell.text.strip() for cell in row.find_all('td')] for row in soup.find_all("tr")]

    df = pd.DataFrame(datas)
    df.to_csv(filename)       


if __name__ == '__main__':
    driver = _build_driver()

    if _get_master :
        get_data_from_idx(driver, stock_url, 'daftar_saham_bei_' + str(date.strftime(date.today(),'%d_%m_%Y')) + '.csv')
        get_data_from_idx(driver, broker_url, 'daftar_broker_terdaftar_' + str(date.strftime(date.today(),'%d_%m_%Y')) + '.csv')


    #_login(driver)
