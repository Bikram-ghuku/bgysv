from discord.ext import commands
import discord
import requests
import sqlite3
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions
conn = sqlite3.connect('./db/data.sqlite')
cursor = conn.cursor()

class setupBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True,help="Setup the bot")
    @commands.has_guild_permissions(administrator=True)
    @has_permissions(administrator=True)
    async def setup(self,ctx):
        message = ctx.message
        server = ctx.message.guild
        question = ["Do you want to enable automod(yes/no)",
        "Do you want to enable level roles(yes/no)",
        "Do you want to enable welcome messages(yes/no)",
        "Do you want to enable leave messages(yes/no)",
        "Do you want a moderator role(yes/no)",
        "Enter the leave message use `{USERNAME}` for username",
        "Enter the welcome message use `{USERNAME}` for username",
        "Enter the level up message use `{USERNAME}` for username and `{LEVEL}` for level",
        ]
        response = []
        for i in question:
            await ctx.message.channel.send(i)
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel, timeout=60)
            if msg.content.lower() == "yes":
                response.append(True)
                await ctx.message.channel.send("Ok")
            elif msg.content.lower() == "no":
                response.append(False)
                await ctx.message.channel.send("Ok")
            else:
                response.append(msg.content)
                await ctx.message.channel.send("Ok")
        
        for i in range(1, 5):
            if response[i] == True:
                if i==1:
                    await ctx.message.channel.send("Enter Number of levels step by 10: ")
                    msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel, timeout=60)
                    roles = {}
                    for i in range(10*(int(msg.content.lower())), -10, -10):
                        role = await server.create_role(name="LeveL • {}".format(i), colour=discord.Colour(0x000000), hoist=True, mentionable=False)
                        await ctx.message.channel.send("Created Role: {}".format(role))
                        roles[i] = role.id
                    
                    cat = discord.utils.get(server.categories, name="SERVER-UPDATES")
                    if cat is None:
                        cat = await server.create_category("SERVER-UPDATES")
                        await ctx.message.channel.send("Created Category: {}".format(cat))
                    level = await server.create_text_channel("🆙┃level┃🆙", category=cat)
                    await ctx.message.channel.send("Created Channel: {}".format(level))

                if i==2:
                    print("2")
                    cat = discord.utils.get(server.categories, name="SERVER-UPDATES")
                    if cat is None:
                        cat = await server.create_category("SERVER-UPDATES")
                        await ctx.message.channel.send("Created Category: {}".format(cat))
                    welcome = await server.create_text_channel("【🎆】welcome", category=cat)
                    await ctx.message.channel.send("Created Channel: {}".format(welcome))

                if i==3:
                    cat = discord.utils.get(server.categories, name="SERVER-UPDATES")
                    if cat is None:
                        cat = await server.create_category("SERVER-UPDATES")
                    leave = await server.create_text_channel("【👋】goodbye", category=cat)
                
                if i==4:
                    mod_role = await server.create_role(name="Moderator", colour=discord.Colour(0x000000), hoist=True, mentionable=False)
                    await ctx.message.channel.send("Created Role: {}".format(mod_role))
                    for channel in server.channels:
                        await channel.set_permissions(mod_role, send_messages=True, read_messages=True, manage_messages=True, manage_roles=True, manage_nicknames=True, kick_members=True, manage_emojis=True, manage_webhooks=True, view_audit_log=True)
                    await mod_role.edit(position=server.me.top_role.position - 1)  

                log_channel = await server.create_text_chanel("Logs")
                await log_channel.set_permissions(server.default_role, send_messages=False, read_messages=False)
                await log_channel.set_permissions(mod_role, send_messages=False, read_messages=True)


        cursor.execute("INSERT INTO server_data VALUES{}"
        .format((server.id, "", response[0], log_channel.id, mod_role.id, [welcome.id, leave.id], response[6], response[5], roles, [response[7], level.id], None)))
        conn.commit()
        await ctx.message.channel.send("Setup Complete")

async def setup(bot):
    await bot.add_cog(setupBot(bot))