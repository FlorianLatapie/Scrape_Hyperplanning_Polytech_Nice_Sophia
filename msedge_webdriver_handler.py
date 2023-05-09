import selenium
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.webdriver import WebDriver


def get_driver(headless: bool = True) -> WebDriver:
    options = Options()
    options.headless = headless

    return selenium.webdriver.Edge(options=options)
