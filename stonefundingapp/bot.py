from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from requests_html import HTMLSession, AsyncHTMLSession
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv
import config

'''
python supreme.py --name="North Face"
'''

base_url = 'https://shop2.gzanders.com'
uvc = [] #universal product code
product_urls = []

def loginZanders(driver):
    driver.get(base_url + '/customer/account/login/')

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID,'email')))
    username = driver.find_element_by_id("email")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID,'pass')))
    password = driver.find_element_by_id("pass")

    username.send_keys(config.email)
    password.send_keys(config.password)

    driver.find_element_by_id("send2").submit()

    if driver.current_url == 'https://shop2.gzanders.com/customer/account/':
        return True
    else:
        return False

def getUVC():
    #Importing data from csv
    with open('C://Users//Maisum Abbas//stonefunding//stonefundingapp//Book1.csv','rt') as f:
        data = csv.reader(f)
        next(data, None) 
        for row in data:
            uvc.append(row[0])
    return uvc

def getProductLinks(driver):
    for item in uvc:
        code = driver.find_element_by_id("search")
        code.send_keys(item)
        time.sleep(3)
        if driver.find_elements_by_xpath("//div[@class='amsearch-products -waste']"):
            code.clear()
        elif driver.find_elements_by_class_name("product-item-link"):
            stockAvailability(driver) 

def stockAvailability(driver):
    driver.find_element_by_class_name("product-item-link").click()
    if driver.find_elements_by_xpath("//span[text()='Back Order']"):
        time.sleep(0)
    elif driver.find_elements_by_xpath("//span[text()='Add to Cart']"):
        driver.find_element_by_id('product-addtocart-button').click()

def checkout(driver):
    driver.find_element_by_xpath("//a[@class='action showcart']").click()
    driver.find_element_by_xpath("//a[@class='chckout-btn']").click()
    #time.sleep(5) #need 5 seconds to check radio button
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'ko_unique_1')))
    driver.find_element_by_name('ko_unique_1').click()
    
    if WebDriverWait(driver, 10).until(EC.alert_is_present()):
        driver.switch_to.alert.accept()
    
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'ko_unique_2')))
    # driver.find_element_by_name('ko_unique_2').click()
    driver.find_element_by_xpath("//button[@class='button action continue primary']").click()
    #time.sleep(15) #need 5 seconds to check radio button
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'zpay')))
    element = driver.find_element_by_id('zpay') #.click()
    driver.execute_script("arguments[0].click();", element)
    time.sleep(5)

def main():

    # Setup our headless browser. 
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    if loginZanders(driver) == True:
        uvc = getUVC()
        while True: 
            getProductLinks(driver)
            checkout(driver)
            driver.find_element_by_xpath("//button[@class='action primary checkout']").click()
            time.sleep(60)
            print('We are finished.')
    else:
        print("Wrong Credentials")

# define main
if __name__ == '__main__':
    main()