import logging
import os
from urllib.parse import urljoin
import discord
from slugify import slugify
from vodscraper import getVod
class VodBot(discord.Client):
    def __init__(self,debug=True):
        super().__init__()
        if(debug):
            if(not os.path.exists("./logs")):
                os.mkdir("./logs")
            logger = logging.getLogger('discord')
            logger.setLevel(logging.DEBUG)
            handler = logging.FileHandler(filename="./logs/discord.log",encoding="utf-8",mode="a")
            handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")) 
            logger.addHandler(handler)
    
    async def on_ready(self):
        print("logged in as {0}!".format(self.user))
    
    async def on_message(self,message):
        if(message.author == self.user):
            return
        elif message.content.startswith("vodbot -h"):
            await message.channel.send(
"""```Usage: vodbot 
Flags:
    -h : help 
    -c : Designates that the item after this is a character name
    -p : Designates that the item after this is a player name 
    -t : Designates that the item after this is a tournament name
Examples:
    vodbot -c mario
    vodbot -p tweek
    vodbot -t Get On My Level 2019
    vodbot -c roy -p tweek -t Get On My Level 2019
```""")
            return None
        elif message.content.startswith("vodbot"):
            flags = {"-c":"character","-p":"player","-t":"tournament"}
            parameter_dict = {"character":"","player":"","tournament":""} 
            parameters = message.content.split(" ")
            if(len(parameters) == 1):
                await message.channel.send("Please enter a query with the correct flags type vodbot -h for help")    
                return None
            for i,parameter in enumerate(parameters):
                if(parameter in flags):
                    if(parameters[i+1] in flags):
                        await message.channel.send("Your search is malformed view help by typing vodbot -h")
                        return None
                    parameter_dict[flags[parameter]] = parameters[i+1]
            video_url = getVod(**parameter_dict) 
            if(video_url == None):
                await message.channel.send("Could not find a video for the given search terms")
                return None
            await message.channel.send("https:"+video_url)
            return None
if __name__ == "__main__":
    test_bot = VodBot()
    test_bot.run("Enter Token Here") 
