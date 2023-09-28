from discord.ext import commands
import discord
import requests
import sqlite3
from discord.utils import get

class giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(giveaway(bot))