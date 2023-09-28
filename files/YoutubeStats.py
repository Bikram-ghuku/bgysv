from discord.ext import commands
import discord
import requests
import sqlite3
from discord.utils import get


conn = sqlite3.connect('./db/data.sqlite')
cursor = conn.cursor()

key = "AIzaSyA2Jr4pUoJ7Ry3F9RE2H76knGtF7OQDZRA"


def get_data(channelid):
    url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&key="+key+"&id="+channelid
    datax = requests.get(url)
    datay = datax.json()
    subs = datay["items"][0]["statistics"]
    return subs



def store_data(guild_id,yt_id,subs_id,views_id,vides_id):
    cursor.execute(f"SELECT * FROM ytdata WHERE server_id ={guild_id}")
    x = cursor.fetchone()
    if x is None:
        try:
            cursor.execute(f"INSERT INTO ytdata(server_id,channel_id,views_id,videoes_id,subs_id) VALUES(\"{guild_id}\",\"{yt_id}\",\"{views_id}\",\"{vides_id}\",\"{subs_id}\")")
            conn.commit()
        except Exception as e:
            print(e)
    else:
        cursor.execute(f"UPDATE ytdata SET channel_id=\"{yt_id}\",views_id=\"{views_id}\",subs_id=\"{subs_id}\",videoes_id=\"{vides_id}\"")
        conn.commit()
        


def check_id(yt_id):
    url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&key="+key+"&id="+yt_id
    datax = requests.get(url)
    datay = datax.json()
    subs = datay["pageInfo"]["resultsPerPage"]
    return subs




class YoutubeStats(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True,help="Create a yt stats of the channel with the help of channel url")
    async def create(self,ctx,url):
        guild = ctx.message.guild
        server = str(ctx.message.guild.id)
        urlus = url.split('/')
        try:
            if(len(urlus[4])==24):
                if(check_id(str(urlus[4]))>=1):
                    await ctx.message.channel.send("Creating YouTube stats")
                    x = get_data(urlus[4])
                    subs = await guild.create_voice_channel("Subscribers : "+x['subscriberCount'])
                    videoes = await guild.create_voice_channel("Video : "+x['videoCount'])
                    views = await guild.create_voice_channel("Views : "+x['viewCount'])
                    s =[subs, videoes, views]
                    for i in s:
                        await i.set_permissions(guild.default_role, connect=False, speak=False)
                    store_data(str(server),str(urlus[4]),str(subs.id),str(views.id),str(videoes.id))
                else:
                    await ctx.message.channel.send("No channel with that Id")
            else:
                await ctx.message.channel.send("The link is not the correct link")
        except Exception as e:
            print(e)
            await ctx.message.channel.send("an unknown error occured please contact us by joining our discord server")



    @commands.command(pass_context=True,hidden=True)
    async def update(self,ctx):
        if ctx.author.id == 531138466990260225:
            succ_msg = discord.Embed(title="Server Update ",description="The following is the result of data")
            cursor.execute("SELECT * FROM ytdata")
            var = cursor.fetchall()
            for key in var:
                cursor.execute(f"SELECT subs_id FROM ytdata WHERE server_id={str(key[0])}")
                subs_id = cursor.fetchone()
                subs_id_int = subs_id[0]
                cursor.execute(f"select views_id from ytdata where server_id={key[0]}")
                views_id = cursor.fetchone()
                views_id_int = views_id[0]
                cursor.execute(f"select videoes_id from ytdata where server_id={key[0]}")
                vids_id = cursor.fetchone()
                vids_id_int = vids_id[0]
                cursor.execute(f"SELECT channel_id from ytdata where server_id={key[0]}")
                yt_id = cursor.fetchone()
                yt_id_int = yt_id[0]
                zaaa = get_data(str(yt_id_int))
                subscriber_present = zaaa["subscriberCount"]
                views_present = zaaa["viewCount"]
                video_present = zaaa["videoCount"]
                try:
                    subs_channel = self.bot.get_channel(int(subs_id_int))
                    vids_channel = self.bot.get_channel(int(vids_id_int))
                    views_channel = self.bot.get_channel(int(views_id_int))
                    await subs_channel.edit(name="Subscriber : "+subscriber_present)
                    await vids_channel.edit(name="videos : "+video_present)
                    await views_channel.edit(name="Views : "+views_present)
                    print("Update command received")
                    succ_msg.add_field(name="Server Updated", value=f"Server updated {key} ✅")
                except Exception as e:
                    succ_msg.add_field(name="Error Updating", value=f"Error updating the server {key} ❌. The following error has occured : {e} ",inline=False)
                    succ_msg.set_footer(text="Developed By Bikram Ghuku")

                await ctx.message.channel.send(embed=succ_msg)
        else:
            war_msg = discord.Embed(title="Warning message",description="You cannot use the command ❌",color=discord.Color.red())
            war_msg.set_footer(text="Developed By Bikram Ghuku")
            await ctx.message.channel.send(embed=war_msg)


async def setup(bot):
    await bot.add_cog(YoutubeStats(bot))