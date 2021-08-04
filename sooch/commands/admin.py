"""
Module that contains admin commands.
An admin command is a command that is only accessible to admins and should never be granted to a normal player
(as they contain direct SQL evals, unlimited data manipulation, etc.)
"""
from typing import List, Optional

import discord

from sooch.commands.shared import services
from sooch.services.players_load import Players
from sooch.services.reg_buildings import RegBuildings


async def set_building(client: discord.Client,
                       message: discord.Message,
                       content: List[str]) -> Optional[discord.Embed]:
    result = discord.Embed()

    await services.reg_buildings_svc.set_building_count(message.author.id, int(content[1]), int(content[2]))

    result.add_field(name="Set building", value="{} amount = {}".format(content[1], content[2]))
    return result