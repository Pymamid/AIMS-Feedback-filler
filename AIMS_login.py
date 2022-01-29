from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from config import *
import time
from tkinter import *
import pandas as pd
import numpy as np
import sys
import datetime

nextsem = ""
if 1 < datetime.datetime.now().month <= 4:
    year = datetime.datetime.now().strftime("%y")
    nextsem = f"AUG{year}-DEC{year}"

else:
    year = int(datetime.datetime.now().strftime("%y")) + 1
    nextsem = f"JAN{year}-APR{year}"

driver = webdriver.Chrome(service=Service(Driver_Path))
actions = ActionChains(driver)


def get_element(by, value):
    element = WebDriverWait(driver=driver, timeout=1000).until(
        EC.presence_of_element_located((by, value))
    )
    return element


def get_all_elements(by, value):
    elements = WebDriverWait(driver=driver, timeout=1000).until(
        EC.presence_of_all_elements_located((by, value))
    )
    return elements


# Fun begins;)

def login(email, password):
    try:
        site = "https://aims.iith.ac.in/aims/login/loginHome"
        driver.get(site)

        email_inp = get_element(by=By.ID, value="uid")
        password_inp = get_element(by=By.ID, value="pswrd")

        email_inp.send_keys(email)
        password_inp.send_keys(password)

        captcha = get_element(by=By.ID, value="appCaptchaLoginImg").get_attribute("src")[-5:]

        captcha_field = get_element(by=By.ID, value="captcha")
        captcha_field.send_keys(captcha)

        submit = get_element(by=By.NAME, value="signIn")
        submit.click()
        return 1
    except:
        driver.quit()
        return 0


def homepage(where):
    try:
        academic = get_element(by=By.XPATH, value="//span[@title='Academic']")
        actions.click(on_element=academic)
        elem = get_element(by=By.XPATH, value=where)
        actions.move_to_element(to_element=elem).click(on_element=elem)
        actions.perform()
    except:
        driver.quit()


def feedback_filling():
    login(email, password)
    homepage("//span@[title='View My Courses']")


def generate_tt():
    login(email, password)
    homepage("//span[@title='Course Registration']")
    elem = get_element(by=By.XPATH, value=f"//span[text()='{nextsem}']")
    parent = elem.parent
    regn_button = parent.find_element(By.XPATH, value=".//input[@value='Go For Registration']").click()
    course_rows = get_all_elements(by=By.CLASS_NAME, value='cNEdit')
    for course in course_rows:
        code = course.find_element(By.CLASS_NAME, value="cCd")
        print(code.get_attribute("title"))
        button = course.find_element(By.XPATH, ".//span[@title='Click For Time Table']")
        time.sleep(0.8)
        actions.click(on_element=button).perform()
        timetable = course.find_element(By.CLASS_NAME, value="timeTabDiv")
        rows = timetable.find_elements(By.TAG_NAME, value='tr')
        segment = [row.find_element(By.XPATH, value=".//td[@class='ttd1']").text for row in rows][0]
        times = set([row.find_element(By.XPATH, value=".//td[@class='ttd2']/span[2]").text for row in rows])
        print(segment, times)
        # break


def get_grade(char):
    if char == "A+" or char == "A":
        return 10
    elif char == "A-":
        return 9
    elif char == "B":
        return 8
    elif char == "B-":
        return 7
    elif char == "C":
        return 6
    elif char == "C-":
        return 5
    elif char == "D":
        return 4
    elif char == "FR" or char == "F" or char == "FS":
        return 0
    else:
        return None


def getcg():
    login(email, password)
    homepage("//span[@title='View My Courses']")
    course_elements = get_all_elements(by=By.CLASS_NAME, value=r'tab_body_bg')

    MAIN_DICT = {
        "courses": []
    }
    num_semesters = 0
    for elem in course_elements:
        class_name = elem.get_attribute("class")
        num_classes = len(class_name.split(" "))

        if num_classes > 3:
            num_semesters += 1

    for elem in course_elements:
        lis = elem.find_elements(By.XPATH, value=".//*")
        course_dict = {}
        if len(elem.get_attribute("class").split(" ")) > 3:
            num_semesters -= 1
            continue
        course_dict["Course Code"] = lis[0].text.strip()
        course_dict["Course Name"] = lis[1].text.strip()
        course_dict["Semester"] = num_semesters + 1
        course_dict["Credits"] = float(lis[2].text.strip())
        course_dict["Registration Type"] = lis[3].text.strip()
        course_dict["Course Type"] = lis[4].text.strip()
        course_dict["Segment"] = lis[5].text.strip()
        course_dict["Instructor Name"] = lis[6].text.strip()
        course_dict["Grade"] = lis[7].text.strip()
        course_dict["Feedback Status"] = lis[-1].get_attribute("title")

        MAIN_DICT["courses"].append(course_dict)

    data = pd.DataFrame(MAIN_DICT["courses"]).replace("", np.nan).dropna()
    data = data[(data['Course Type'] != "Additional") | (data["Course Type"] != "Audit")]
    total_credits = np.sum(data["Credits"])
    number_grades = np.array(data['Grade'].apply(get_grade))
    points = np.sum(data["Credits"] * number_grades)
    print(points / total_credits)
    print(data)
    driver.back()
    time.sleep(3)
    driver.quit()


def quit():
    try:
        driver.quit()
    except:
        print("Driver already closed")
    sys.exit(0)


try:
    root = Tk()
    root.eval("tk::PlaceWindow . center")
    root.title("AIMS Automation")
    root.geometry("300x400")
    btn1 = Button(root, text="Fill the Feedback", fg='red', command=feedback_filling).pack()
    btn2 = Button(root, text="Generate Timetable", fg='red', command=generate_tt).pack()
    btn3 = Button(root, text="Get CGPA", fg='red', command=getcg).pack()
    btn4 = Button(root, text="Exit the program", fg="red", command=quit).pack()
    root.mainloop()
except:
    print("Something wrong. Please rerun the program")
