"""
Contains models for players and manages database information.
Loaded players are instantiated using the Player class.
"""
from sooch.player import Player
from typing import Optional


class Players:
    """Wrap around a SQL database and return players."""

    def __init__(self, database):
        self.database = database

    async def get_player(self, discord_id: int) -> Optional["Player"]:
        """Return the player info associated with the ID requested"""
        cursor = self.database.connection.cursor()
        cursor.execute(
            ("SELECT"
             "`discord_id`, `name`,`sooch_skin`, `embed_color`,"
             "`sooch`, `tsooch`, `csooch`,"
             "`last_claim`"
             "FROM `player` WHERE `discord_id` = ?"),
            (discord_id,)
        )
        row = cursor.fetchone()

        if row is None:
            return None

        return Player(
            (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        )

    async def add_player(self, player: "Player"):
        """Add the provided player into the database"""
        cursor = self.database.connection.cursor()
        cursor.execute(
            ("INSERT INTO `player`"
             "(`name`, `discord_id`, `sooch_skin`, `embed_color`,"
             "`sooch`, `tsooch`, `csooch`, `last_claim`)"
             "VALUES(?, ?, ?, ?, ?, ?, ?)"),
            (player.name, player.discord_id, player.sooch_skin, player.embed_color,
             player.sooch, player.tsooch, player.csooch, player.last_claim)
        )
        self.database.connection.commit()

    # We can't really use these. Doing multiple calls to the DB like this is very expensive.
    # I would prefer functions inside Player to mutate attribute values and a final save function here that commits
    # everything in a single bulk save.
    # -plaao

    #async def set_sooch_skin(self, discord_id: int, sooch_skin: str):
    #    """Set the sooch skin of the player"""
    #    cursor = self.database.connection.cursor()
    #    cursor.execute(
    #        "UPDATE `player` SET `sooch_skin`=? WHERE `discord_id`=?",
    #        (sooch_skin, discord_id)
    #    )
    #    self.database.connection.commit()
#
    #async def set_embed_color(self, discord_id: int, embed_color: int):
    #    """Set the embed color of the player"""
    #    cursor = self.database.connection.cursor()
    #    cursor.execute(
    #        "UPDATE `player` SET `embed_color`=? WHERE `discord_id`=?",
    #        (embed_color, discord_id)
    #    )
    #    self.database.connection.commit()
#
    #async def set_sooch(self, discord_id: int, sooch: int):
    #    """Set the amount of sooch the player has"""
    #    cursor = self.database.connection.cursor()
    #    cursor.execute(
    #        "UPDATE `player` SET `sooch`=? WHERE `discord_id`=?",
    #        (sooch, discord_id)
    #    )
    #    self.database.connection.commit()
#
    #async def set_tsooch(self, discord_id: int, tsooch: int):
    #    """Set the amount of transcension sooch the player has"""
    #    cursor = self.database.connection.cursor()
    #    cursor.execute(
    #        "UPDATE `player` SET `tsooch`=? WHERE `discord_id`=?",
    #        (tsooch, discord_id)
    #    )
    #    self.database.connection.commit()
#
    #async def set_csooch(self, discord_id: int, csooch: int):
    #    """Set the amount of consolidation sooch the player has"""
    #    cursor = self.database.connection.cursor()
    #    cursor.execute(
    #        "UPDATE `player` SET `csooch`=? WHERE `discord_id`=?",
    #        (csooch, discord_id)
    #    )
    #    self.database.connection.commit()
#
    #async def set_last_claim(self, discord_id: int, last_claim: int):
    #    """Set the last claim time of the player"""
    #    cursor = self.database.connection.cursor()
    #    cursor.execute(
    #        "UPDATE `player` SET `last_claim`=? WHERE `discord_id`=?",
    #        (last_claim, discord_id)
    #    )
    #    self.database.connection.commit()
    #"""