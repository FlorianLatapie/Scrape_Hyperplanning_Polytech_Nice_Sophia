# https://discord.com/api/oauth2/authorize?client_id=1110501745345433610&permissions=8&scope=bot
import time

import discord
from discord.ext import commands
from discord.ext import tasks


import sys
import os

helper_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\helper")
scraper_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\scraper")

print(os.path)

sys.path.insert(1, r'' + helper_folder)
sys.path.insert(1, r'' + scraper_folder)

from MyCredentials import MyCredentials
from MarkChecker import MarkChecker
from Discipline import Discipline

credentials = MyCredentials()
TOKEN = credentials.get_bot_token()

global GUILD_ID, CHANNEL_ID

GUILD_ID = None
CHANNEL_ID = None

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

markChecker = MarkChecker()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    # check()
    weird.start()
    # asyncio.create_task(check())


@bot.event
async def on_guild_join(guild):
    channel = discord.utils.get(guild.text_channels)

    embed = discord.Embed(title="Thank you for adding me",
                          description="I'm here to notify you if a new note is added on Hyperplanning", color=0x800080)
    embed.add_field(name="To configure me, make the command", value="!help ", inline=False)

    await channel.send(embed=embed)


@bot.command()
async def help2(ctx):
    embed = discord.Embed(title="Help", color=0x800080)
    embed.add_field(name="1 - Manage HYPER-BOT", value="!configure", inline=True)
    await ctx.send(embed=embed)


@bot.command()
async def configure(ctx):
    global GUILD_ID, CHANNEL_ID
    # Choose the channel
    guild = ctx.guild
    channels = guild.text_channels

    bot_member = ctx.guild.get_member(bot.user.id)

    channels_permitted = []
    my_list_channel_permitted = []
    for channel in channels:
        permissions = channel.permissions_for(bot_member)
        # print(channel.name, channel.id)

        if permissions.send_messages:
            my_list_channel_permitted.append(channel.name)
            channels_permitted.append(channel)

    embed = discord.Embed(title="Configuration",
                          description="1/2 - Choose the channel in which you want the notifications to appear",
                          color=0x800080)

    list_string = "\n".join(
        my_list_channel_permitted)
    embed.add_field(name="Channel list available ", value=list_string, inline=False)

    channel_message = await ctx.send(embed=embed)

    def check_message(message):
        return message.author == ctx.author and message.channel == ctx.channel

    while (True):
        try:
            channel_name_choose = await bot.wait_for('message', check=check_message, timeout=30)
            if (channel_name_choose.content in my_list_channel_permitted):
                break
            else:
                await channel_message.delete()
                await channel_name_choose.delete()
                embed = discord.Embed(title="Wrong channel", description="You must enter a valid channel name",
                                      color=0xff6464)
                await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title="Time out", description="You have 30 seconds to answer", color=0xff6464)
            await ctx.send(embed=embed)
            return

    await channel_name_choose.delete()
    await channel_message.delete()

    for channel in channels_permitted:
        if (channel.name == channel_name_choose.content):
            channel_choose = channel

    GUILD_ID = ctx.guild.id
    CHANNEL_ID = channel_choose.id

    embed = discord.Embed(title="Notification", description="Notifications will be here", color=0xff6464)
    await channel_choose.send(embed=embed)

@tasks.loop(seconds=40)
async def weird():
    try:
        print("\nCheck ...")
        if (GUILD_ID != None and GUILD_ID != None):
            list_new_mark = await markChecker.get_new_mark(credentials.get_username(), credentials.get_user_password())
            print(list_new_mark)
            for new_mark in list_new_mark:
                await send_notification(new_mark.name)
            print("\nEnd check: ", len(list_new_mark), "\n")
        else:
            print("\nEnd check\n")
    except:
        print("weird BUG !")


async def send_notification(discipline):
    if (GUILD_ID != None and CHANNEL_ID != None):
        guild = bot.get_guild(GUILD_ID)
        channel = guild.get_channel(CHANNEL_ID)

        embed = discord.Embed(title="New mark", description="A new mark in " + discipline, color=0xff6464)
        await channel.send(embed=embed)



async def check():
    while True:
        print("\nCheck ...")
        if (GUILD_ID != None and GUILD_ID != None):
            list_new_mark = await markChecker.get_new_mark(credentials.get_username(), credentials.get_user_password())
            print(list_new_mark)
            for new_mark in list_new_mark:
                await send_notification(new_mark.name)
            print("\nEnd check: ", len(list_new_mark), "\n")
        else:
            print("\nEnd check\n")
        time.sleep(30)


bot.run(TOKEN)