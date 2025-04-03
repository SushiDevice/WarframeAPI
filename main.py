from discord.ext import commands
from dotenv import load_dotenv
import discord
import os
import logging 
import api_calls


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

#client = discord.Client(intents = intents)

bot = commands.Bot( command_prefix='!',
                    intents=intents
                    )


@bot.command()
async def items(ctx, item):
    try:
        call = await api_calls.request_item(item)
        await ctx.send(f"your item is: {call['price']} platinum on warframe market seller, from user {call['seller']}. Has {call['quantity']} in stock")
    except:
        await ctx.send(f"An error ocurred in your query, please try again later")
     
bot.run(bot_key,
            log_handler= handler
            )