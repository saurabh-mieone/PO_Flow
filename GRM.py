import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep


uname = "hsr_user_1"
pswd = "Stockone@123"
PO_num = "11-None-None20211016_00057"


def initiate():
    opt = Options()
    opt.headless = False
    driver = webdriver.Firefox()
    driver.get("http://app.stockone.com/#/login")
    return driver


def login(driver, username, password):
    inp_fields = driver.find_elements_by_tag_name("input")
    submit = driver.find_element_by_tag_name("button")
    driver.find_element_by_xpath("//*[@placeholder='Username']").send_keys(username)
    driver.find_element_by_xpath("//*[@placeholder='Password']").send_keys(password, Keys.ENTER)
    return driver


def Recv_PO_Open(driver, PO_num):
    # waiting for inbound to be available after login
    temp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="fa fa-dropbox"]'))
    )

    # clicking on inbound
    inbound = driver.find_element_by_xpath('//*[@class="fa fa-dropbox"]/..')
    inbound.click()

    recv_PO = driver.find_element_by_xpath("//*[@href='#/inbound/ReceivePO']")
    recv_PO.click()

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

    try:
        driver.find_element_by_xpath("//input[@id='file-upload']").send_keys(os.getcwd() + "/samplefile.txt")
    except:
        pass

    sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Generate GRN']"))
    ).click()

    sleep(2)

    driver.find_element_by_xpath("//button[text()='Continue']").click()

    sleep(2)

    driver.find_element_by_xpath("//button[@class='close']").click()

def QC(driver,PO_num):
    driver.find_element_by_xpath("//a[@ui-sref='app.inbound.QualityCheck']").click()

    WebDriverWait(driver, 1000).until(
        EC.presence_of_element_located((By.XPATH, "//label[text()='Search:']/input"))
    ).send_keys(PO_num, Keys.ENTER)

    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, f"//*[text()='{PO_num}']"))
    ).click()


driver = initiate()
driver = login(driver, uname, pswd)
driver = Recv_PO_Open(driver, PO_num)
