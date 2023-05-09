from abc import ABC, abstractmethod
import selenium
from selenium.webdriver.edge.webdriver import WebDriver


class IWebDriverHandler(ABC):
    @abstractmethod
    def get_driver(self, headless: bool = True) -> WebDriver:
        pass


class WebDriverFactory:
    MS_EDGE = "msedge"
    CHROME = "chrome"
    DEFAULT = MS_EDGE

    @staticmethod
    def get(browser: str) -> IWebDriverHandler:
        if browser == WebDriverFactory.MS_EDGE:
            return MSEdgeWebDriverHandler()
        elif browser == WebDriverFactory.CHROME:
            return ChromeWebDriverHandler()
        else:
            raise Exception(f"Unknown browser: {browser}")


class MSEdgeWebDriverHandler(IWebDriverHandler):
    def get_driver(self, headless: bool = True) -> WebDriver:
        from selenium.webdriver.edge.options import Options

        options = Options()
        options.headless = headless

        return selenium.webdriver.Edge(options=options)

# chrome
class ChromeWebDriverHandler(IWebDriverHandler):
    def get_driver(self, headless: bool = True) -> WebDriver:
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.headless = headless

        return selenium.webdriver.Chrome(options=options)
