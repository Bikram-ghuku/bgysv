import discord
from discord.ext import commands
import asyncio

banword = ["sex","fuck","banchod","madarchod","chutiya","Bitch"]

async def check_banwords(lol):
    chan = lol.channel
    for x in banword:
        if x in lol.content:
            await lol.delete()
            x = await chan.send(f"{lol.author.mention} you are not allowed to say that word")
            await asyncio.sleep(2)
            await x.delete()
            z = True
        else:
            z = False
    return z



class autoMod(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message):
        await check_banwords(message)




def setup(bot):
    bot.add_cog(autoMod(bot))