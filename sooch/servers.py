class Servers:
    """Wrap around a SQL database and return servers."""

    def __init__(self, database):
        self.database = database

    async def get_server(self, discord_id: int) -> "Server":
        """Return the server info associated with the ID requested"""
        cursor = self.database.connection.cursor()
        cursor.execute(
            "select `name`, `command_prefix` from `server` where `discord_id` = ?",
            (discord_id,)
        )
        row = cursor.fetchone()

        if row is None:
            return None

        return Server(
            discord_id,
            row[0],
            row[1]
        )

    async def add_server(self, server):
        cursor = self.database.connection.cursor()
        cursor.execute(
            "insert into `server`(`discord_id`, `name`, `command_prefix`) values(?, ?, ?)",
            (server.discord_id, server.name, server.command_prefix)
        )
        self.database.connection.commit()


class Server:
    def __init__(self, discord_id, name, command_prefix):
        self.discord_id = discord_id
        self.name = name
        self.command_prefix = command_prefix
