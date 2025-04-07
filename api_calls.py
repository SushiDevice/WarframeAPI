import aiohttp
import asyncio

MbaseURL = "https://api.warframe.market/v1"
SbaseURL = "https://api.warframestat.us"

#todo ==> I should create an only session instance for all this request to the API

async def request_item(item: str):
    async with aiohttp.ClientSession() as session:
       async with session.get(f"{MbaseURL}/items/{item}/orders") as response:
            result = await response.json()
            result = result["payload"]["orders"][0] 
            price = result["platinum"]
            seller = result["user"]["ingame_name"]
            quantity = result["quantity"]
            f_result = {
                        "price": price,
                        "seller": seller,
                        "quantity": quantity
                        }
            return f_result

#Todo ==> add inventory
async def void_trader():
    async with aiohttp.ClientSession() as session:
       async with session.get(f"{SbaseURL}/pc/voidTrader") as response:
            result = await response.json()
            start = result["activation"]
            ends = result["expiry"]
            location = result["location"]
            f_result = {
                "Start": start,
                "Ends": ends,
                "Location":location,
            }
            return f_result

async def get_drop(item: str):
    async with aiohttp.ClientSession() as session:
       async with session.get(f"{SbaseURL}/drops/search/{item}") as response:
            result = await response.json()
            relics = []
            # Response is a list of objects
            for i in result:
                relics.append(i["place"])
                continue                
            f_result = {
                "Relics": relics
            }
            return f_result

#test = asyncio.run(get_drop("gauss prime blueprint"))
#print(test)
