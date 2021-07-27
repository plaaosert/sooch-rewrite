"""Contain models for the amount of regular buildings players own."""
from typing import List, Tuple

set_query: List[str] = []
for set_building_id in range(1, 51+1):
    set_query.append(
        f"INSERT INTO `reg_buildings`(`discord_id`, `b{set_building_id}`) "
        f"VALUES (?, ?) ON CONFLICT DO "
        f"UPDATE SET `b{set_building_id}` = ? WHERE `discord_id`=?"
    )


class RegBuildings:
    """Wrap around a SQL database and return regular buildings."""

    def __init__(self, database):
        self.database = database

    async def get_building_count(self, discord_id: int) -> Tuple[int, ...]:
        """Return the amount of buildings the player with the ID has."""
        cursor = self.database.connection.cursor()
        cursor.execute(
            "SELECT * FROM `reg_buildings` WHERE `discord_id` = ?",
            (discord_id,)
        )
        row = cursor.fetchone()

        if row is None:
            return (0,) * 51

        # First should be `discord_id` so drop it.
        return row[1:]

    async def set_building_count(self, discord_id: int,
                                 building_id: int, count: int):
        """Set the amount of buildings the player has."""
        cursor = self.database.connection.cursor()
        cursor.execute(
            set_query[building_id],
            (discord_id, count, count, discord_id)
        )
        self.database.connection.commit()

    async def remove_buildings(self, discord_id: int):
        """Resets all the building associated with the provided discord ID."""
        cursor = self.database.connection.cursor()
        cursor.execute(
            "DELETE FROM `reg_buildings` WHERE `discord_id` = ?",
            (discord_id,)
        )
        self.database.connection.commit()
