"""Implement listeners for all the events SoochBot cares about."""
import logging

import discord

from sooch.servers import Server, Servers


logger = logging.getLogger("sooch")


async def on_guild_join(servers: Servers, guild: discord.Guild):
    """Handle guild joins, adding it to the database as necessary."""
    logger.info(
        "Joined guild %s, checking if we've been here before", guild.name)
    server = await servers.get_server(guild.id)
    if server is None:
        logger.info(
            ("Guild %s is a new guild that was not found in our database,"
             "adding it."),
            guild.name)
        await servers.add_server(Server(
            guild.id,
            guild.name,
            "s!"
        ))


async def on_ready(client: discord.Client, servers: Servers):
    """Setup the bot with latest info from the Discord server."""
    logger.info("Connected to Discord.")
    for guild in client.guilds:
        logger.info(
            "Found guild %s, checking we have a copy in the database.",
            guild.name)
        server = await servers.get_server(guild.id)
        if server is None:
            logger.info(
                "Guild %s was not in the database, adding it.", guild.name)
            await servers.add_server(Server(
                guild.id,
                guild.name,
                "s!"
            ))
