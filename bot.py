import discord
from discord.ext import commands
import requests
import json as jason
from discord import ext
from discord.utils import get
import time
import random
import asyncio
import datetime
import sqlite3, os



x=0

O_T = {}
var = {}
chaa = {}


datay = ""
botid = os.environ['BOTID']
client = commands.Bot(command_prefix="b!",description="A bot that creates and updates yotube stats and shows them in your server")


conn = sqlite3.connect('db/data.sqlite')
cursor = conn.cursor()






@client.command(pass_context=True,help="Views the bot's latency")
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")
    print(f'Ping {int(ping)}ms')









    

@client.event
async def on_ready():
    cursor.execute('''CREATE TABLE IF NOT EXISTS ytdata(
    server_id TEXT,
    channel_id TEXT,
    views_id TEXT,
    videoes_id TEXT,
    subs_id TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS strike_logs(
    server_id TEXT,
    user_id TEXT,
    count TEXT
    )''')
    print("Bot online")
    await client.change_presence(activity=discord.Game(name="b!help."))



if __name__ == "__main__":
    client.load_extension('files.Moderation')
    client.load_extension('files.CommandEvents')
    client.load_extension('files.YoutubeStats')
    client.load_extension('files.autoMod')
    client.run(botid)
