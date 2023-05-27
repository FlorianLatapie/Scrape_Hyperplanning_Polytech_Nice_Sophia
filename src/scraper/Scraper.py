import time
import argparse
import configparser
from webdriver_handler import WebDriverFactory
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from Discipline import Discipline
import jsonpickle
import os


class Scraper:
    def __init__(self, average=None, link="http://sco.polytech.unice.fr/1/etudiant", verbose=False,
                 headless_driver=True):
        self.average = average
        self.link = link
        self.verbose = verbose
        self.headless_driver = headless_driver

        self.file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "discipline.json")


    async def start3(self, username, password):

        if self.verbose:
            start_time = time.time()

        if not os.path.exists(self.file_path):
            self.current_discipline = None
        else:
            with open(self.file_path, 'r') as file:
                serialized_object = file.read()
            self.current_discipline = jsonpickle.decode(serialized_object)

        self.new_discipline = None

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

        await self.login(username, password)
        await self.go_to_dernieres_notes()

        # self.close_browser()

        if self.verbose:
            end_time = time.time()
            print(f"Time elapsed: {end_time - start_time} s")

        return await self.perform_calculations()

    async def login(self, username, password):
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.NAME, 'submit').click()

    async def go_to_dernieres_notes(self):
        dernieres_notes = "//header[@title='Les 10 dernières notes']"
        WebDriverWait(self.driver, 10).until(lambda driver_: driver_.find_element(By.XPATH, dernieres_notes))
        self.driver.find_element(By.XPATH, dernieres_notes).click()

        WebDriverWait(self.driver, 10).until(lambda driver_: driver_.find_elements(By.CLASS_NAME, "ie-titre-gros"))

        page_source = self.driver.page_source
        # print(type(page_source))
        soup = BeautifulSoup(page_source, 'html.parser')

        span_tags = soup.find_all('span', attrs={'class': 'ie-titre-gros'})

        list_discipline = []

        if len(span_tags) % 2 != 0:
            exit("Not a pair number")

        # Don't need general average
        for i in range(0, len(span_tags) - 2, 2):
            list_discipline.append(Discipline(span_tags[i].text, float(span_tags[i + 1].text.replace(",", "."))))

        self.new_discipline = list_discipline

    async def perform_calculations(self):
        list_new_mark = []

        if (self.current_discipline == None):
            with open(self.file_path, 'w') as file:
                file.write(jsonpickle.encode(self.new_discipline))
        else:
            current_discipline = self.current_discipline
            new_discipline = self.new_discipline

            for i in range(len(new_discipline)):

                if not new_discipline[i] in current_discipline:
                    list_new_mark.append(new_discipline[i])

            with open(self.file_path, 'w') as file:
                file.write(jsonpickle.encode(self.new_discipline))
        return list_new_mark

    def close_browser(self):
        self.driver.quit()
        if self.verbose:
            print("Browser closed ...")
