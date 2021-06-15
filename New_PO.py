from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from time import sleep
import os
import requests
from datetime import datetime

uname = "krmngla_user_1"
pswd = "Stockone@123"


def sku_code():
    with open("./SKU master") as file:
        SKU = list()
        for i in file:
            SKU = i.split("$")
        return SKU


sku_codes = sku_code()
sup_ID = ["SUP1"]


def login(driver, username, password):
    inp_fields = driver.find_elements_by_tag_name("input")
    submit = driver.find_element_by_tag_name("button")
    driver.find_element_by_xpath("//*[@placeholder='Username']").send_keys(username)
    driver.find_element_by_xpath("//*[@placeholder='Password']").send_keys(password, Keys.ENTER)
    return driver


def initiate():
    opt = Options()
    opt.headless = True
    driver = webdriver.Firefox(options=opt)
    driver.get("http://app.stockone.com/#/login")
    return driver


def newPO_Open(driver):
    # waiting for inbound to be available after login
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="fa fa-dropbox"]'))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@href='#/inbound/RaisePO']"))
    ).click()

    # waiting for newPO button to be available
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="btn btn-success pull-right ml10"]'))
    ).click()

    return driver


def fill_details(driver):
    # waiting to SUP_ID get loaded
    temp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@placeholder='Search Supplier']"))
    )

    # entering SUP_ID
    driver.find_element_by_xpath("//*[@placeholder='Search Supplier']").send_keys(random.choice(sup_ID))
    driver.implicitly_wait(5)
    driver.find_element_by_xpath("//*[@class='ng-scope ng-binding']").click()

    # waiting for ship_address
    temp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@class = 'select2-arrow']"))
    )

    # entering ship_address
    driver.find_element_by_xpath("//*[@class='select2-arrow']/..").click()
    driver.find_element_by_xpath(
        "//*[@class='select2-results-dept-0 select2-result select2-result-selectable ng-binding ng-scope select2-highlighted']").click()

    # entering SKU_CODE
    driver.find_element_by_xpath("//*[@placeholder='Search WMS Code/Description']").send_keys(random.choice(sku_codes))
    temp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@class='ng-scope ng-binding']"))
    )
    driver.find_element_by_xpath("//*[@class='ng-scope ng-binding']").click()

    # entering quantity
    driver.find_element_by_name("order_quantity").clear()
    driver.find_element_by_name("order_quantity").send_keys(random.choice(range(3, 11)))

    # entering price
    driver.find_element_by_name("price").clear()
    driver.find_element_by_name("price").send_keys(random.choice(range(30, 100)))

    # entering taxes
    driver.find_element_by_name("sgst_tax").clear()
    driver.find_element_by_name("sgst_tax").send_keys(random.choice(range(5, 18)))
    driver.find_element_by_name("cgst_tax").clear()
    driver.find_element_by_name("cgst_tax").send_keys(random.choice(range(5, 18)))

    # entering signature TnC
    driver.find_element_by_tag_name("textarea").send_keys("Dummy TnC for testing")

    # confirming PO"
    driver.find_element_by_xpath("//*[text()='Confirm PO']").click()
    # click continue button
    temp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[text()='Continue']"))
    )
    sleep(2)
    driver.execute_script("arguments[0].click();", temp)

    # extracting PO_number
    sleep(2)
    PO_number = driver.find_element_by_xpath("//b[text()='PO Number :']/..").text.split(":")[1]

    sleep(2)

    driver.find_element_by_xpath("//button[@class='close']").click()

    return driver, PO_number


def Recv_PO_Open(driver, PO_num):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="fa fa-dropbox"]'))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="fa fa-dropbox"]'))
    ).click()

    recv_PO = driver.find_element_by_xpath("//*[@href='#/inbound/ReceivePO']")
    recv_PO.click()

    sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//label[text()='Search:']/input"))
    ).send_keys(PO_num, Keys.ENTER)

    sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//*[text()='{PO_num}']"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@name='grn_date']"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//option[@class='ng-binding']"))
    ).click()

    max_quantity = int(driver.find_element_by_name("po_quantity").get_attribute("title"))

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='quantity']"))
    ).send_keys(random.choice(range(1, max_quantity + 1)))

    sleep(2)

    try:
        driver.find_element_by_xpath("//input[@id='file-upload']").send_keys(os.getcwd() + "/samplefile.txt")
    except:
        pass

    sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Generate GRN']"))
    ).click()

    sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Continue']"))
    ).click()

    sleep(2)

    driver.find_element_by_xpath("//button[@class='close']").click()

    return driver


def QC(driver, PO_num):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@ui-sref='app.inbound.QualityCheck']"))
    ).click()

    sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//label[text()='Search:']/input"))
    ).send_keys(PO_num, Keys.ENTER)

    sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//*[text()='{PO_num}']"))
    ).click()

    sleep(1)

    max_value = int(driver.find_element_by_name("quantity").get_attribute("value"))
    driver.find_element_by_name("accepted_quantity").send_keys(random.choice(range(1, max_value + 1)))

    sleep(1)

    driver.find_element_by_xpath("//button[text()='Confirm']").click()

    sleep(4)

    driver.find_element_by_xpath("//button[@class='close']").click()

    return driver


def PAC(driver, PO_num):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Put away Confirmation']/.."))
    ).click()

    sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//label[text()='Search:']/input"))
    ).send_keys(PO_num, Keys.ENTER)

    sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//td[text()='{PO_num}']"))
    ).click()

    sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//button[text()='Confirm']"))
    ).click()

    return driver


try:
    driver = initiate()
    driver = login(driver, uname, pswd)
    driver = newPO_Open(driver)
    driver, PO_number = fill_details(driver)

    sleep(2)  # for marginal time
    driver = Recv_PO_Open(driver, PO_number)  # GRN

    try:
        sleep(2)
        driver = QC(driver, PO_number)
    except:
        pass
    sleep(2)  # for marginal time
    driver = PAC(driver, PO_number)

    mssg = f"Created new PO with \n PO Number :: {PO_number} \n successfully at {datetime.now()}"
    requests.get(f"http://127.0.0.1:8989/failure_mail/{mssg}")

    driver.quit()

except Exception as mssg:
    mssg = f"Failure occured \n reason of failure is {mssg}"
    requests.get(f"http://127.0.0.1:8989/failure_mail/{mssg}")

# print(mssg)