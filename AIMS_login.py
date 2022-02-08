import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
import random

PATH = ""
driver = webdriver.Chrome(PATH)

driver.get("https://aims.iith.ac.in/aims/")

Roll_Number = ""
Password = ""

uid = driver.find_element_by_id("uid")
uid.send_keys(Roll_Number)

pwd = driver.find_element_by_id("pswrd")
pwd.send_keys(Password)

captcha_img = driver.find_element_by_id("appCaptchaLoginImg")
tmp = captcha_img.get_attribute('src')
cap1 = tmp[-5:]
captcha1 = driver.find_element_by_id("captcha")
captcha1.send_keys(cap1)

button1 = driver.find_element_by_id("login")
button1.click()

actions = ActionChains(driver)

try:
    captcha2 = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "captcha"))
    )

    academic = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//span[@title='Academic']"))
    )
    actions.click(on_element=academic)
    
    view_courses = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//span[@title='View My Courses']"))
    )
    actions.move_to_element(to_element = view_courses).click(on_element = view_courses)
    actions.perform()

    feedback = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='iconLeft']"))
    )
    feedback_buttons = driver.find_elements_by_class_name('fb_status_change_icon')
    n = len(feedback_buttons)
    if n != 0:
        for i in range(n):
            feedback_wait = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='iconLeft']"))
            )

            feedback_button = driver.find_element_by_class_name('fb_status_change_icon')   
            feedback_link = feedback_button.get_attribute('href')
            # print(f'\n\n\n{feedback_link}\n\n\n')
            driver.get(feedback_link)

            feedback2 = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='iconLeft']"))
            )
            feedback2_buttons = driver.find_elements_by_class_name('fb_status_change_icon')
            m = len(feedback2_buttons)
            for j in range(m):
                feedback_wait = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//span[@class='iconLeft']"))
                )

                feedback2_button = driver.find_element_by_class_name('fb_status_change_icon')
                feedback2_link = feedback2_button.get_attribute('href')
                driver.get(feedback2_link)

                feedback_value = "'4.00'"
                feedback3 = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, f"//input[@value={feedback_value}]"))
                )

                Remarks = ["Great Course!", "Very Informative", "Enjoyable", "Wonderful", "Exciting"]
                driver.find_element_by_id('fbRemarks').send_keys(random.choice(Remarks))

                console_feedback_command = f'$("[value={feedback_value}]").click()'
                driver.execute_script(console_feedback_command)

                #submit_button_id = "'savefb'"
                #console_submit_command = f'$("[id={submit_button_id}]").click()'
                #driver.execute_script(console_feedback_command)

                print(time.time())
                try:
                    print("about to look for element")
                    def find(driver):
                        e = driver.find_element_by_id("savefb")
                        if (e.get_attribute("disabled")=='true'):
                            return False
                        return e
                    element = WebDriverWait(driver, 10).until(find)
                    print("still looking?")
                finally: 
                    print('yowp')
                print("ok, left the loop")
                print(time.time())
                actions.move_to_element(to_element = element).click(on_element = element)
                actions.perform()

    else: 
        driver.close()

finally:
    time.sleep(10)
