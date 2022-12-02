from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# new lines for selenium 4
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Ensure that:
# Selenium is upgraded to v4.0.0
# pip3 install -U selenium
# Webdriver Manager for Python is installed
# pip3 install webdriver-manager

from sftp_get_files import grab_files

import time
import pathlib

import credentials
import platform
import datetime


# get timestamp for log
temp_timestamp = str(datetime.datetime.now())
print(2 * "\n")
print(temp_timestamp)


grab_files(
    [
        "01_0_Student_Match.csv",
        "02_0_Staff_Match.csv",
    ]
)


cur_dir = pathlib.Path.cwd()
print(cur_dir)
one_up = pathlib.Path(__file__).resolve().parents[1]

state_reports = pathlib.Path.cwd() / "incoming_files"

# choose correct chromedrier
print("\nchromedriver for:")
if platform.system() == "Darwin":
    print("mac")
    # browser = webdriver.Chrome(cur_dir / "chromedriver_86")
    chromedriver = cur_dir / "chromedriver"
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    # browser = webdriver.Chrome(options=options, executable_path=chromedriver)
else:
    print("pi")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(
        "/usr/lib/chromium-browser/chromedriver", options=options
    )


browser.implicitly_wait(100)
browser.get("https://slds.education.vermont.gov/edFusion/Web/Login.aspx")
time.sleep(1)


# log in
# username = browser.find_element_by_id("txtUserName")
username = browser.find_element("id", "txtUserName")
username.send_keys(credentials.my_username)
password = browser.find_element("id", "txtAcceptId")
password.send_keys(credentials.my_password)

signin_btn = browser.find_element("id", "login1")
signin_btn.click()

# hover and click on menu item below
action = ActionChains(browser)
time.sleep(3)
firstLevelMenu = browser.find_element("link text", "Integrate")
time.sleep(3)
action.move_to_element(firstLevelMenu).perform()
secondLevelMenu = browser.find_element("link text", "Submission Upload")
action.move_to_element(secondLevelMenu).perform()

secondLevelMenu.click()

time.sleep(1)


def slds_file_upload(cycles, file_list, dir_info):

    # web_pdb.set_trace()
    for index in range(cycles):

        # drop down box to choose submission type
        domain_dropdown = browser.find_element("id", "ctl00_MainContent_ddlFileType")
        domain_dropdown.click()
        time.sleep(2)

        browser.find_element(
            "css selector", ".rddlItem[title='Match Collections']"
        ).click()
        time.sleep(3)

        # upload set of blank student files

        file_upload_string = ""
        for file in file_list:
            file_path = str(dir_info / file)
            file_upload_string = file_upload_string + file_path + " \n "

        print(f"uploading set of match files {index}")
        # print(file_upload_string)
        # trim final new line character from string
        file_upload_string = file_upload_string[:-3]

        # send files to choose file button
        browser.find_element("id", "ctl00_MainContent_rdFileUploadfile0").send_keys(
            file_upload_string
        )
        time.sleep(3)

        # click upload button
        browser.find_element("id", "ctl00_MainContent_imgbtnUpload").click()
        time.sleep(5)

        js = "document.getElementById('ctl00_MainContent_rbScheduleNow_input').click()"
        browser.execute_script(js)
        print("scheduled")
        time.sleep(10)


# old_student_file_list = ["03_0_Student_Identity.csv","03_4_PS_Enroll.csv","03_5_PS_GradeProg.csv"]

student_file_list = [
    "01_0_Student_Match.csv",
    "02_0_Staff_Match.csv",
]

slds_file_upload(1, student_file_list, state_reports)

# slds_file_upload(1, student_file_list, one_up)

print("done")

browser.close()
