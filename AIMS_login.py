from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import *


def get_element_by_id(driver, value):
    element = WebDriverWait(driver=driver, timeout=5).until(
        EC.presence_of_element_located((By.ID, value))
    )
    return element

def get_element_by_class(driver, value):
    element = WebDriverWait(driver=driver, timeout=5).until(
        EC.presence_of_element_located((By.CLASS_NAME, value))
    )
    return element

def get_element_by_tag(driver, value):
    element = WebDriverWait(driver=driver, timeout=5).until(
        EC.presence_of_element_located((By.TAG_NAME, value))
    )
    return element

def get_element_by_xpath(driver, value):
    element = WebDriverWait(driver=driver, timeout=5).until(
        EC.presence_of_element_located((By.XPATH, value))
    )
    return element

def get_element_by_name(driver, value):
    element = WebDriverWait(driver=driver, timeout=5).until(
        EC.presence_of_element_located((By.NAME, value))
    )
    return element


def login(driver, email, password):
    try:
        email_inp = get_element_by_id(driver=driver, value="uid")
        password_inp = get_element_by_id(driver=driver, value="pswrd")

        email_inp.send_keys(email)
        password_inp.send_keys(password)

        captcha_image = get_element_by_id(driver=driver, value="appCaptchaLoginImg")
        captcha = captcha_image.get_attribute("src")[-5:]

        captcha_field = get_element_by_id(driver=driver, value="captcha")
        captcha_field.send_keys(captcha)

        submit = get_element_by_name(driver=driver, value="signIn")
        submit.click()
        time.sleep(10)

    except:
        driver.quit()

if __name__ == '__main__':
    driver = webdriver.Chrome(Driver_Path)

    site = "https://aims.iith.ac.in/aims/login/loginHome"
    driver.set_window_size(1280, 1080)
    driver.get(site)
    login(driver, email, password)