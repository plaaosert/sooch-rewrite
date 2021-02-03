from typing import Optional

import discord
import sooch.message as msg

# Keeping this file as a future "guide" command
# could be implemented (as well as other server, inventory and trade help commands)


# Initialize the default help text
default_text = ""


# User setup function to prevent circle importing
def init_default_text():
    for command in msg.commands:
        # Use global variable
        global default_text
        default_text += f"`{command}` *or* `{''.join(msg.commands.get(command).aliases) if msg.commands.get(command).aliases else 'None'}` \n"


# Ignore warning for now
async def help(client: discord.Client,
               message: discord.Message,
               content: list[str]) -> Optional[discord.Embed]:

    # Initialize the embed
    embed = discord.Embed()

    # Checks if default text is setup
    if default_text == "":
        init_default_text()

    # Checks if there are any arguments
    if not content[1:]:
        embed.add_field(name="Help", value=default_text, inline=True)

    # Otherwise check if the argument is valid and that there is only one argument
    elif content[1] in map(lambda cmd: cmd[2:], list(msg.commands.keys())) and not content[2:]:
        # Using a help_text variable to keep code readable
        # Not sure how to pre-generate this text without extra nonsense
        # TODO: get s!help s!<command> to work

        help_text = f"\n Description: *{msg.commands.get('s!' + content[1]).description}* \n " \
                    f"Aliases: *{''.join(msg.commands.get('s!' + content[1]).aliases) if msg.commands.get('s!' + content[1]).aliases else 'None'}* \n " \
                    f"Syntax: *{msg.commands.get('s!' + content[1]).syntax}* \n"

        embed.add_field(name=f"Getting help on `s!{content[1]}`", value=help_text, inline=True)

    # If all fails, send an error message
    else:
        embed.add_field(name="Invalid Arguments",
                        value=f"`{content[1]}` is not a real command" if not content[2:] else "Provided mutliple arguments - Only 1 is required",
                        inline=True)
        embed.set_footer(
            text="If you think this is an error, please contact the devs or submit a bug report with s!report")

    return embed
