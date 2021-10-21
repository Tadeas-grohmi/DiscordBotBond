import discord
import asyncio
from discord.ext.buttons import Paginator
from pymongo import MongoClient
import certifi

class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass

def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content
        
        
async def zapis(command):
    mango_url = "mongodb+srv://Bond:Drago00914*@disbotbond.xo3fb.mongodb.net/test"
    cluster = MongoClient(mango_url, tlsCAFile=certifi.where())
    db = cluster["Zaznamy"]
    collection = db["zaznamy"]
    data = collection.find_one({"_id": "Zaznamy"})
    if data == None:
        collection.insert({
            "_id":"Zaznamy"
        })
    else:
        data = collection.find_one({"_id": "Zaznamy"})
        post = ({"$inc": {f"{command}": 1}})
        collection.update(data, post)