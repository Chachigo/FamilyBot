from interactions import *
from datetime import datetime
from interactions.ext.prefixed_commands import prefixed_command, PrefixedContext
import requests
import json
import time
from config import *

class free_epicgames(Extension):
    def __init__(self,bot):
        print("Epic Games Plugin loaded")

    force = False
    
    @Task.create(IntervalTrigger(seconds=10))
    async def send_epic_free_games(self) -> None:
        now = datetime.now()
        if self.force == True or now.weekday() == 3 and now.hour == 17 and now.minute == 15:
            epic_games_channel = await self.bot.fetch_channel(EPIC_CHANNEL_ID)
            epic_url = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=fr&country=FR&allowCountries=FR"
            base_shop_url = "https://store.epicgames.com/fr/p/"

            answer = requests.get(epic_url)

            json_answer = json.loads(answer.text)

            game_list = json_answer["data"]["Catalog"]["searchStore"]["elements"]
            await epic_games_channel.send("The free games on the Epic Game Store this week are:")
            for game in game_list:
                if (game["offerType"] == 'BASE_GAME'
                    and game["price"]["totalPrice"]["discountPrice"] == 0
                    and game["status"] == "ACTIVE"
                    and len(game["promotions"]["promotionalOffers"]) == 1):
                    try:
                        game_epic_id = game["offerMappings"][0]["pageSlug"]
                    except:
                        game_epic_id = game["urlSlug"]
                    await epic_games_channel.send(base_shop_url + game_epic_id)
            time.sleep(60)

    @prefixed_command(name="force_epic")
    async def force_command(self,ctx: PrefixedContext)-> None:
        if ctx.author_id == ADMIN_DISCORD_ID and ctx.guild is None:
            self.force = True
            await self.send_epic_free_games()
            self.force = False
            await self.bot.send_log_dm("Force epic")
            return
    
    @listen()
    async def on_startup(self):
        self.send_epic_free_games.start()
        print("--Epic Games Task Started")