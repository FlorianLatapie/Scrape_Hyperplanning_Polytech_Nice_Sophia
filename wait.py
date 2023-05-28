import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.FirefoxOptions()
options.add_argument('-headless')

driver = webdriver.Firefox(options=options)
driver.maximize_window()

driver.get("http://sco.polytech.unice.fr/1/etudiant")

print(driver.page_source)


while 1:
    print("con")
    time.sleep(10)