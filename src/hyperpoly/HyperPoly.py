import asyncio
import sys
import os
from discord_webhook import DiscordWebhook, DiscordEmbed

helper_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../helper")
sys.path.insert(1, r'' + helper_folder)

scraper_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../scraper")
sys.path.insert(1, r'' + scraper_folder)

from MyCredentials import MyCredentials
from Discipline import Discipline
from Scraper import Scraper
from Logger import logger

credentials = MyCredentials()
scraper = Scraper()

async def check():
    """
    Performs a check for new marks using the Scraper class and sends a notification if new marks are found.
    """
    try:
        logger.info("Check ...")
        list_new_mark = await scraper.start(credentials.get_username(), credentials.get_user_password())
        logger.info(list_new_mark)
        for new_mark in list_new_mark:
            await send_notification(new_mark.name)
        logger.info("End check: " + str(len(list_new_mark)))
    except Exception as error:
        logger.error("An exception occurred:", error)


async def send_notification(discipline):
    """
    Sends a notification to a Discord server with the name of the discipline where a new mark is found.

    Parameters:
    - discipline (str): The name of the discipline.
    """
    webhook = DiscordWebhook(url=credentials.get_webhook_url())
    embed = DiscordEmbed(title="New mark", description="A new mark in " + discipline, color='0xff6464')
    webhook.add_embed(embed)
    webhook.execute()
    logger.info("Send notification: A new mark in " + discipline)


async def my_async_function():
    """
    Main async function that periodically calls the check function and sleeps for 60 seconds.
    """
    logger.info("Init")
    while True:
        await check()
        await asyncio.sleep(60)


asyncio.run(my_async_function())
