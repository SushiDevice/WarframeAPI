import aiohttp
import asyncio # For testing purposes

MbaseURL = "https://api.warframe.market/v1"
SbaseURL = "https://api.warframestat.us"
# Still not useful
#AssetUrl = "https://warframe.market/static/assets"

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

async def item_info(item: str):
    async with aiohttp.ClientSession() as session:
       async with session.get(f"{SbaseURL}/items/{item}") as response:
            result = await response.json()
            damages = result["damage"]
            damageStat = damages.items()
            # Store as a list of tuples
            damageStat = "\n".join([f"{k}: {v}" for k, v in damageStat])
            # Image from wiki 
            image = result["wikiaThumbnail"]
            f_result = {
                "Stats": damageStat,
                "Image": image
                }            
            return f_result
       
async def get_warframe(warframe: str):
    async with aiohttp.ClientSession() as session:
       async with session.get(f"{SbaseURL}/warframes/search/{warframe}") as response:
            result = await response.json()
            # When querying a base warframe, the result is a list containing the base warframe and the prime version
            # We need to get the first element of the list
            result = result[0]
            health = result["health"]
            armor = result["armor"]
            shields = result["shield"]
            energy = result["power"]
            image = result["wikiaThumbnail"]
            aura = result["aura"]
            mastery = result["masteryReq"]
            f_result = {
                "Health": health,
                "Armor": armor,
                "Shields": shields,
                "Energy": energy,
                "Image": image,
                "Aura": aura,
                "Mastery": mastery
            }
            return f_result
       
test = asyncio.run(get_warframe("volt"))
print(test)
