from abc import ABC, abstractmethod
import selenium



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
    from selenium.webdriver.edge.webdriver import WebDriver

    def get_driver(self, headless: bool = True) -> WebDriver:
        from selenium.webdriver.edge.options import Options

        options = Options()
        options.headless = headless

        return selenium.webdriver.Edge(options=options)

# chrome
class ChromeWebDriverHandler(IWebDriverHandler):
    from selenium.webdriver.chrome.webdriver import WebDriver

    def get_driver(self, headless: bool = True) -> WebDriver:
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.headless = headless

        return selenium.webdriver.Chrome(options=options)
