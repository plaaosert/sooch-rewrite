"""Utilities for manipulating path."""

from os import path
import sys


def from_root(relative: str):
    """
    Return the path to the file from the root of the project where the README
    file resides.

    :param relative: The relative path from the root of the project
    """
    # Note: It relies on the fact that sooch_bot.py is in sooch/ and works the
    #       path out from there.
    sooch_folder = path.dirname(sys.argv[0])
    return path.normpath(path.join(sooch_folder, "..", relative))
