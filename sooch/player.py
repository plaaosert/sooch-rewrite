"""Contain class and method that allows for manipulation of player data."""
import time
from typing import Tuple
from sooch.commands.shared import services
from sooch.buildings import reg_buildings, trans_buildings


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
    def __init__(self, bot, data: Tuple, initialise=False):
        self.bot = bot

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

            self.base_income = 0
            self.income = 0
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

            self.base_income = 0
            self.income = 0

    @classmethod
    def from_loaded_data(cls, bot, data):
        """
        Take in raw data loaded from the database, applies preprocessing as
        necessary and passes it into the constructor.
        """
        # -- preprocessing goes here --
        return cls(bot, data)

    @classmethod
    def from_new_player(cls, bot, pid: int, name: str) -> "Player":
        """Creates a new player with only ID and username from the bot."""
        # Should not have to apply preprocessing since both are strings.
        return cls(bot, (pid, name), True)

    async def calculate_all_stats(self):
        """Update all player's stat such as income and other bonuses."""
        # Mostly concerned with temp buffs and bonuses from t/cprops.
        # Nothing to do here... yet.
        await self.get_base_sooch_income()

    async def get_base_sooch_income(self):
        # Get buildings from buildings service.
        building_counts = await services.reg_buildings_svc.get_building_count(self.discord_id)
        self.base_income = sum(reg_buildings[i].income * building_counts[i] for i in range(len(building_counts)))

    async def calculate_income(self):
        """
        Update player currency income values based on their income bonus. Call this after calculate_all_stats
        and after doing any command that modifies player.
        """
