import json
import logging
import os
import sys

import discord

from sooch.database import Database
from sooch.listeners import GuildJoinListener, ReadyListener
from sooch.servers import Servers
from logging.handlers import TimedRotatingFileHandler
from logging import StreamHandler, Formatter, DEBUG


class SoochBot(discord.Client):
    def __init__(self):
        formatter = Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
        file_handler = TimedRotatingFileHandler(
            filename="sooch.log",
            when="midnight",
            backupCount=14,
            encoding="utf-8",
            utc=True
        )
        file_handler.setFormatter(formatter)
        stream_handler = StreamHandler(stream=sys.stdout)
        stream_handler.setFormatter(formatter)
        self.logger = logging.getLogger("sooch")
        self.logger.setLevel(DEBUG)
        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)
        discord_logger = logging.getLogger("discord")
        discord_logger.setLevel(DEBUG)
        discord_logger.addHandler(stream_handler)
        discord_logger.addHandler(file_handler)
        self.config = self.load_config()
        self.database = Database(self.config)
        self.servers = Servers(self.database)
        self.ready_listener = ReadyListener(self.servers)
        self.guild_join_listener = GuildJoinListener(self.servers)
        super().__init__(command_prefix=self.get_server_prefix)

    def load_config(self):
        self.save_default_config()
        with open("./config.json", "r", encoding="utf-8") as config_file:
            config_text = config_file.read()
            return json.loads(config_text)

    def save_default_config(self):
        if not os.path.isfile("./config.json"):
            with open("./config.json", "w", encoding="utf-8") as config_file:
                config_file.writelines(json.dumps({
                    "token": "",
                    "database": {
                        "type": "sqlite",
                        "file": "./sooch.db"
                    }
                }))

    async def get_server_prefix(self, bot, message):
        server = await self.servers.get_server(message.guild_id)
        return server.command_prefix

    def start_sooching(self):
        self.run(self.config["token"])

    async def on_ready(self):
        await self.ready_listener.on_ready(self)

    async def on_guild_join(self, guild):
        await self.guild_join_listener.on_guild_join(guild)


def main():
    sooch_bot = SoochBot()
    sooch_bot.start_sooching()


main()
