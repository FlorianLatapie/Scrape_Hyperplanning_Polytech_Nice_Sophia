# https://discord.com/api/oauth2/authorize?client_id=1110501745345433610&permissions=8&scope=bot
import discord

import sys

sys.path.insert(1, r'..\helper')
print(sys.path)

from my_credentials import My_credentials
# from scrape import Scraper
from mongoDB import MongoDB
from discord.ext import commands

from mark_checker import MarkChecker

credentials = My_credentials()

TOKEN = credentials.get_bot_token()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

db = MongoDB()
db.connect()

markChecker = MarkChecker(db)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_guild_join(guild):
    channel = discord.utils.get(guild.text_channels)

    embed = discord.Embed(title="Thank you for adding me",
                          description="I'm here to notify you if a new note is added on Hyperplanning", color=0x800080)
    embed.add_field(name="To configure me, make the command", value="!configure ", inline=False)

    embed.set_footer(
        text="Only the owner of the discord can choose if he wants to be notified on his server (and who has the authorization to manage HYPER-BOT)")
    await channel.send(embed=embed)


@bot.event
async def on_member_join(member):
    print("GO GO GO: ", member)


@bot.command()
async def configure(ctx):
    embed = discord.Embed(title="Configuration", color=0x800080)
    embed.add_field(name="1 - Give authorization to manage HYPER-BOT", value="!giveManage <@username> ", inline=False)
    embed.add_field(name="2 - Manage HYPER-BOT", value="!manage (if you own the server)", inline=True)
    embed.add_field(name="3 - HYPER-BOT in your DM", value="!manageDM (If you want HYPER-BOT slide in your DM)",
                    inline=True)
    await ctx.send(embed=embed)

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        response = await bot.wait_for('message', check=check, timeout=60)  # Attend la réponse pendant 60 secondes
        await ctx.send(f"Vous avez répondu : {response.content}")
    except:
        await ctx.send("Temps écoulé, veuillez réessayer plus tard.")


@bot.command()
async def manage(ctx):
    # Warning
    embed = discord.Embed(title="Manage",
                          description="Warning: Before starting the management, you should know that you will have to give identifiers of your hyperplanning.",
                          color=0xff6464)
    disclaimer_message = await ctx.send(embed=embed)

    options = ['🔴', '🟢']

    for option in options:
        await disclaimer_message.add_reaction(option)

    def check(reaction, user):
        return user == ctx.author and reaction.message == disclaimer_message

    try:
        reaction, user = await bot.wait_for('reaction_add', check=check, timeout=30)

        if reaction.emoji == '🔴':
            embed = discord.Embed(title="End of the management", description="Maybe next time", color=0x800080)
            await ctx.send(embed=embed)
            await disclaimer_message.delete()
            return

    except:
        embed = discord.Embed(title="Time out", description="You have 30 seconds to answer", color=0xff6464)
        await ctx.send(embed=embed)

    await disclaimer_message.delete()

    # Choose the channel
    guild = ctx.guild
    channels = guild.text_channels

    bot_member = ctx.guild.get_member(bot.user.id)

    channels_permitted = []
    my_list_channel_permitted = []
    for channel in channels:
        permissions = channel.permissions_for(bot_member)
        print(channel.name, channel.id)

        if permissions.send_messages:
            my_list_channel_permitted.append(channel.name)
            channels_permitted.append(channel)

    embed = discord.Embed(title="Manage",
                          description="Choose the channel in which you want the notifications to appear",
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

    embed = discord.Embed(title="Selected channel : " + channel_name_choose.content,
                          color=0x800080)
    await ctx.send(embed=embed)

    embed = discord.Embed(title="Last step", description="Last step in your DM !: ",
                          color=0x800080)
    await ctx.send(embed=embed)

    def check_message_author(message):
        return message.author == ctx.author

    embed = discord.Embed(title="Username", description="What is your hyperplanning username ?", color=0x800080)
    ask_username = await ctx.author.send(embed=embed)

    try:
        username = await bot.wait_for('message', check=check_message_author, timeout=30)
    except:
        embed = discord.Embed(title="Time out", description="You have 30 seconds to answer", color=0xff6464)
        await ctx.send(embed=embed)
        return

    await ask_username.delete()
    print(username.content)

    embed = discord.Embed(title="Password", description="What is your hyperplanning password ?", color=0x800080)
    ask_password = await ctx.author.send(embed=embed)

    try:
        password = await bot.wait_for('message', check=check_message_author, timeout=30)
    except:
        embed = discord.Embed(title="Time out", description="You have 30 seconds to answer", color=0xff6464)
        await ctx.send(embed=embed)
        return

    await ask_password.delete()
    print(password.content)

    print("Save in DB", ctx.guild.id, channel_choose.id, username.content, password.content)

    average = await markChecker.get_average_server(username.content, password.content)

    print("Save in DB average", average)

    db.insert_server(ctx.guild.id, channel_choose.id, username.content, password.content, average)


async def send_notification(guild_id, channel_id):
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(channel_id)

    embed = discord.Embed(title="New mark", description="@everyone", color=0xff6464)
    await channel.send(embed=embed)


bot.run(TOKEN)
