from discord.ext import commands, tasks
from dotenv import load_dotenv
import discord
import os
import logging 
import api_calls
import time
import datetime
from utils import parser

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
async def price(ctx,*, item, member: discord.Member = None):
    try:
        if member is None:
            member = ctx.author
        #testing this
        emoji = ctx.bot.get_emoji(1357688180089819177)
        print(item)
        item = parser.priceParse(item)
        call = await api_calls.request_item(item)
        embed = discord.Embed(
            title=f"Your requested item: `{item}`",
            description="Here are some offers available on Warframe Market",
            color=discord.Color.green()
        )
        embed.set_author(name=member.display_name, icon_url=member.avatar.url)
        embed.set_thumbnail(url="https://warframe.market/static/build/resources/images/logo-black.3bec6a3a0f1e6f1edbb1.png")
        #Testing
        for i in range(0, len(call)):
                # This is prettier i think...
                embed.add_field(name=f"{i}.- Seller", value=
                                f" > Name: [{call[i]['name']}](https://warframe.market/profile/{call[i]['name']}) \n "
                                f" > Price: {call[i]["price"]} {emoji} \n"
                                f" > Stock: {call[i]["quantity"]}  \n"
                                f" > Platform: {call[i]["platform"]}"
                                , inline=True)
        #Testing
        embed.set_footer(text="WarframeMarketBot - type !help to get more info about commands!")
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"An error occurred in your query, please try again later. Details: {e}")

@bot.command()
async def baro(ctx):
    try:
        call = await api_calls.void_trader()
        if call["Active"] is True:
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
        else: 
            embed = discord.Embed(
                title="Baro Ki'Teer",
                description="Sorry Tenno, Baro Ki'Teer is not in the solar system right now. \n",
                color=discord.Color.green()
            )
            

        #embed.set_image(url="https://static.wikia.nocookie.net/warframe/images/a/a7/TennoCon2020BaroCropped.png/revision/latest?cb=20200712232455")
        embed.set_footer(text="WarframeMarketBot - type !help to get more info about commands!")
        await ctx.send(embed=embed)
    except Exception as e: 
        await ctx.send(f"An error occurred in your query, please try again later. Details: {e}")

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
        embed.add_field(name="Can be found in the following relics:", value=f"{relics}")
        embed.set_footer(text="WarframeMarketBot - type !help to get more info about commands!")
        await ctx.send(embed=embed)
    except Exception as e: 
        await ctx.send(f"An error occurred in your query, please try again later. Details: {e}")

@bot.command()
async def weapon(ctx,*, item, member: discord.Member = None):
    try:
        if member is None:
            member = ctx.author
        call = await api_calls.weapon_info(item)
        embed = discord.Embed(
            title=f"Your requested item: `{item}`",
            description=f"__Weapon type:__ {call['Type']}",
            color=discord.Color.green()
        )
        embed.set_author(name=member.display_name, icon_url=member.avatar.url)
        embed.set_thumbnail(url=call["Image"])
        embed.add_field(name="Basic stats", value=
                        f"> Critical chance: {call["Stats"]["crit_chance"]} \n"
                        f"> Critical multiplier: {call["Stats"]["crit_mult"]}\n"
                        f"> Fire rate: {call["Stats"]["fire_rate"]}\n"
                        f"> Magazine: {call["Stats"]["mag_size"]}\n"
                        f"> Multishot: {call["Stats"]["multi_shot"]}\n"
                        )
        embed.add_field(name="__🔸 Attack Types:__", value="", inline=False)
        # Maybe store call["Atack"] for more redeability?
        for i in range(0, len(call["Atacks"])):
            embed.add_field(name=f"{call['Atacks'][i]["name"]}", value=
                            f" > Speed: {call['Atacks'][i]["speed"]} \n"
                            f" > Critical Chance: {call['Atacks'][i]["crit_chance"]} \n"
                            f" > Critical Multiplier: {call['Atacks'][i]["crit_mult"]} \n"
                            f" > Status Chance: {call['Atacks'][i]["status_chance"]} \n"
                            , inline=True)
        embed.add_field(name="", value=f"You can find a related build to [{item}](https://overframe.gg/?hl=es) here.", inline=False)
        embed.set_footer(text="WarframeMarketBot - type !help to get more info about commands!")
        await ctx.send(embed=embed)
    except Exception as e: 
        await ctx.send(f"An error occurred in your query, please try again later. Details: {e}")

@bot.command()
async def warframe(ctx,*, warframe, member: discord.Member = None):
    try:
        if member is None:
            member = ctx.author
        call = await api_calls.get_warframe(warframe)
        embed = discord.Embed(
            title=f"Your requested warframe: `{warframe}`",
            description="The called warframe has the following stats:",
            color=discord.Color.green()
        )
        embed.set_author(name=member.display_name, icon_url=member.avatar.url)
        embed.set_thumbnail(url=call["Image"])
        embed.add_field(name="Health", value= f"{call["Health"]}", inline=True)
        embed.add_field(name="Armor", value= f"{call["Armor"]}", inline=True)
        embed.add_field(name="Energy", value= f"{call["Energy"]}", inline=True)
        embed.add_field(name="Shields", value= f"{call["Shields"]}", inline=True)
        embed.add_field(name="Aura", value= f"{call["Aura"]}", inline=True)
        embed.add_field(name="Mastery Required", value= f"{call["Mastery"]}", inline=True)
        embed.set_footer(text="WarframeMarketBot - type !help to get more info about commands!")
        await ctx.send(embed=embed)
    except Exception as e: 
        await ctx.send(f"An error occurred in your query, please try again later. Details: {e}")

@bot.command()
async def helpme(ctx):
    try:
        botImage = bot.user.avatar.url
        embed = discord.Embed(
            title="Hi! I'm WarframeMarketBot",
            description="I can help you with the following commands:",
            color=discord.Color.green()
        )
        embed.add_field(name="", value=""
                                    "`!price <item>` Get the price of an item on Warframe Market. \n"
                                    "\n"
                                    "`!drops <item>` Get the relics where you can find an item. \n"
                                    "\n"
                                    "`!weapon <item>` Get the stats of a weapon. \n"
                                    "\n"
                                    "`!warframe <warframe>` Get the stats of a warframe. \n"
                                    "\n"
                                    "`!baro` Get the current status of Baro Ki'Teer. \n"
                                    )
        embed.set_thumbnail(url=botImage)
        embed.set_footer(text="WarframeMarketBot - Call me when you need me!")
        await ctx.send(embed=embed)
    except Exception as e: 
        await ctx.send(f"An error occurred in your query, please try again later. Details: {e}")

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