"""
Module that contains base command.
A base command is a command that is immediately accessible to the player at the
start of the game and necessary for progression.
"""
import math
import time
from typing import Optional

import discord

from sooch import buildings
from sooch.player import Player
from sooch.services.players_load import Players
from sooch.services.reg_buildings import RegBuildings
from sooch.services.claiming import claim_all

player_svc: Optional[Players] = None
reg_buildings_svc: Optional[RegBuildings] = None


async def setup_default_player(discord_id: int, discord_name: str) -> Player:
    """Setup default player info in the database."""
    # Not in database so setup default.
    player = Player.from_new_player(discord_id, discord_name)
    await player_svc.add_player(player)
    return player


async def claim(client: discord.Client,
                message: discord.Message,
                content: list[str]) -> Optional[discord.Embed]:
    """Handle the s!claim command."""
    del client, content
    player_id = message.author.id
    player_name = message.author.name

    player = await player_svc.get_player(player_id)
    if player is None:
        player = await setup_default_player(player_id, player_name)

    claim_result = claim_all(player)

    result = discord.Embed()
    # Embed here needs to be modular since we have a lot of claim info. Do later todo

    return result
