from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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

def get_all_elements_by_class(driver, value):
    elements = WebDriverWait(driver=driver, timeout=5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, value))
    )
    return elements

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
    site = "https://aims.iith.ac.in/aims/login/loginHome"
    driver.get(site)
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
        return True
    except:
        driver.quit()
        return False

def homepage(driver, email, password):
    # site = "https://aims.iith.ac.in/aims/login/home"
    # driver.get(site)
    if login(driver, email, password):
        academic = get_element_by_xpath(driver, "//span[@title='Academic']")
        # print(academic.get_attribute("title"))
        actions.click(on_element=academic)

        view_courses = get_element_by_xpath(driver, "//span[@title='View My Courses']")
        # print(view_courses.get_attribute("title"))
        actions.move_to_element(to_element=view_courses).double_click(on_element=view_courses)
        actions.perform()


if __name__ == '__main__':
    driver = webdriver.Chrome(Driver_Path)
    driver.set_window_size(1280, 1080)
    actions = ActionChains(driver)
    homepage(driver, email, password)