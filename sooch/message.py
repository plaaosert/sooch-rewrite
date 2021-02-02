from sooch.command import InvalidCommand, CreditsCommand

valid_prefix = {
    "s!": True,
    "s.": True,
    "s$": True
}


commands = {
    "s!credits": CreditsCommand()
}
invalid_command = InvalidCommand()


async def on_message(client, message):
    if message.author.bot:
        # Ignore all bot messages.
        return
    if not valid_prefix.get(message.content[:2], False):
        # Check if the prefix is valid.
        # If it's not, ignore the message.
        return

    content = message.content.split(" ")
    command = commands.get(content[0], invalid_command)
    to_send = await command.handle(client, message, content)
    if not to_send is None:
        to_send.title = content[0]
        to_send.description = "Requested by {}".format(message.author.mention)
        await message.channel.send(embed=to_send)
