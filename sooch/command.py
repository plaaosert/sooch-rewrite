import discord


class Command:
    def __init__(self, command, description, syntax, aliases=[]):
        self.command = command
        self.aliases = aliases
        self.description = description
        self.syntax = syntax


class InvalidCommand(Command):
    def __init__(self):
        # These are just placeholders.
        super().__init__("s!invalid", "An invalid command", "s!invalid")

    async def handle(self, client, message, content):
        command = content[0]

        embed = discord.Embed()
        embed.add_field(
            name="Invalid command.",
            value=("{} is an invalid command. "
                   "Please try again or type `s!help` or `s.help` for a list of commands.").format(
                command),
            inline=False)
        return embed


class CreditsCommand(Command):
    def __init__(self):
        super().__init__("s!credits",
                         "Show all the people that helped make Sooch a reality", "s!credits")
        self.credits_embed = discord.Embed()
        with open("./credits.txt", "r", encoding="utf-8") as credits_file:
            credits_text = credits_file.read()
            for field_data in credits_text.split("\n\n===\n\n"):
                field = field_data.split("\n", maxsplit=1)
                self.credits_embed.add_field(
                    name=field[0],
                    value=field[1],
                    inline=True,
                )

    async def handle(self, client, message, content):
        return self.credits_embed
