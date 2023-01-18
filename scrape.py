import os
import time

import requests
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

import credentials_handler
import helper

# # Consts
link = "http://sco.polytech.unice.fr/1/etudiant"
verbose = True

# # Prepare
start_time = time.time()

credentials = credentials_handler.return_login_password()

options = Options()
options.headless = True

driver: WebDriver = selenium.webdriver.Edge(options=options)

# ## Start browser
if verbose:
    print("Browser started ...")

driver.get(link)

# ### Login page
driver.find_element(By.ID, 'username').send_keys(credentials[0])
driver.find_element(By.ID, 'password').send_keys(credentials[1])
driver.find_element(By.NAME, 'submit').click()

# ### Main page
ressources_pedagogiques_XPATH = helper.embrace_for_text_search('Dernières ressources pédagogiques')
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 's')
WebDriverWait(driver, 10).until(lambda driver_: driver_.find_element(By.XPATH, ressources_pedagogiques_XPATH))
driver.find_element(By.XPATH, ressources_pedagogiques_XPATH).click()

# ### Ressources pédagogiques page
WebDriverWait(driver, 10) \
    .until(lambda driver_:
           driver_.find_element(By.XPATH, helper.embrace_for_text_search('Toutes les matières')))

elements = driver.find_elements(By.CLASS_NAME, 'icon_piece_jointe')

# the first element is a checkbox
# get the parent containing the list of downloadable files
fifth_parent = elements[1] \
    .find_element(By.XPATH, '..') \
    .find_element(By.XPATH, '..') \
    .find_element(By.XPATH, '..') \
    .find_element(By.XPATH, '..') \
    .find_element(By.XPATH, '..')

if not os.path.exists("downloads"):
    os.makedirs("downloads")

if verbose:
    print("Downloading files ...")

for element in fifth_parent.find_elements(By.XPATH, './/a'):
    with open("downloads/" + element.text, 'wb') as f:
        f.write(requests.get(element.get_attribute('href')).content)

if verbose:
    print("files downloaded, closing browser ...")

driver.quit()

if verbose:
    print("Browser closed ...")
    end_time = time.time()
    print(f"Time elapsed: {end_time - start_time}")
