from typing import Optional

import discord
import sooch.message as msg

# Keeping this file separate from misc.py as a future "guide" command could be implemented
# (as well as other server, inventory and trade help commands)


# Help embeds will be cached into memory for faster access
cached_embeds = {}


def set_default_text():
    # Checks if "default is already assigned
    # This function is used to prevent circle importing
    if not "default" in cached_embeds.keys():
        # Caches the default embed
        cached_embeds["default"] = "\n".join(

            # Basically iterates through commands and hell knows what
            # tl;dr: it works
            map(lambda
                    t: f"`{t}` *or* `{''.join(msg.commands.get(t).aliases) if msg.commands.get(t).aliases else 'None'}`",
                msg.commands)
        )

    return cached_embeds.get("default")


# Ignore warning for now
async def help(client: discord.Client,
               message: discord.Message,
               content: list[str]) -> Optional[discord.Embed]:
    # Initialize the embed + parsed arguments
    embed = discord.Embed()
    args = None

    # Checks if there are any arguments
    if not content[1:]:
        embed.add_field(name="Help", value=set_default_text(), inline=True)

    # Parses content so that it removes the "s!" if it exists
    else:
        args = content[1] if not content[1].startswith("s!") else content[1][2:]

    # Otherwise check if the argument is valid and that there is only one argument
    if args in map(lambda cmd: cmd[2:], list(msg.commands.keys())) and not content[2:]:

        # Check if embed already exists in cache
        # If not, add it to the cache with key content[1]
        if not args in cached_embeds.keys():
            cached_embeds[args] = f"\n Description: *{msg.commands.get('s!' + args).description}* \n " \
                                  f"Aliases: *{''.join(msg.commands.get('s!' + args).aliases) if msg.commands.get('s!' + args).aliases else 'None'}* \n " \
                                  f"Syntax: *{msg.commands.get('s!' + args).syntax}* \n"

        embed.add_field(name=f"Getting help on `s!{args}`", value=cached_embeds.get(args), inline=True)

    # If all fails, send error message
    elif args:
        embed.add_field(name="Invalid Arguments",
                        value=f"`{content[1]}` is not a real command" if not content[
                                                                             2:] else "Provided mutliple arguments - Only 1 is required",
                        inline=True)
        embed.set_footer(
            text="If you think this is an error, please contact the devs or submit a bug report with s!report")

    return embed
