import discord
from discord.ext import commands
from datetime import datetime,date,time,timedelta
import asyncio


userMap = {}
DIFF = 5
MSGS = 5

async def delete_msg(member:discord.Member,number:int,channel:discord.channel):
    with channel.typing():
        async for m in channel.history():
            if m.author == member:
                await m.delete()
    




class copyPastaResolver(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_message(self,message):
        now = datetime.now()
        if message.author.bot:
            return
        elif message.author.id in userMap:
            userData = userMap[message.author.id]
            lastTime = userData['lastTime']
            diff = lastTime - now
            diff_sec = diff.total_seconds()
            if int(diff_sec)<=int(DIFF):
                spam_count = userData['strikes']
                spam_count_a = spam_count+1
                userData['strikes'] = spam_count_a
                if int(userData['strikes'])>=MSGS:
                    userData['strikes'] = 0
                    x = await message.channel.send(f'Don\'t spam {message.author.mention}. Spamming is not allowed')
                    await delete_msg(message.author,int(userData['strikes']),message.channel)
                    await asyncio.sleep(5)
                    await x.delete()
            else:
                del userMap[message.author.id]
        else:
            userMap[message.author.id] = {'lastTime':datetime.now(),'strikes':1}





def setup(bot):
    bot.add_cog(copyPastaResolver(bot))