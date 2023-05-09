from abc import ABC, abstractmethod
import selenium
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.webdriver import WebDriver


class IWebDriverHandler(ABC):
    @abstractmethod
    def get_driver(self, headless: bool = True) -> WebDriver:
        pass


class WebDriverFactory:
    MSEdge = "msedge"

    @staticmethod
    def get(browser: str) -> IWebDriverHandler:
        if browser == "msedge":
            return MSEdgeWebDriverHandler()
        else:
            raise Exception(f"Unknown browser: {browser}")


class MSEdgeWebDriverHandler(IWebDriverHandler):
    def get_driver(self, headless: bool = True) -> WebDriver:
        options = Options()
        options.headless = headless

        return selenium.webdriver.Edge(options=options)
