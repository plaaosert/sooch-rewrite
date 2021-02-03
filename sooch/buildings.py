"""
Define buildings that are present in the game.
Every building type is stored in a different list but their classes all inherit
from BaseBuilding.
"""
import math
from typing import Optional


class BaseBuilding:
    """Contain methods applicable to every building in the game"""
    base_cost_amp = 0  # 0.0x increase is equivalent to "no increase"

    def __init__(self, name, cost, cost_amp=None):
        self.name = name
        self.cost = int(cost)
        # Some buildings may have steeper cost scaling than others of its type
        # An example is: Black consolidation vial
        self.cost_amp = cost_amp if cost_amp else self.__class__.base_cost_amp

    def get_cost(self, original, amount, cost_inc_divisor):
        """
        Return the amount a user needs to pay to purchase buildings.

        :param original: The number of buildings the user owns currently
        :param amount: The number of buildings to buy
        :param cost_inc_divisor:
            The building cost multiplier reduction for the player.
            Should be some float value.
        """
        # Take a shortcut here if cost_amp is == 0; we simply return the cost
        # since it never changes.
        if self.cost_amp == 0:
            return self.cost * amount

        # For a regular building: (0.2 / divisor) + 1 to get some value
        # 1 < costamp <= 1.2
        cost_inc = (self.cost_amp / cost_inc_divisor) + 1

        first_cost = self.cost * (cost_inc ** original)
        return int(first_cost * (1 - cost_inc ** amount) / (1 - cost_inc))

    def get_max_amount(self, original, balance, cost_inc_divisor):
        """
        Return the amount of buildings a user can purchase.

        :param original: The number of buildings the user owns currently
        :param balance:
            The current amount of the specific currency the user owns
        :param cost_inc_divisor:
            The building cost multiplier reduction for the player.
        """
        # Take a shortcut here if base_cost_amp is == 0; we simply return the
        # balance divided by the cost.
        if self.cost_amp == 0:
            return math.floor(balance / self.cost)

        # For a regular building: (0.2 / divisor) + 1 to get some value
        # 1 < costamp <= 1.2
        cost_inc = (self.cost_amp / cost_inc_divisor) + 1

        first_cost = self.cost * (cost_inc ** original)
        can_purchase = math.log(
            balance * (cost_inc - 1) / first_cost + 1, cost_inc)
        return math.floor(can_purchase)


class RegBuilding(BaseBuilding):
    """
    Regular buildings that are available to the player at the very start of the
    game and purchasable with just Sooch.
    """

    id_inc = 0
    # 0.2x increase per building bought
    # Will be divided by the player's costamp divisor to get the final costamp
    base_cost_amp = 0.2
    building_type = "Sooch"

    def __init__(self, name, cost, income, cost_amp=None):
        # Apply ID for the building object and increment it
        self.id = self.__class__.id_inc
        self.__class__.id_inc += 1

        # Set up name and cost from super
        super().__init__(name, cost, cost_amp)

        # Building-specific attributes
        self.income = int(income)


class TransBuilding(BaseBuilding):
    """
    Transcension buildings that are available to players after they transcend
    using `s!transcend` and purchasable with Transcension Sooch.
    """
    id_inc = 0
    building_type = "Transcension Sooch"

    def __init__(self, name, cost, cost_amp=None):
        # Apply ID for the building object and increment it
        self.id = self.__class__.id_inc
        self.__class__.id_inc += 1

        # Set up name and cost from super
        super().__init__(name, cost, cost_amp=None)

        # Building-specific attributes
        #   lol

def populate_lookup(original: list[BaseBuilding]) -> dict[str, BaseBuilding]:
    """
    Set up the lookup table for a list of buildings.
    Keys in the lookup table include:
    ID, name, name permutations (shortened names and their lowercase version).

    Lower value buildings are prioritised so "fa" resolves to "Farm" instead of
    "Factory" in the regular building list.
    """
    new_lookup = {}
    for building in original:
        new_lookup[str(building.id)] = building
        new_lookup[building.name.lower()] = building

        for i in range(1, len(building.name)):
            sliced_name = building.name[:i].lower()
            if sliced_name not in new_lookup:
                new_lookup[sliced_name] = building

    return new_lookup


# Big ol' list baby
reg_buildings = [
    RegBuilding("Farm",           1.00e+01,  6.00e+02),
    RegBuilding("BigFarm",        1.00e+02,  9.50e+02),
    RegBuilding("BiggerFarm",     2.50e+02,  1.75e+03),
    RegBuilding("HyperFarm",      1.00e+03,  5.60e+03),
    RegBuilding("TerraceFarm",    2.50e+03,  9.00e+03),
    RegBuilding("CubicFarm",      1.00e+04,  2.00e+04),
    RegBuilding("VerticalFarm",   6.00e+04,  7.00e+04),
    RegBuilding("HuntingLodge",   2.20e+05,  2.40e+05),
    RegBuilding("Bank",           1.00e+06,  1.00e+06),
    RegBuilding("BigBank",        5.00e+06,  5.50e+06),
    RegBuilding("InvestmentBank", 2.20e+07,  2.70e+07),
    RegBuilding("GlobalBank",     9.00e+07,  8.50e+07),
    RegBuilding("Village",        5.00e+08,  6.25e+08),
    RegBuilding("City",           5.00e+09,  5.00e+09),
    RegBuilding("Metropolis",     5.00e+10,  4.50e+10),
    RegBuilding("Mine",           1.00e+12,  8.00e+11),
    RegBuilding("MegaMine",       1.00e+13,  7.00e+12),
    RegBuilding("GigaMine",       1.00e+14,  6.00e+13),
    RegBuilding("ZettaMine",      1.00e+15,  4.50e+14),
    RegBuilding("CoreMine",       1.00e+16,  2.50e+15),
    RegBuilding("Workhouse",      1.00e+19,  1.90e+17),
    RegBuilding("Factory",        1.00e+21,  1.00e+19),
    RegBuilding("WorkForce",      1.00e+22,  9.00e+19),
    RegBuilding("FactoryState",   1.00e+24,  9.50e+21),
    RegBuilding("Nation",         1.00e+28,  4.50e+24),
    RegBuilding("Empire",         1.00e+31,  5.00e+27),
    RegBuilding("Dominion",       1.00e+34,  3.00e+30),
    RegBuilding("Control",        1.00e+37,  2.50e+33),
    RegBuilding("Aspect",         1.50e+40,  2.00e+37),
    RegBuilding("Divinity",       1.75e+43,  1.40e+39),
    RegBuilding("God",            2.00e+46,  1.20e+42),
    RegBuilding("Beyond",         2.50e+49,  7.00e+44),
    RegBuilding("Further",        2.75e+52,  3.00e+47),
    RegBuilding("Absolution",     3.00e+55,  1.50e+50),
    RegBuilding("TheEnd",         3.50e+58,  1.00e+53),
    RegBuilding("Dream",          3.75e+61,  7.50e+55),
    RegBuilding("DreamFarm",      6.50e+64,  5.50e+59),
    RegBuilding("DreamMine",      9.50e+67,  3.00e+62),
    RegBuilding("Hallucination",  2.95e+69,  1.70e+68),
    RegBuilding("FalseFarm",      2.45e+71,  1.50e+71),
    RegBuilding("FalseVillage",   2.25e+75,  1.30e+76),
    RegBuilding("FalseFactory",   1.50e+85,  1.10e+82),
    RegBuilding("Temple",         1.25e+100, 9.00e+93),
    RegBuilding("Monastery",      1.00e+110, 8.00e+102),
    RegBuilding("Altar",          9.20e+120, 7.00e+112),
    RegBuilding("FalseGod",       8.50e+130, 6.50e+120),
    RegBuilding("DreamGod",       7.25e+140, 5.50e+128),
    RegBuilding("Idolator",       6.50e+150, 3.50e+136),
    RegBuilding("HolyBook",       2.95e+160, 2.00e+141),
    RegBuilding("TrueGod",        1.25e+175, 1.00e+147),
    RegBuilding("FinalTruth",     1.00e+200, 1.00e+152)
]

# Left for testing purposes for now.
trans_buildings = [
    TransBuilding("test-building", 10),
]

# This is where the magic happens. Every single permutation of building names
# are generated.
reg_building_lookup = populate_lookup(reg_buildings)

# print("Lookup table generated with {} entries".format(
#     len(reg_building_lookup)))
# print("{:.3e}".format(trans_buildings[0].get_cost(0, 100, 1.5)))
# print("{:.3e}".format(trans_buildings[0].get_cost(0, 100, 1.2)))
# print("{:.3e}".format(trans_buildings[1].get_cost(0, 100, 1.5)))
# print("{:.3e}".format(trans_buildings[1].get_cost(0, 100, 1.2)))
