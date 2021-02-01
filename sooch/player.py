# Player class.
# Player should be spawned once upon loading and then calculate their own stats.


class Player:
    # Constructor for player takes a list of information of the same order as the DB.
    # If the value of initialise is True, initialise player with the initial values.
    def __init__(self, data, initialise=False):
        self.pid = data[0]
        self.name = data[1]
        # Further initialise all variables here as they are needed
        # properties, t_properties, income, etc.
        # The values should be as if a new player is being created. Since new players always have the same
        # values for income and similar, they can be initialised using constants.

    @classmethod
    def from_loaded_data(cls, data):
        # Takes in raw data loaded from the database,
        # applies preprocessing as necessary and passes it into the constructor.
        # -- preprocessing goes here --
        return cls(data)

    @classmethod
    def from_new_player(cls, pid, name):
        # Takes in only ID and username from the bot.
        # Should not have to apply preprocessing since both are strings.
        return cls((pid, name), True)

    def calculate_all_stats(self):
        # Function to calculate all player's stats such as income and other bonuses.
        # Mostly concerned with temp buffs and bonuses from t/cprops.
        pass  # Nothing to do here... yet.
