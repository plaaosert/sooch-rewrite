"""
A class to store all utilities which may be reused several times within the code.
"""
from typing import Tuple

from sooch import buildings


def format_balance(bal: float) -> str:
    """
    Used to format a decimal into either standard form (when it goes over 1.0e+10)
    Or places commas every 3 numbers.

    This makes balances/costs easier to read.
    :param bal: the decimal itself.
    :return: the formatted decimal as a string.
    """

    # This should support arbitrary usage of different function code -
    # like how sooch original had 12 different formatting methods
    if bal > 1.00e+10:
        return '{:.2e}'.format(bal)
    else:
        return '{:,}'.format(bal)


def determine_income(count: Tuple[int]) -> float:
    """
    Used to determine a user's income from their building counts.
    :param count: The tuple of building counts.
    :return: The income in sooch/hour.
    """
    income = 0
    for building_id, building in enumerate(buildings.reg_buildings):
        income += count[building_id] * building.income
    return income
