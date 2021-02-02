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
