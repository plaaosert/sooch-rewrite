"""
Handles incoming messages and dispatches them to the appropriate handler.
"""
from dataclasses import dataclass, field
from typing import Callable, Optional, List, Dict, Coroutine, Any

import discord
from sooch.commands import base, misc, help


@dataclass
class Command:
    """Class representing a command that can be executed."""
    handler: Callable[[discord.Client, discord.Message, List[str]],
                      Coroutine[Any, Any, Optional[discord.Embed]]]
    name: str = "s!invalid"
    description: str = "No description provided"
    syntax: Optional[str] = None
    aliases: List[str] = field(default_factory=list)


valid_prefix = {
    "s!": True,
    "s.": True,
    "s$": True,
    "S!": True,
    "S.": True,
    "S$": True
}


commands = [
    Command(
        name="s!credits",
        description="Show all the people that helped make Sooch a reality",
        aliases=["s!cr"],
        handler=misc.credits_command
    ),
    Command(
        name="s!claim",
        description="Claim the hard-made sooch your buildings made",
        aliases=["s!c"],
        handler=base.claim
    ),
    Command(
        name="s!help",
        description="Get help",
        aliases=["s!h"],
        syntax="s!help <command>",
        handler=help.help_command
    ),
]
invalid_command = Command(handler=misc.invalid)
help.populate_help_embeds(commands)

command_lookup: Dict[str, Command] = {}
for cmd in commands:
    command_lookup[cmd.name] = cmd
    for alias in cmd.aliases:
        command_lookup[alias] = cmd


async def on_message(client: discord.Client, message: discord.Message):
    """
    Handle incoming messages from Discord, dispatching it to commands/invalid
    command handler if necessary
    """
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
    command = command_lookup.get(content[0].lower(), invalid_command)
    to_send = await command.handler(client, message, content)
    if to_send is not None:
        to_send.title = content[0]
        to_send.description = "Requested by {}".format(message.author.mention)
        await message.channel.send(embed=to_send)
