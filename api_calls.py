import aiohttp
import asyncio
baseURL = "https://api.warframe.market/v1"

async def request_item(item: str):
    async with aiohttp.ClientSession() as session:
       async with session.get(f"{baseURL}/items/{item}/orders") as response:
            result = await response.json()
            #result = result["payload"]["item"]["items_in_set"][0]["tags"][0]
            price = result["payload"]["orders"][0]["platinum"]
            seller = result["payload"]["orders"][0]["user"]["ingame_name"]
            quantity = result["payload"]["orders"][0]["quantity"]
            f_result = {"price": price,
                        "seller": seller,
                        "quantity": quantity
                        }
            return f_result


#result = asyncio.run(request_item("mirage_prime_systems"))
#print(result)
