import os
import time
import argparse
import configparser
from webdriver_handler import WebDriverFactory
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class Scraper:
    def __init__(self, average=None, link="http://sco.polytech.unice.fr/1/etudiant", verbose=False,
                 headless_driver=True):
        self.average = average
        self.link = link
        self.verbose = verbose
        self.headless_driver = headless_driver

    def start(self, username, password):
        if self.verbose:
            start_time = time.time()

        config = configparser.RawConfigParser()
        config.read('../config/my_config.ini')

        arg_parser = argparse.ArgumentParser(prog="scrape_files.py")
        arg_parser.add_argument("--webdriver", "-wd", type=str, default=WebDriverFactory.DEFAULT,
                                help="webdriver to use")
        arg_parser.add_argument("--no-headless", action='store_false', default=True, help="display browser or not")
        args = arg_parser.parse_args()

        self.driver = WebDriverFactory.get(args.webdriver).get_driver(headless=self.headless_driver)

        if self.verbose:
            print("Browser started ...")

        self.driver.get(self.link)

        self.login(username, password)
        self.go_to_dernieres_notes()
        average = self.perform_calculations()
        self.close_browser()

        if self.verbose:
            end_time = time.time()
            print(f"Time elapsed: {end_time - start_time} s")

        return average

    def login(self, username, password):
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.NAME, 'submit').click()

    def go_to_dernieres_notes(self):
        dernieres_notes = "//header[@title='Les 10 dernières notes']"
        WebDriverWait(self.driver, 10).until(lambda driver_: driver_.find_element(By.XPATH, dernieres_notes))
        self.driver.find_element(By.XPATH, dernieres_notes).click()

    def perform_calculations(self):
        WebDriverWait(self.driver, 10).until(lambda driver_: driver_.find_elements(By.CLASS_NAME, "ie-titre-gros"))
        ie_titre_gros_html_tags = self.driver.find_elements(By.CLASS_NAME, "ie-titre-gros")
        nb_of_ie_titre_gros = len(ie_titre_gros_html_tags)

        return float(ie_titre_gros_html_tags[nb_of_ie_titre_gros - 1].get_attribute('innerHTML').replace(',', '.'))

    def close_browser(self):
        self.driver.quit()
        if self.verbose:
            print("Browser closed ...")