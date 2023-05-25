import sys

sys.path.insert(1, r'..\scraper')
print(sys.path)

from scrape import Scraper


class MarkChecker:
    def __init__(self, mongodb):
        self.mongodb = mongodb
        self.scraper = Scraper()

    async def get_average_server(self, username, password):
        return self.scraper.start(username, password)
