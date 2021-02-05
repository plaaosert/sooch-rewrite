"""
Module that contains command that provide information on how to progress to
the player.
"""
from typing import Optional

import discord

# Preload all help embeds
help_embeds: dict[str, discord.Embed] = {}


def populate_help_embeds(commands: list[any]):
    """Populate the help embed cache with the provided list of commands."""
    default_text = ""

    for command in commands:
        # Create joined aliases for help embeds and the default embed
        aliases = ' '.join(command.aliases) or "None"

        embed_text = ("Description: *{}*"
                      "\nAliases: *{}*"
                      "\nSyntax: *{}*").format(command.description,
                                               aliases,
                                               command.syntax)

        help_embeds[command.name] = discord.Embed().add_field(
            name="Help for `{}`".format(command.name),
            value=embed_text,
            inline=True
        )

        # This type of help text works for now
        # Once all features have been implemented, we can rework the help embed
        default_text += "`{}` *or* `{}`\n".format(command.name, aliases)

    # Set the default text after setting all the help texts
    help_embeds["default"] = discord.Embed().add_field(
        name="Help", value=default_text, inline=True)


async def help_command(client: discord.Client,
                       message: discord.Message,
                       content: list[str]) -> Optional[discord.Embed]:
    """Handle the s!help command."""
    del client, message

    # Initialize the embed + parsed arguments
    embed = discord.Embed()
    help_command_arguments = None

    # Checks if there are any arguments
    if not content[1:]:
        embed = help_embeds.get("default")

    # Adds "s!" to the beginning if it is not there
    else:
        help_command_arguments = content[1] if content[1].startswith(
            "s!") else "s!" + content[1]

    # Otherwise check if the argument is valid and that there is only one
    # argument
    if help_command_arguments in help_embeds.keys() and not content[2:]:
        embed = help_embeds.get(help_command_arguments)

    # If all fails, send error message
    elif help_command_arguments:
        embed.add_field(
            name="Invalid Arguments",
            value="`{}` is an invalid command \n\n"
                  "Correct syntax: `s!help <command>`".format(
                      ' '.join(content[1:])),
            inline=True
        )

        embed.set_footer(
            text=("If you think this is an error, please contact the devs or"
                  "submit a bug report with s!report")
        )

    return embed
