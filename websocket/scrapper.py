from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from dotenv import load_dotenv
import os
import time
import pandas as pd

url = "https://stockbit.com/login"
load_dotenv()
email = os.getenv('STOCKBIT_EMAIL')
password = os.getenv('STOCKBIT_PASSWORD')

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

# get semua broker yang terdaftar di BEI
def get_all_broker_from_idx(driver: webdriver.Chrome):    
    idx_url = 'https://www.idx.co.id/id/anggota-bursa-dan-partisipan/profil-anggota-bursa'

    driver.get(idx_url)

    wait = WebDriverWait(driver, 15)
    btn_selectall = wait.until(
        EC.presence_of_element_located((By.NAME, 'perPageSelect'))
    )
    select = Select(btn_selectall)
    select.select_by_value("-1")

    table = driver.find_element(By.TAG_NAME, 'tbody')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    brokers = []

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'td')
        brokers.append([a.text for a in cols ])

    df = pd.DataFrame(brokers)
    df.to_csv('daftar_broker_idx.csv')    


def get_all_stocks_from_idx(driver: webdriver.Chrome):


if __name__ == '__main__':
    driver = _build_driver()
    get_all_broker_from_idx(driver)
    #_login(driver)
