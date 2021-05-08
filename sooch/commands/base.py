"""
Module that contains base command.
A base command is a command that is immediately accessible to the player at the
start of the game and necessary for progression.
"""
import math
import time
from typing import Optional

import discord

from sooch import buildings, utilities
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
                       utilities.format_balance(income), building_count),
            inline=False
        )
    else:
        result.add_field(
            name="Claim Results",
            value=("Claimed {} Sooch from a total of "
                   "{} properties after {} minutes.").format(
                       utilities.format_balance(income), building_count, delta_min),
            inline=False
        )
    result.add_field(
        name="New Balance",
        value=f"{utilities.format_balance(new_sooch_balance)} Sooch",
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

    # Get basic player information.
    building_array = await reg_buildings_svc.get_building_count(player_id)
    old_balance = player.sooch
    old_income = utilities.determine_income(building_array)
    # If there's no building specified to be built
    if not content[1:]:
        result.add_field(
            name="Balance",
            value=f"Your current balance is {utilities.format_balance(player.sooch)}.",
            inline=False
        )
        start_search = 0
        end_search = 5
        list_count = 1
        while end_search != -1:
            value = ""
            # We'll grab up to 5 buildings at a time.
            for i in range(start_search, end_search):
                building = buildings.reg_buildings[i]
                building_amount = building_array[building.id]
                # TODO: Also cost reduction
                building_cost = building.get_cost(building_amount, building_amount + 1, 1.0)

                emote = "<:yes:805476872330543166>"
                # If the player cannot afford the building, prompt the program to finish searching after that bunch
                if building_cost > player.sooch:
                    emote = "<:nope:805476871982153748>"
                    end_search = -6
                value += f"{emote} **{i + 1}**) {building.name} - {utilities.format_balance(building_cost)} " \
                         f"<:sooch:804702160217440276>\n"
            start_search += 5
            end_search += 5
            if end_search >= len(buildings.reg_buildings):
                end_search = len(buildings.reg_buildings) - 1
            result.add_field(name=f"Price List {list_count}", value=value, inline=True)
            list_count += 1
        return result
    else:
        new_time = int(time.time())
        delta_seconds = new_time - player.last_claim
        # TODO: Claim time acceleration - maybe separate this into its own function?
        delta_min = math.floor(delta_seconds / 60)
        # If it's been more than one minute, claim any sooch
        if delta_min > 0:
            result = await claim(client, message, content)
        # Surround this with a try in case a player tries to access a building that doesn't exist.
        try:
            # If searching by numeric ID
            if content[1].isnumeric():
                # Add 1 to it so
                building = buildings.reg_buildings[int(content[1]) - 1]
            else:
                building = buildings.reg_building_lookup[content[1]]
        except KeyError or IndexError:
            result.add_field(
                name="This building doesn't exist.",
                value=f"Yeah, {content[1]} definitely doesn't exist.",
                inline=False
            )
            return result

    amount = 1
    # If an amount has been specified
    if content[2:] and content[2].isnumeric():
        amount = int(content[2])

    building_amount = building_array[building.id]
    new_amount = building_amount + amount
    required_cost = building.get_cost(building_amount, new_amount, 1.0)  # TODO: variable cost reduction
    # If the player can afford to build the new properties, let them proceed.
    # If not, tell them they can't afford the property/ies.
    if player.sooch >= required_cost:
        # Set the new sooch amount and build count.
        await player_svc.set_sooch(player_id, player.sooch - required_cost)
        await reg_buildings_svc.set_building_count(player_id, building.id, building_array[building.id] + amount)

        name = "New Propert"
        property_name = building.name
        if amount == 1:
            name += "y"
        else:
            name += "ies"
            property_name += "s"

        new_count = await reg_buildings_svc.get_building_count(player_id)
        result.add_field(
            name=name,
            value=f"Bought {amount} {property_name} for {utilities.format_balance(required_cost)} "
                  f"<:sooch:804702160217440276>. Income: **{utilities.format_balance(building.income)}** "
                  f"<:sooch:804702160217440276>/hr",
            inline=False
        )
        result.add_field(
            name="Income",
            value=f"{utilities.format_balance(old_income)} <:sooch:804702160217440276>/hr"
                  f"\n     ▼ ▼ ▼"
                  f"\n{utilities.format_balance(utilities.determine_income(new_count))}"
                  f" <:sooch:804702160217440276>/hr",
            inline=True
        )
        result.add_field(
            name="Balance",
            value=f"{utilities.format_balance(old_balance)} <:sooch:804702160217440276>"
                  f"\n     ▼ ▼ ▼"
                  f"\n{utilities.format_balance(old_balance - required_cost)} <:sooch:804702160217440276>",
            inline=True
        )
        result.add_field(
            name="Cost",
            value=f"{utilities.format_balance(required_cost)} <:sooch:804702160217440276> per {property_name}"
                  f"\n     ▼ ▼ ▼"
                  f"\n{utilities.format_balance(building.get_cost(new_amount, new_amount + 1, 1.0))}"
                  f" <:sooch:804702160217440276> per {property_name}"
        )
        return result
    else:
        return result  # TODO: cannot buy

