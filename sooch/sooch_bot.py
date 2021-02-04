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

from sooch import listeners, message, path
from sooch.commands import base
from sooch.database import Database
from sooch.services.players import Players
from sooch.services.reg_buildings import RegBuildings
from sooch.services.servers import Servers


class SoochBot(discord.Client):
    """Represent an instance of SoochBot."""

    def __init__(self):
        formatter = Formatter(
            "%(asctime)s:%(levelname)s:%(name)s: %(message)s")
        log_path = path.from_root("sooch.log")
        file_handler = TimedRotatingFileHandler(
            filename=log_path,
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

        # Read from config.
        self.config = self.load_config()
        self.database = Database(self.config)

        # Initialize all the other modules.
        listeners.servers = Servers(self.database)
        base.player_svc = Players(self.database)
        base.reg_buildings_svc = RegBuildings(self.database)

        super().__init__()

    def load_config(self):
        """
        Load configs from a config file, generating the default one if
        necessary.
        """
        self.save_default_config()
        config_path = path.from_root("config.json")
        with open(config_path, "r", encoding="utf-8") as config_file:
            config_text = config_file.read()
            return json.loads(config_text)

    def save_default_config(self):
        """
        Save the default config file at the expected location if it
        does not exist.
        """
        config_path = path.from_root("config.json")
        if not os.path.isfile(config_path):
            with open(config_path, "w", encoding="utf-8") as config_file:
                config_file.writelines(json.dumps({
                    "token": "",
                    "database": {
                        "type": "sqlite",
                        "file": "./sooch.db"
                    }
                }, indent=4))
            self.logger.info(
                "Config file has been created. Please fill in the token.")
            sys.exit()

    def start_sooching(self):
        """Start the bot with the token present in the config."""
        self.run(self.config["token"])

    async def on_ready(self):
        """Prepare the SoochBot to serve commands when it connects."""
        await listeners.on_ready(self)

    async def on_guild_join(self, guild):
        """Register the guild that just joined if necessary."""
        await listeners.on_guild_join(guild)

    async def on_message(self, msg: discord.Message):
        """Handle messages that are command and ignore others."""
        await message.on_message(self, msg)


def main():
    """Create an instance of SoochBot and start it."""
    sooch_bot = SoochBot()
    sooch_bot.start_sooching()


main()
