import discord
from discord.ext import commands
from datetime import datetime,date,time,timedelta
import asyncio


topleveldomain = [".com",".in",".tk","https://","http://",".gg",".uk",".us",".ly"]

async def delete_msg(member:discord.Member,number:int,channel:discord.channel):
    with channel.typing():
        async for m in channel.history():
            if m.author == member:
                await m.delete()
    




class linksResolver(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_message(self,message):
        for x in topleveldomain:
            if x in message.content.lower() and not message.content.lower.startswith("bb!create"):
                await message.delete()
                await message.author.send("Don't share links here its not")






async def setup(bot):
    await bot.add_cog(linksResolver(bot))