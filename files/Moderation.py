from discord.ext import commands
import discord
import requests
import sqlite3
from discord.utils import get
conn = sqlite3.connect('./db/data.sqlite')
cursor = conn.cursor()


async def clear_command(channel,number:int=100):
    await channel.purge(limit=number)

class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True,help="Kicks a member with the provided reason.")
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self,ctx, member : discord.Member,*,reason:str=None):
        message = ctx.message
        server = ctx.message.guild
        await message.delete()
        try:
            print(member)
            kick_message_target = discord.Embed(title="Kick message",description=f"you have been kicked in {str(server)} as {reason}",color=discord.Color.blue())
            kick_message = discord.Embed(title="Successfuly kicked" ,description=f"The following user has been kicked: {member} ✅",color=discord.Color.blue())
            kick_message_target.set_footer(text="Developed By Bikram Ghuku")
            kick_message.set_footer(text="Developed By Bikram Ghuku")
            await member.send(embed=kick_message_target)
            await ctx.message.channel.send(embed=kick_message)
            await member.kick(reason=reason)
        except Exception:
            await member.kick(reason=reason)
    

    @commands.command(pass_context=True,help="Bans a member with a given reason")
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self,ctx, member : discord.Member,*,reason:str=None):
        message = ctx.message
        server = ctx.message.guild
        await message.delete()
        if message.author.server_permissions.ban_members:
            try:
                print(member)
                kick_message_target = discord.Embed(title="Ban message",description=f"you have been banned in {str(server)} as {reason}",color=discord.Color.blue())
                kick_message = discord.Embed(title="Successfuly banned" ,description=f"The following user has been Banned: {member} ✅",color=discord.Color.blue())
                kick_message_target.set_footer(text="Developed By Bikram Ghuku")
                kick_message.set_footer(text="Developed By Bikram Ghuku")
                await member.send(embed=kick_message_target)
                await ctx.message.channel.send(embed=kick_message)
                await member.ban(reason=reason)
            except Exception:
                await member.ban(reason=reason)

    @commands.command(pass_context=True,help="Mutes a member and stops him from typing anything else")
    @commands.has_guild_permissions(manage_roles=True)
    async def mute(self,ctx, member:discord.Member,*,reason:str=None):
        await ctx.message.delete()
        server = ctx.message.guild
        role = discord.utils.get(server.roles,name="Muted")
        embene = discord.Embed(title="Muted",description=f"You have in muted in {str(server)} for {str(reason)} you won't be automatically unmuted. You need to contact a moderator for unmute", color=discord.Color.blue())
        embene2 = discord.Embed(title="Success",description=f"✅ Successfully muted {str(member)}",color=discord.Color.blue())
        embene2.set_footer(text="Developed By Bikram Ghuku")
        embene.set_footer(text="Developed By Bikram Ghuku")
        await member.send(embed=embene)
        await ctx.message.channel.send(embed=embene2)
        await member.add_roles(role)

    @commands.command(pass_context=True,help="Unmutes a member who is muted")
    @commands.has_guild_permissions(manage_roles=True)
    async def unmute(self,ctx,member :discord.Member):
        await ctx.message.delete()
        for role_mention in member.roles:
            if role_mention.name=="Muted":
                server = ctx.message.guild
                role = discord.utils.get(server.roles,name="Muted")
                embene = discord.Embed(title="Unmute",description=f"You have in unmuted in {str(server)} ", color=discord.Color.blue())
                embene2 = discord.Embed(title="Success",description=f"✅ Successfully unmuted {str(member)}",color=discord.Color.blue())
                embene.set_footer(text="Developed By Bikram Ghuku")
                embene2.set_footer(text="Developed By Bikram Ghuku")
                await ctx.message.channel.send(embed=embene2)
                await member.send(embed=embene)
                await member.remove_roles(role)
            else:
                pass
    
    @commands.command(pass_context=True,help="Warns a member with a reason(requires manage server permission)")
    @commands.has_permissions(manage_guild=True)
    async def warn(self,ctx,member:discord.Member,*,reason:str=None):
        await ctx.message.delete()
        try:
            await member.send(f"You were warned in {ctx.guild} for \n `{reason}`")
            embene2 = discord.Embed(title="Success",description=f"✅ Successfully warned {str(member)}",color=discord.Color.blue())
            embene2.set_footer(text="Developed By Bikram Ghuku")
            await ctx.send(embed=embene2)
        except Exception as e:
            embene2 = discord.Embed(title="Error",description=f"❌ Couldn't warn {str(member)} error: {e}",color=discord.Color.red())
            embene2.set_footer(text="Developed By Bikram Ghuku")
            await ctx.send(embed=embene2)



    @commands.command(pass_context=True,help="Strike a member with a reason(Requires admin permissions)")
    @commands.has_permissions(administrator=True)
    async def strike(self,ctx,member:discord.Member,*,reason:str=None):
        await ctx.message.delete()
        try:
            cursor.execute(f"SELECT count FROM strike_logs WHERE server_id=\"{ctx.guild.id}\" AND user_id=\"{member.id}\"")
            x = cursor.fetchone()
            await ctx.send(x)
            if x is None:
                cursor.execute(f"INSERT INTO strike_logs(count,user_id,server_id) VALUES(\"1\",\"{member.id}\",\"{ctx.guild.id}\")")
                conn.commit()
            else:
                strikes = int(x[0])+1
                cursor.execute(f"UPDATE strike_logs SET count=\"{strikes}\" WHERE user_id=\"{member.id}\" AND server_id=\"{ctx.guild.id}\"")
                conn.commit()
            await member.send(f"You were striked in {ctx.guild} for \n `{reason}` you currently have `{int(x[0])+1}`")
            embene2 = discord.Embed(title="Success",description=f"✅ Successfully striked {str(member)}",color=discord.Color.blue())
            embene2.set_footer(text="Developed By Bikram Ghuku")
            await ctx.send(embed=embene2)
        except Exception as e:
            embene2 = discord.Embed(title="Error",description=f"❌ Couldn't strike {str(member)} error: {e}",color=discord.Color.red())
            embene2.set_footer(text="Developed By Bikram Ghuku")
            await ctx.send(embed=embene2)

    @commands.command(pass_context=True,help="Deletes messages sent by a user in a fixed amount of time")
    @commands.has_permissions(manage_messages=True)
    async def purge(self,ctx,number:int=100):
        with ctx.channel.typing():
            await clear_command(ctx.channel,number)
            await ctx.send(f"Successfuly deleted {number} of messages.")


    
        






def setup(bot):
    bot.add_cog(Moderation(bot))