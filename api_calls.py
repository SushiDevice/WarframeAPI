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
            result = result["payload"]["orders"]
            sellers = []
            counter = 0
            for i in result:
                if i["order_type"] == "sell":
                    seller = dict.fromkeys(["name", "price", "quantity", "platform"])
                    seller["price"] = i["platinum"]
                    seller["quantity"] = i["quantity"]
                    seller["name"] = i["user"]["ingame_name"]
                    seller["platform"] = i["user"]["platform"]
                    # Append the dictionary into the list 
                    # we get a list of dictionaries 
                    sellers.append(seller)
                    counter+=1
                    # Limit the number of sellers or we die
                    if counter == 12:
                        break
            return sellers

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

async def weapon_info(item: str):
    async with aiohttp.ClientSession() as session:
       async with session.get(f"{SbaseURL}/items/{item}") as response:
            result = await response.json()
            damages = result["damage"]
            #damageStat = damages.items()
            # Store as a list of tuples
            #damageStat = "\n".join([f"{k}: {v}" for k, v in damageStat])
            atacks = result["attacks"]
            # Image from wiki 
            #image = result["wikiaThumbnail"]
            f_result = {
                #"Stats": damageStat,
                #"Image": image,
                "Atacks": atacks,
                }            
            return f_result["Atacks"][0]
       
async def get_warframe(warframe: str):
    async with aiohttp.ClientSession() as session:
       async with session.get(f"{SbaseURL}/warframes/search/{warframe}") as response:
            result = await response.json()
            # When querying a base warframe, the result is a list containing the base warframe and the prime version
            # We need to get the first element of the list to get the base warframe
            # If prime is called, then we only get the prime, so its the same process
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
       
test = asyncio.run(weapon_info("boltor"))
print(test)
