from discord.ext import commands, tasks
from dotenv import load_dotenv
import discord
import os
import logging 
import api_calls
import time
import datetime

#bot.invoke allows to invoke a command from another command

#Token
load_dotenv()
bot_key= os.getenv("BOT_TOKEN")

#Logger
handler = logging.FileHandler(filename="disscord.log",
                               encoding="utf-8",
                               mode="w"
                               )

#Events
#Listens and reponds to something
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot( command_prefix='!',
                    intents=intents
                    )

global timeAlert

@bot.command()
async def items(ctx, item):
    try:
        #testing this
        emoji = ctx.bot.get_emoji(1357688180089819177)
        call = await api_calls.request_item(item)
        embed = discord.Embed(
            title=f"Your requested item '{item}'",
            description=(
                f"Is currently {call['price']} platinum {emoji} on warframe market. \n"
                "\n"
                f"From seller: {call['seller']}. \n"
                "\n"
                f"Has {call['quantity']} in stock."
            ),
            color=discord.Color.green()
        )
        embed.set_footer(text="WarframeMarketBot - type !help to get more info about commands!")
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"An error occurred in your query, please try again later. Details: {e}")

@bot.command()
async def baro(ctx):
    try:
        call = await api_calls.void_trader()
        embed = discord.Embed(
            title="Baro Ki'Teer",
            description=(f"```¡Baro Baro Ki'Teer has arrived to the solar system! \n"
                "\n"                        
                "His stancy will last from the current dates: \n"
                "\n"
                f"Started ==> {call['Start']} \n"
                "\n"
                f"Ending ==> {call['Ends']} \n"
                "\n" 
                f"Currently can be found at {call['Location']}.```"
            ),
             color=discord.Color.green()
        )
        #embed.set_image(url="https://static.wikia.nocookie.net/warframe/images/a/a7/TennoCon2020BaroCropped.png/revision/latest?cb=20200712232455")
        embed.set_footer(text="WarframeMarketBot - type !help to get more info about commands!")
        await ctx.send(embed=embed)
    except:
        await ctx.send("An error ocurred in your query, please try again later")

@bot.command()
async def drops(ctx,*, item, member: discord.Member = None):
    try:
        if member is None:
            member = ctx.author
        call = await api_calls.get_drop(item)
        embed = discord.Embed(
            title=f"Your requested item: {item}",
            color=discord.Color.green()
        )
        embed.set_author(name=member.display_name, icon_url=member.avatar.url)
        relics = '\n'.join(call["Relics"])
        embed.add_field(name="Can be found in the following relics:", value=f"```{relics}```")
        embed.set_footer(text="WarframeMarketBot - type !help to get more info about commands!")
        await ctx.send(embed=embed)
    except Exception as e: 
        await ctx.send(f"An error occurred in your query, please try again later. Details: {e}")

@bot.command()
async def info(ctx,*, item, member: discord.Member = None):
    try:
        if member is None:
            member = ctx.author
        call = await api_calls.item_info(item)
        embed = discord.Embed(
            title=f"Your requested item: {item}",
            color=discord.Color.green()
        )
        embed.set_author(name=member.display_name, icon_url=member.avatar.url)
        embed.set_thumbnail(url=call["Image"])
        embed.add_field(name="", value= "Your item stats are the following:", inline=True)
        embed.add_field(name= "", value= call["Stats"], inline=False)	
        embed.set_footer(text="WarframeMarketBot - type !help to get more info about commands!")
        await ctx.send(embed=embed)
    except: 
        await ctx.send("An error ocurred in your query, please try again later")


# In construction
"""@bot.command()
async def set_alert(ctx, time):

    if not time:
        ctx.send("Please provide a date value in the following format to set an alert: \n"
                 "YYYY-MM-DD"
                 )
    else: 
        start_time = datetime.datetime.now()"""

bot.run(bot_key,
            log_handler= handler
            )