"""
Logic for claiming. Claiming is done by a series of "claim events" called in sequence by the main claim procedure.
"""
import time
from dataclasses import dataclass
import sooch.player


@dataclass
class ClaimResult:
    """Represent a claim result."""
    hours = 0
    spare_mins = 0

    this_claim_mult = 1

    basic_income = 0
    trans_income = 0

    crit_success = False
    items_gained = []

    tax_loss = 0
    event_currency = None


def determine_times(player: sooch.player.Player):
    # Get base difference (in seconds) from the last stored claim time. Multiply by time acceleration.
    base_diff = time.time() - player.last_claim
    # diff = base_diff * player.time_mult TODO add calculated stats like this
    diff = base_diff

    minutes = diff // 60
    hours = minutes // 60

    minutes_real = base_diff // 60
    hours_real = minutes // 60

    return hours, hours_real, minutes, minutes_real


def claim_basic(result, player, hours, minutes):
    pass


def claim_trans(result, player, hours, minutes):
    pass


def claim_crit(result, player, hours, minutes):
    """
    Handle a CRITICAL HIT, including rolling for one.
    """
    pass


def claim_items(result, player, hours_real, minutes_real):
    # Handles claiming all item types (Astral, Cosmic, Celestial are handled separately but still in this function)
    """
    original code snippet for this:

    while True:
        #print("rolling for item")
        timesTried += 1
        itemType = random.randint(0, 1)

        chanceMax = 1250000
        chanceMax /= 1 + ((math.log2(hours_real + (spareMins_real / 60) + 2) ** 1.25) / timesTried)
        chanceMax = int(chanceMax)

        #print(chanceMax, itemType, (math.log2(hours + (spareMins / 60) + 4)) / (len(itemsToAdd) + 1))

        itemRarityRoll = random.randint(1, chanceMax)
        for rarityID in range(-4, 6):
            if rarityChances[rarityID + 1][itemType] < itemRarityRoll:
                if itemType == 1 or rarityID >= -1:
                    break

        if rarityID != -4:
            if rarityID < 0:
                rarityID = 9 - rarityID

        itemPool = itemPools[itemType][rarityID]

        if len(itemPool) != 0:
            itemsToAdd.append(Item(random.choice(itemPool), random.randint(1, int(hours_real / 72) + (3 if itemType == 1 else 1))))
        else:
            break
    """
    pass


def claim_all(player: sooch.player.Player):
    hours, hours_real, minutes, minutes_real = determine_times(player)

    result = ClaimResult()
    result.hours = hours
    result.spare_mins = minutes % 60

    # Basic claim from buildings
    claim_basic(result, player, hours, minutes)

    # Consolidation claim (for tsooch)
    claim_trans(result, player, hours, minutes)

    # Crit chance
    claim_crit(result, player, hours, minutes)

    # Item drops
    claim_items(result, player, hours_real, minutes_real)

    # Special events? The candles again? Who knows...?
    # ???????????????????

    # Claiming can increase XP which can give a bonus to income, so we need to recalculate income here.
    player.calculate_income()

    # Return everything.
    return result
