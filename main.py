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
        embed.set_footer(text="WarframeMarketBot")
        await ctx.send(embed=embed)

    except:
        await ctx.send("An error ocurred in your query, please try again later")

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
        embed.add_field(name="Relic", value="Soy una reliquia", inline=False)
        #embed.set_image(url="https://static.wikia.nocookie.net/warframe/images/a/a7/TennoCon2020BaroCropped.png/revision/latest?cb=20200712232455")
        embed.set_footer(text="WarframeMarketBot")
        await ctx.send(embed=embed)
    except:
        await ctx.send(f"An error ocurred in your query, please try again later")

# In construction
@bot.command()
async def set_alert(ctx, time):

    if not time:
        ctx.send("Please provide a date value in the following format to set an alert: \n"
                 "YYYY-MM-DD"
                 )
    else: 
        start_time = datetime.datetime.now()


@bot.command()
async def get_drops(ctx, item):
    try:
        call = await api_calls.request_item(item)
        embed = discord.Embed(
            title=f"Your requested item '{item}' can be found in the following relics",
            description=(
               
            ),
            color=discord.Color.green()
        )
        embed.add_field(name="Relic", value=call['Relic'], inline=False)
        embed.set_footer(text="WarframeMarketBot")
        await ctx.send(embed=embed)

    except:
        await ctx.send("An error ocurred in your query, please try again later")


bot.run(bot_key,
            log_handler= handler
            )