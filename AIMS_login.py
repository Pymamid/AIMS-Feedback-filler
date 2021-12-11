from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from config import *


def get_element(driver, by, value):
    element = WebDriverWait(driver=driver, timeout=5).until(
        EC.presence_of_element_located((by, value))
    )
    return element


def get_all_elements(driver, by, value):
    elements = WebDriverWait(driver=driver, timeout=5).until(
        EC.presence_of_all_elements_located((by, value))
    )
    return elements


# Fun begins;)


def login(driver, email, password):
    site = "https://aims.iith.ac.in/aims/login/loginHome"
    driver.get(site)
    try:
        email_inp = get_element(driver=driver, by=By.ID, value="uid")
        password_inp = get_element(driver=driver, by=By.ID, value="pswrd")

        email_inp.send_keys(email)
        password_inp.send_keys(password)

        captcha_image = get_element(driver=driver, by=By.ID, value="appCaptchaLoginImg")
        captcha = captcha_image.get_attribute("src")[-5:]

        captcha_field = get_element(driver=driver, by=By.ID, value="captcha")
        captcha_field.send_keys(captcha)

        submit = get_element(driver=driver, by=By.CLASS_NAME, value="signIn")
        submit.click()
        time.sleep(10)
    except:
        driver.quit()


def homepage(driver):
    # site = "https://aims.iith.ac.in/aims/login/home"
    # driver.get(site)
    try:
        academic = get_element(driver, by=By.XPATH, value="//span[@title='Academic']")
        # print(academic.get_attribute("title"))
        actions.click(on_element=academic)

        view_courses = get_element(driver, by=By.XPATH, value="//span[@title='View My Courses']")
        actions.move_to_element(to_element=view_courses).click(on_element=view_courses)
        actions.perform()
    except:
        driver.quit()


def courses_page(driver):
    course_elements = get_all_elements(driver, by=By.CLASS_NAME, value=r'tab_body_bg')
    driver.quit()


if __name__ == '__main__':
    driver = webdriver.Chrome(Driver_Path)
    driver.set_window_size(1280, 1080)
    actions = ActionChains(driver)
    login(driver, email, password)
    homepage(driver)
    courses_page(driver)
