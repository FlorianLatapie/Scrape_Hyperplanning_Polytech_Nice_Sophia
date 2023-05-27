import sys
import os

scraper_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../scraper")

sys.path.insert(1, r'' + scraper_folder)

from Scraper import Scraper


class MarkChecker:
    def __init__(self):
        self.scraper = Scraper()

    async def get_new_mark(self, username, password):
        return await self.scraper.start3(username, password)
