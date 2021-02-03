"""
The entry point of SoochBot. Initializes all components and starts handling
commands when start_sooching() is called.
"""

import json
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from logging import StreamHandler, Formatter, DEBUG

import discord

from sooch import message
from sooch.database import Database
from sooch.listeners import GuildJoinListener, ReadyListener
from sooch.servers import Servers


class SoochBot(discord.Client):
    """Represent an instance of SoochBot."""

    def __init__(self):
        formatter = Formatter(
            "%(asctime)s:%(levelname)s:%(name)s: %(message)s")
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

        super().__init__()

    def load_config(self):
        """
        Load configs from a config file, generating the default one if
        necessary.
        """
        self.save_default_config()
        with open("./config.json", "r", encoding="utf-8") as config_file:
            config_text = config_file.read()
            return json.loads(config_text)

    @staticmethod
    def save_default_config():
        """
        Save the default config file at the expected location if it
        does not exist.
        """
        if not os.path.isfile("./config.json"):
            with open("./config.json", "w", encoding="utf-8") as config_file:
                config_file.writelines(json.dumps({
                    "token": "",
                    "database": {
                        "type": "sqlite",
                        "file": "./sooch.db"
                    }
                }))

    def start_sooching(self):
        """Start the bot with the token present in the config."""
        self.run(self.config["token"])

    async def on_ready(self):
        await self.ready_listener.on_ready(self)

    async def on_guild_join(self, guild):
        await self.guild_join_listener.on_guild_join(guild)

    async def on_message(self, msg: discord.Message):
        """Handle messages that are command and ignore others."""
        await message.on_message(self, msg)


def main():
    """Create an instance of SoochBot and start it."""
    sooch_bot = SoochBot()
    sooch_bot.start_sooching()


main()
