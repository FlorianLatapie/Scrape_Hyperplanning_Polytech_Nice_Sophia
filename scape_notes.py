import os
import time

import requests
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

import credentials_handler
import helper

# # Consts
link = "http://sco.polytech.unice.fr/1/etudiant"
verbose = True

# # Prepare
if verbose:
    start_time = time.time()

credentials = credentials_handler.return_login_password()

options = Options()
options.headless = False

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
dernieres_notes = "//header[@title='Les 10 dernières notes']"
WebDriverWait(driver, 10).until(lambda driver_: driver_.find_element(By.XPATH, dernieres_notes))

driver.find_element(By.XPATH, dernieres_notes).click()

WebDriverWait(driver, 10).until(lambda driver_: driver_.find_elements(By.CLASS_NAME, "ie-titre-gros"))

ie_titre_gros_html_tags = driver.find_elements(By.CLASS_NAME, "ie-titre-gros")
nb_of_ie_titre_gros = len(ie_titre_gros_html_tags)

average = float(ie_titre_gros_html_tags[nb_of_ie_titre_gros-1].get_attribute('innerHTML').replace(',', '.'))
print("found average :", average)


if not os.path.exists("average.txt"):
    average_file = open("average.txt", "w")
    average_file.write(str(average))
    average_file.close()

with open("average.txt", "r") as average_file:
    average_file_content = average_file.read()
    print("average_file_content :", average_file_content)
    # compare average with average_file_content
    if average != float(average_file_content):
        print("New average detected")
        # write the new average in average.txt
        average_file = open("average.txt", "w")
        average_file.write(str(average))
        average_file.close()
    else:
        print("No new average detected")