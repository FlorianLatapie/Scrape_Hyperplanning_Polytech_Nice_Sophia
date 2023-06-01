import asyncio
from discord_webhook import DiscordWebhook, DiscordEmbed

import sys
import os

helper_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../helper")
scraper_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../scraper")

sys.path.insert(1, r'' + helper_folder)
sys.path.insert(1, r'' + scraper_folder)

from MyCredentials import MyCredentials
from MarkChecker import MarkChecker
from Discipline import Discipline

credentials = MyCredentials()
markChecker = MarkChecker()

async def check():
    index = 0
    while True:
        try:
            print("\nCheck ...")
            list_new_mark = await markChecker.get_new_mark(credentials.get_username(), credentials.get_user_password())
            print(list_new_mark)
            for new_mark in list_new_mark:
                await send_notification(new_mark.name)
            print("\nEnd check: ", len(list_new_mark), "\n")
        except Exception as error:
            # handle the exception
            print("An exception occurred:", error)  # An exception occurred: division by zero
        index += 1
        await asyncio.sleep(60)


async def send_notification(discipline):
    webhook = DiscordWebhook(
        url=credentials.get_webhook_url())
    embed = DiscordEmbed(title="New mark", description="A new mark in " + discipline, color='0xff6464')
    webhook.add_embed(embed)
    webhook.execute()


async def my_async_function():
    await check()


asyncio.run(my_async_function())
