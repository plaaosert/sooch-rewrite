from typing import Optional

import discord
import sooch.message as msg


# Using a separate file for now, could merge with misc later (if needed)

async def help(client: discord.Client,
               message: discord.Message,
               content: list[str]) -> Optional[discord.Embed]:

    # Initialize the embed and text (the value for the field)
    embed = discord.Embed()
    help_text = ""

    # Checks if there are any arguments
    if not content[1:]:
        for command in msg.commands:
            help_text += f"`{command}` *sor* `{''.join(msg.commands.get(command).aliases)}` \n"
        embed.add_field(name="**Help**", value=help_text, inline=True)

    # Otherwise check if the argument is valid
    elif content[1] in map(lambda cmd: cmd[2:], list(msg.commands.keys())):
        help_text += f"\n Description: *{msg.commands.get('s!' + content[1]).description}* \n"
        help_text += f"Aliases: *{''.join(msg.commands.get('s!' + content[1]).aliases)}* \n"
        help_text += f"Syntax: *{msg.commands.get('s!' + content[1]).syntax}* \n"
        embed.add_field(name=f"Getting help on `s!{content[1]}`", value=help_text, inline=True)

    # If all fails, send an error message
    else:
        embed.add_field(name="Your arguments are invalid",
                        value=f"You probably mistyped something or `{content[1]}` is not a real command",
                        inline=True)
        embed.set_footer(text="If you think this is an error, please contact the devs or submit a bug report with s!report")

    return embed
