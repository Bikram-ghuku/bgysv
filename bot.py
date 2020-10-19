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
import sqlite3



x=0
banword = ["sex","fuck","banchod","madarchod","chutiya","Bitch"]
O_T = {}
var = {}
chaa = {}


datay = ""
botid = "NzQ1MTIyMjc0Nzk3MTU4NDU1.XztLMg.-_dVaROw5zBEmlIHyyQja2PPsvY"
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
async def on_message(message):
    await check_banwords(message)
    await client.process_commands(message)


async def check_banwords(lol):
    chan = lol.channel
    for x in banword:
        if x in lol.content:
            await lol.delete()
            x = await chan.send(f"{lol.author.mention} you are not allowed to say that word")
            await asyncio.sleep(2)
            await x.delete()




    

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
    client.run(botid)