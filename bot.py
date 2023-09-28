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
import os


x=0

O_T = {}
var = {}
chaa = {}


datay = ""
botid = "MTA0MTIwNzI1ODY2ODg3OTg5Mg.GQVVfd.iINBKr5DqgZqcw_U9wenlJks0GqF192wZmqE0Q"
client = commands.Bot(command_prefix="bb!",description="A bot that creates and updates yotube stats and shows them in your server", intents=discord.Intents.all())


conn = sqlite3.connect('db/data.sqlite')
cursor = conn.cursor()


@client.command(pass_context=True,help="Views the bot's latency")
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")
    print(f'Ping {int(ping)}ms')

@client.command(pass_context=True,help="Views the bot's latency")
async def invite(ctx):
    embed = discord.Embed(title="Invite me",url="https://discord.com/api/oauth2/authorize?client_id=745122274797158455&permissions=8&scope=bot")
    await ctx.send(embed=embed)
    

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
    count INT
    )''')
    print("Bot online")
    await client.change_presence(activity=discord.Game(name=f"bb!help on {str(len(client.guilds))} servers"))



async def main():
    for file in os.listdir("./files"):
        if file.endswith(".py"):
            name = file[:-3]
            await client.load_extension(f"files.{name}")
            print(f"Loaded {name}")
    await client.start(botid)

if __name__ == "__main__":
    asyncio.run(main())