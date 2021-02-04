"""Contain class and method that allows for manipulation of player resources."""
from typing import Tuple


class Player:
    """
    Represent an instance of a player that is playing the game.
    Constructor for player takes a list of information of the same order as the
    DB.
    If the value of initialise is set to True, the player is initialised with
    initial values.

    It should be spawned once upon loading and then calculate their own stats.
    """

    def __init__(self, data: Tuple[str, str, ...], initialise=False):
        self.pid = data[0]
        self.name = data[1]

        # Further initialise all variables here as they are needed
        # properties, t_properties, income, etc.
        # The values should be as if a new player is being created. Since new
        # players always have the same values for income and similar, they can
        # be initialised using constants.
        if initialise:
            # Initialise the resources.
            pass
        else:
            # Read from the provided resources.
            pass

    @classmethod
    def from_loaded_data(cls, data):
        """
        Take in raw resources loaded from the database, applies preprocessing as
        necessary and passes it into the constructor.
        """
        # -- preprocessing goes here --
        return cls(data)

    @classmethod
    def from_new_player(cls, pid: str, name: str) -> "Player":
        """Creates a new player with only ID and username from the bot."""
        # Should not have to apply preprocessing since both are strings.
        return cls((pid, name), True)

    def calculate_all_stats(self):
        """Update all player's stat such as income and other bonuses."""
        # Mostly concerned with temp buffs and bonuses from t/cprops.
        # Nothing to do here... yet.
