from typing import Callable, Optional
from sooch.commands import *

import discord


class Command:
    def __init__(self,
                 handler: Callable[[discord.Client, str, list[str]],
                                   Optional[discord.Embed]],
                 name: str = "s!invalid",
                 description: str = "No description provided",
                 syntax: Optional[str] = None,
                 aliases: list[str] = ["None"]):
        self.name = name
        self.aliases = aliases
        self.description = description
        self.syntax = syntax
        self.handler = handler
        if syntax is None:
            # Default to just the name if it's not provided.
            self.syntax = self.name


valid_prefix = {
    "s!": True,
    "s.": True,
    "s$": True
}


commands = {
    "s!credits": Command(
        name="s!credits",
        description="Show all the people that helped make Sooch a reality",
        handler=misc.credits
    ),
    "s!help": Command(
        name="s!help",
        description="Get help.",
        aliases=["s!h"],
        handler=help.help
    )
}
invalid_command = Command(handler=misc.invalid)


async def on_message(client: discord.Client, message: discord.Message):
    if message.author.bot:
        # Ignore all bot messages.
        return
    if not valid_prefix.get(message.content[:2], False):
        # Check if the prefix is valid.
        # If it's not, ignore the message.
        return

    if message.content[:2] == "s.":
        # TODO: Check for server admin
        pass
    elif message.content[:2] == "s$":
        # TODO: Check for bot admin
        pass

    content = message.content.split(" ")
    command = commands.get(content[0], invalid_command)
    to_send = await command.handler(client, message, content)
    if to_send is not None:
        to_send.title = content[0]
        to_send.description = "Requested by {}".format(message.author.mention)
        await message.channel.send(embed=to_send)
