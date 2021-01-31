import logging

from sooch.servers import Server


class GuildJoinListener:
    def __init__(self, servers):
        self.servers = servers
        self.logger = logging.getLogger("sooch")

    async def on_guild_join(self, guild):
        self.logger.info("Joined guild %s, checking if we've been here before", guild.name)
        server = await self.servers.get_server(guild.id)
        if server is None:
            self.logger.info("Guild %s is a new guild that was not found in our database, adding it.", guild.name)
            await self.servers.add_server(Server(
                guild.id,
                guild.name,
                "s!"
            ))


class ReadyListener:
    def __init__(self, servers):
        self.servers = servers
        self.logger = logging.getLogger("sooch")

    async def on_ready(self, client):
        self.logger.info("Connected to Discord.")
        for guild in client.guilds:
            self.logger.info("Found guild %s, checking we have a copy in the database.", guild.name)
            server = await self.servers.get_server(guild.id)
            if server is None:
                self.logger.info("Guild %s was not in the database, adding it.", guild.name)
                await self.servers.add_server(Server(
                    guild.id,
                    guild.name,
                    "s!"
                ))
