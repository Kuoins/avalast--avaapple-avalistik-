from modules.base_module import Module
from modules.location import refresh_avatar
import threading
import time
import asyncio

class_name = "News"

CACHE_TIME = 300

PICTURE_DIRECTORY = "http://ava-box.ml/files/promo/"

class News(Module):
    prefix = "nws"

    def __init__(self, server):
        self.server = server
        self.commands = {"ugt": self.update_news, "getglbl": self.get_global_news}
        self.newsList = []
        thread = threading.Thread(target=self._background)
        thread.daemon = True
        thread.start()
 
    async def update_news(self, msg, client):      
        await client.send(["nws.hasnews", {"gnexst": True, "gnunr": False}])    

    async def get_global_news(self, msg, client):
        await client.send(["nws.getglbl", {'nlst': {'l': self.newsList}}])    

    async def global_news(self):
        news_list = []
        r = self.server.redis
        for news in await r.smembers("news:global_news"):
            news_id = news
            add_time = await r.get(f"news:global_news:{news_id}:add_time")
            title = await r.get(f"news:global_news:{news_id}:title")
            message = await r.get(f"news:global_news:{news_id}:message")
            picture_name = await r.get(f"news:global_news:{news_id}:picture_url")
            action = await r.get(f"news:global_news:{news_id}:action")
            url = await r.get(f"news:global_news:{news_id}:url")
            picture_url = f"{PICTURE_DIRECTORY}{picture_name}.png"
            news_list.append({"i": news_id, "n": True, "tp": "gi", "tm": add_time, "te": 0, "rm": False, "trgt": 0,
                              "ttl": title, "msg": message, "purl": picture_url, "tgt": action, "url": url, "sbtp": None})                
        return news_list
        
    def _background(self):
        while True:
            self.newsList = global_news(self)
            asyncio.sleep(CACHE_TIME)     