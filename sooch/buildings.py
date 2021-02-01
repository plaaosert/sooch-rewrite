# Building definitions.
# Each building type is stored in a different list but their classes inherit from BaseBuilding.


class RegBuilding:
    id_inc = 0

    def __init__(self, name, cost, income):
        self.id = RegBuilding.id_inc
        RegBuilding.id_inc += 1
        self.name = name
        self.cost = int(cost)
        self.income = int(income)


# Function to set up a lookup table for a list of buildings.
# ID, name, all name permutations.
# In general, prioritise lower value buildings (
def populate_lookup(original):
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

# This is where the magic happens. Every single permutation of
reg_building_lookup = populate_lookup(reg_buildings)
# print("Lookup table generated with {} entries".format(len(reg_building_lookup)))
