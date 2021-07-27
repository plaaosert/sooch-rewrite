"""Contain class and method that allows for manipulation of player data."""
import time
from typing import Tuple


class Player:
    """
    Represent an instance of a player that is playing the game.
    Constructor for player takes a list of information of the same order as the
    DB.
    If the value of initialise is set to True, the player is initialised with
    initial values.

    It should be spawned once upon loading and then calculate their own stats.
    Since every action of a player is atomic (before saving), we only calculate stats once - on creation.

    We also need to use calculate_income separately upon building anything to get the new player income; for showing
    updated income amounts and updating the leaderboard.
    """

    # Need to have some sort of type hint for "Tuple[int, str, ...]" - but I don't know how to make that type hint,
    # like, work.
    # - plaao
    def __init__(self, data: Tuple, initialise=False):
        self.discord_id = data[0]
        self.name = data[1]

        # Further initialise all variables here as they are needed
        # properties, t_properties, income, etc.
        # The values should be as if a new player is being created. Since new
        # players always have the same values for income and similar, they can
        # be initialised using constants.
        if initialise:
            # Initialise the data.
            self.sooch_skin = ""
            self.embed_color = None
            self.sooch = 10
            self.tsooch = 0
            self.csooch = 0
            self.last_claim = time.time()
        else:
            # Read from the provided data.
            # We need to always read buildings and skills (because we need to calculate income)
            # Probably just use a left join in the original query when we get round to that.
            self.sooch_skin = data[2]
            self.embed_color = data[3]
            self.sooch = data[4]
            self.tsooch = data[5]
            self.csooch = data[6]
            self.last_claim = data[7]

    @classmethod
    def from_loaded_data(cls, data):
        """
        Take in raw data loaded from the database, applies preprocessing as
        necessary and passes it into the constructor.
        """
        # -- preprocessing goes here --
        return cls(data)

    @classmethod
    def from_new_player(cls, pid: int, name: str) -> "Player":
        """Creates a new player with only ID and username from the bot."""
        # Should not have to apply preprocessing since both are strings.
        return cls((pid, name), True)

    def calculate_all_stats(self):
        """Update all player's stat such as income and other bonuses."""
        # Mostly concerned with temp buffs and bonuses from t/cprops.
        # Nothing to do here... yet.

    def calculate_income(self):
        """
        Update player currency income values based on their income bonus. Call this after calculate_all_stats
        and after doing any command that modifies player.
        """
