import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from Discipline import Discipline
import jsonpickle
import os

helper_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../helper")
sys.path.insert(1, r'' + helper_folder)

from Logger import logger


class Scraper:
    def __init__(self, link: str = "http://sco.polytech.unice.fr/1/etudiant"):
        """
        Initializes a new instance of the Scraper class.

        Parameters:
        - link (str): The URL of the web page to scrape.
        """
        self.link = link

        self.file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "discipline.json")

    async def start(self, username, password):
        """
        Starts the scraping process.

        Parameters:
        - username (str): The username for logging in.
        - password (str): The password for logging in.

        Returns:
        - list: A list of new marks (Discipline objects).
        """
        start_time = time.time()

        if not os.path.exists(self.file_path):
            self.current_discipline = None
        else:
            with open(self.file_path, 'r') as file:
                serialized_object = file.read()
            self.current_discipline = jsonpickle.decode(serialized_object)

        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')

        helper_folder = os.path.dirname(os.path.abspath(__file__)) + "/../../logs/geckodriver.log"

        self.driver = webdriver.Firefox(options=options, service_log_path=helper_folder)
        self.driver.set_page_load_timeout(60)
        self.driver.maximize_window()

        self.new_discipline = None

        logger.info("Browser started ...")

        self.driver.get(self.link)

        await self.login(username, password)
        await self.go_to_dernieres_notes()

        self.close_browser()

        end_time = time.time()
        logger.info(f"Time elapsed: {end_time - start_time} s")

        return await self.perform_calculations()

    async def login(self, username, password):
        """
        Logs in to the web page using the provided username and password.

        Parameters:
        - username (str): The username for logging in.
        - password (str): The password for logging in.
        """
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.NAME, 'submit').click()

    async def go_to_dernieres_notes(self):
        """
        Navigates to the page containing the latest marks.
        """
        last_notes = "//header[@title='Les 10 dernières notes']"
        WebDriverWait(self.driver, 10).until(lambda driver_: driver_.find_element(By.XPATH, last_notes))
        self.driver.find_element(By.XPATH, last_notes).click()

        WebDriverWait(self.driver, 10).until(lambda driver_: driver_.find_elements(By.CLASS_NAME, "ie-titre-gros"))

        page_source = self.driver.page_source
        # print(type(page_source))
        soup = BeautifulSoup(page_source, 'html.parser')

        span_tags = soup.find_all('span', attrs={'class': 'ie-titre-gros'})

        list_discipline = []

        if len(span_tags) % 2 != 0:
            logger.error("A discipline do not have marks")
            exit("Not a pair number")

        # Don't need general average
        for i in range(0, len(span_tags) - 2, 2):
            list_discipline.append(Discipline(span_tags[i].text, float(span_tags[i + 1].text.replace(",", "."))))

        self.new_discipline = list_discipline

    async def perform_calculations(self):
        """
        Performs calculations to determine new marks.

        Returns:
        - list: A list of new marks (Discipline objects).
        """
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
        """
        Closes the web browser.
        """
        self.driver.quit()
        logger.info("Browser closed ...")
