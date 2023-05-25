import os
import time
import argparse

import sys
sys.path.insert(1, r'..\helper')
# print(sys.path)

from my_credentials import My_credentials
import configparser
from webdriver_handler import WebDriverFactory

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

credentials = My_credentials()

# # Consts
link = "http://sco.polytech.unice.fr/1/etudiant"
verbose = True
headless_driver = True

# # Prepare
if verbose:
    start_time = time.time()

config = configparser.RawConfigParser()

# read the configuration file
config.read('../config/my_config.ini')

arg_parser = argparse.ArgumentParser(prog="scrape_files.py")
arg_parser.add_argument("--webdriver", "-wd", type=str, default=WebDriverFactory.DEFAULT, help="webdriver to use")
arg_parser.add_argument("--no-headless", action='store_false', default=True, help="display browser or not")
args = arg_parser.parse_args()

driver = WebDriverFactory.get(args.webdriver).get_driver(headless=args.no_headless)

# ## Start browser
if verbose:
    print("Browser started ...")

driver.get(link)

# ### Login page
driver.find_element(By.ID, 'username').send_keys(credentials.get_username())
driver.find_element(By.ID, 'password').send_keys(credentials.get_user_password())
driver.find_element(By.NAME, 'submit').click()

# ### Home page
dernieres_notes = "//header[@title='Les 10 dernières notes']"
WebDriverWait(driver, 10).until(lambda driver_: driver_.find_element(By.XPATH, dernieres_notes))
driver.find_element(By.XPATH, dernieres_notes).click()

# ### Dernières notes page
WebDriverWait(driver, 10).until(lambda driver_: driver_.find_elements(By.CLASS_NAME, "ie-titre-gros"))
ie_titre_gros_html_tags = driver.find_elements(By.CLASS_NAME, "ie-titre-gros")
nb_of_ie_titre_gros = len(ie_titre_gros_html_tags)

# ## Perform calculations
average = float(ie_titre_gros_html_tags[nb_of_ie_titre_gros - 1].get_attribute('innerHTML').replace(',', '.'))
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
        print("\033[92m" + "New average detected : " + str(average) + "\033[0m")
        # write the new average in average.txt
        average_file = open("average.txt", "w")
        average_file.write(str(average))
        average_file.close()
    else:
        print("\033[93m" + "No new average detected : " + str(average) + "\033[0m")

# ## Close browser

driver.quit()

if verbose:
    print("Browser closed ...")
    end_time = time.time()
    print(f"Time elapsed: {end_time - start_time} s")
