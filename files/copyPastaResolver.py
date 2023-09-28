import discord
from discord.ext import commands
from datetime import datetime,date,time,timedelta
import asyncio


userMap = {}
DIFF = 5
NUMBER = 5
MSGS = NUMBER/DIFF

async def delete_msg(member:discord.Member,number:int,channel:discord.channel):
    with channel.typing():
        async for m in channel.history():
            for _ in range(number):
                if m.author == member:
                    await m.delete()
    




class copyPastaResolver(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.usermap = {}
    @commands.Cog.listener()
    async def on_message(self,message):
        now = datetime.now()
        if message.author.bot and message.content.startswith("bb!"):
            return
        if message.author in self.usermap.keys():
            self.usermap[message.author.id].append(now)
        else:
            self.usermap[message.author.id] = [now]

        # if len(self.usermap[message.author.id])>=NUMBER:
        #     if self.usermap[message.author.id][-1]-self.usermap[message.author.id][0]<timedelta(seconds=DIFF):
        #         await delete_msg(message.author, NUMBER, message.channel)
        #         await message.channel.send(f"{message.author.mention} Please don't spam")
        #     else:
        #         self.usermap[message.author.id].pop(0)





async def setup(bot):
    await bot.add_cog(copyPastaResolver(bot))