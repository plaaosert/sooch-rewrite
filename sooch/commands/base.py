"""
Module that contains base command.
A base command is a command that is immediately accessible to the player at the
start of the game and necessary for progression.
"""
import math
import time
from typing import Optional, List

import discord

from sooch import buildings
from sooch.player import Player
from sooch.commands.shared import services
from sooch.services.claiming import claim_all


async def setup_default_player(client, discord_id: int, discord_name: str) -> Player:
    """Setup default player info in the database."""
    # Not in database so setup default.
    player = Player.from_new_player(client, discord_id, discord_name)
    await services.player_svc.add_player(player)
    return player


async def claim(client: discord.Client,
                message: discord.Message,
                content: List[str]) -> Optional[discord.Embed]:
    """Handle the s!claim command."""
    player_id = message.author.id
    player_name = message.author.name

    player = await services.player_svc.get_player(player_id)
    if player is None:
        player = await setup_default_player(client, player_id, player_name)

    claim_result = claim_all(player)

    result = discord.Embed()
    # Embed here needs to be modular since we have a lot of claim info. Do later todo

    debug_data = (
        "hours",
        "spare_mins",
        "this_claim_mult",
        "basic_income",
        "trans_income",
        "crit_success",
        "items_gained",
        "tax_loss",
        "event_currency"
    )

    player_debug_data = (
        "base_income",
        "income"
    )

    result.add_field(name="Result test", value="```\n" + "\n".join("{:20} {}".format(
        d + ":", getattr(claim_result, d)
    ) for d in debug_data) + "\n```")

    result.add_field(name="Player attributes", value="```\n" + "\n".join("{:20} {}".format(
        d + ":", getattr(player, d)
    ) for d in player_debug_data) + "\n```", inline=False)

    return result
