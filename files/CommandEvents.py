from discord.ext import commands
import asyncio
import discord
import sqlite3




class CommandEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error, commands.errors.MissingPermissions):
            embene = discord.Embed(title="You dont have permission to do it",description=f"you dont have the required premisiion to do that. The following error was raised:{error}")
            embene.set_footer(text="Developed By Bikram Ghuku")
            await ctx.message.delete()
            x = await ctx.send(ctx.message.author.mention,embed=embene)
            await asyncio.sleep(2)
            await x.delete()
        elif isinstance(error, commands.errors.BotMissingPermissions):
            embene = discord.Embed(title="I dont have permission to do that",description=f"I dont have the required premission to do that. The following error was raised:{error}")
            embene.set_footer(text="Developed By Bikram Ghuku")
            await ctx.message.delete()
            x = await ctx.send(ctx.message.author.mention,embed=embene)
            await asyncio.sleep(2)
            await x.delete()
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            embene = discord.Embed(title="Please provide the required arguments",description=f"Please provide all the required parameters. The following error was raised:{error}")
            embene.set_footer(text="Developed By Bikram Ghuku")
            await ctx.message.delete()
            await ctx.send(ctx.message.author.mention,embed=embene)
            await asyncio.sleep(2)
        else:
            embene = discord.Embed(title="ERROR",description=f"There was an error. The following error was raised:{error}")
            embene.set_footer(text="Developed By Bikram Ghuku")
            await ctx.send(ctx.message.author.mention,embed=embene)
            await asyncio.sleep(2) 


    



async def setup(bot):
    await bot.add_cog(CommandEvents(bot))