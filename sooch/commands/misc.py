from typing import Optional

from sooch import path
import discord


async def invalid(client: discord.Client,
                  message: discord.Message,
                  content: list[str]) -> Optional[discord.Embed]:
    command = content[0]

    embed = discord.Embed()
    embed.add_field(
        name="Invalid command.",
        value=("{} is an invalid command. "
               "Please try again or type `s!help` or `s.help` "
               "for a list of commands.").format(
            command),
        inline=False)
    return embed

credits_embed = discord.Embed()
credits_path = path.from_root("sooch/embeds/credits.txt")
with open(credits_path, "r", encoding="utf-8") as credits_file:
    credits_text = credits_file.read()
    for field_data in credits_text.split("\n\n===\n\n"):
        field = field_data.split("\n", maxsplit=1)
        credits_embed.add_field(
            name=field[0],
            value=field[1],
            inline=True,
        )


async def credits(client: discord.Client,
                  message: discord.Message,
                  content: list[str]) -> Optional[discord.Embed]:
    return credits_embed
