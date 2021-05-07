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
from sooch.services.players import Player, Players
from sooch.services.reg_buildings import RegBuildings

player_svc: Optional[Players] = None
reg_buildings_svc: Optional[RegBuildings] = None


async def setup_default_player(discord_id: int) -> Player:
    """Setup default player info in the database."""
    # Not in database so setup default.
    player = Player(
        discord_id=discord_id,
        sooch=10,
        # Free 1 minute claim to get the player started.
        last_claim=int(time.time()) - 60,
    )
    await player_svc.add_player(player)
    return player


async def claim(client: discord.Client,
                message: discord.Message,
                content: list[str]) -> Optional[discord.Embed]:
    """Handle the s!claim command."""
    del client, content
    player_id = message.author.id

    player = await player_svc.get_player(player_id)
    if player is None:
        player = await setup_default_player(player_id)

    new_time = int(time.time())
    delta_seconds = new_time - player.last_claim
    delta_min = math.floor(delta_seconds / 60)  # TODO: Claim time acceleration

    if delta_min < 1:
        # TODO: Claim time acceleration
        return discord.Embed().add_field(
            name="There is nothing to claim",
            value=(f"There is nothing to claim at the moment. "
                   f"Try again in {60 - delta_seconds} seconds.")
        )

    count = await reg_buildings_svc.get_building_count(player_id)
    income_per_min = 0
    building_count = 0
    for building_id, building in enumerate(buildings.reg_buildings):
        income_per_min += count[building_id] * building.income / 60
        building_count += count[building_id]

    income = income_per_min * delta_min
    new_sooch_balance = player.sooch + income
    await player_svc.set_last_claim(player_id, new_time)
    await player_svc.set_sooch(player_id, new_sooch_balance)

    # TODO: Format everything correctly.
    result = discord.Embed()
    if delta_min == 1:
        result.add_field(
            name="Claim Results",
            value=("Claimed {} Sooch from a total of "
                   "{} properties after 1 minute.").format(
                       income, building_count),
            inline=False
        )
    else:
        result.add_field(
            name="Claim Results",
            value=("Claimed {} Sooch from a total of "
                   "{} properties after {} minutes.").format(
                       income, building_count, delta_min),
            inline=False
        )
    result.add_field(
        name="New Balance",
        value=f"{new_sooch_balance} Sooch",
        inline=False
    )

    return result


async def build(client: discord.Client,
                message: discord.Message,
                content: list[str]) -> Optional[discord.Embed]:

    player_id = message.author.id
    # Get the Sooch player
    player = await player_svc.get_player(player_id)
    if not player:
        player = setup_default_player(player_id)

    # Prepare the embed, in case we want to also include claim information
    result = discord.Embed()

    new_time = int(time.time())
    delta_seconds = new_time - player.last_claim
    # TODO: Claim time acceleration - maybe separate this into its own function?
    delta_min = math.floor(delta_seconds / 60)
    # If it's been more than one minute, claim any sooch
    if delta_min > 0:
        result = await claim(client, message, content)

    # Get basic player information.
    old_balance = player.sooch
    # If there's no building specified to be built
    if not content[1:]:
        # TODO: Print building list
        return result
    else:
        # Surround this with a try in case a player tries to access a building that doesn't exist.
        try:
            # If searching by numeric ID
            if content[1].isnumeric():
                # Add 1 to it so
                building = buildings.reg_buildings[int(content[1]) - 1]
            else:
                building = buildings.reg_building_lookup[content[1]]
        except IndexError:
            # TODO: send error message
            return result

    amount = 1
    # If an amount has been specified
    if content[2:] and content[2].isnumeric():
        amount = int(content[2])
    # Get the required cost for building the properties
    building_array = await reg_buildings_svc.get_building_count(player_id)
    building_amount = building_array[building.id]
    required_cost = building.get_cost(building_amount, building_amount + amount, 1.0)  # TODO: variable cost reduction
    # If the player can afford to build the new properties, let them proceed.
    # If not, tell them they can't afford the property/ies.
    if player.sooch >= required_cost:
        # Set the new sooch amount and build count.
        await player_svc.set_sooch(player_id, player.sooch - required_cost)
        await reg_buildings_svc.set_building_count(player_id, building.id, building_array[building.id] + amount)
        return result  # TODO: bought
    else:
        return result  # TODO: cannot buy

