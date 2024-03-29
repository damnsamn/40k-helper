import classes
import helpers
import state
from dice import Dice




# Gameplay actions
# ------------------------------------------
def hits(skill, shots):
    """[skill] [n_rolls]"""
    dice = Dice(6)
    results = dice.roll(shots)

    def filter_hits(roll):
        return roll >= skill

    total_hits = list(filter(filter_hits, results))

    print(
        f'Hits: {len(total_hits)} / {shots} - Success: {len(total_hits)/shots * 100}%')
    return total_hits


def wounds(strength, toughness, n_hits):
    """[strength] [toughness] [n_hits]"""
    dice = Dice(6)

    compare_roll = helpers.strenth_toughness_check(strength, toughness)

    results = dice.roll(n_hits)

    def filter_hits(roll):
        return roll >= compare_roll

    total_wounds = list(filter(filter_hits, results))

    print(
        f'Wounds: {len(total_wounds)} / {n_hits} - Success: {len(total_wounds)/n_hits * 100}%')


def save(armour_save, penetration, n_wounds):
    """[save] [penetration] [n_wounds]"""
    dice = Dice(6)
    armour_save = armour_save + penetration
    results = dice.roll(n_wounds)

    def filter_hits(roll):
        return roll >= armour_save

    successful_saves = list(filter(filter_hits, results))

    print(
        f'Saves: {len(successful_saves)} / {n_wounds} - Success: {len(successful_saves)/n_wounds * 100}%')
    return successful_saves

def probabilities(skill, strength, toughness, armour_save, penetration, shots):
    """[skill] [strength] [toughness] [save] [ap] [shots]"""
    chance_hit = (6 - (skill - 1))/6
    chance_wound = (6 - (helpers.strenth_toughness_check(strength, toughness) - 1))/6
    chance_save = (6 - ((armour_save + penetration) - 1))/6

    if chance_save < 0:
        chance_save = 0

    chance_save = 1 - chance_save

    success_chance = chance_hit * chance_wound * chance_save

    success_chance_shots = success_chance
    for x in range(shots):
        print_success_chance = int(success_chance_shots * 100)
        print(f"{x + 1} shot{'s' if x > 0 else ''}: {print_success_chance}%")
        success_chance_shots = ((1 - success_chance_shots) * success_chance_shots) + success_chance_shots

    print(f"{success_chance * shots} average wounds")

def fight(attacker, defender):
    """[attacker_index] [defender_index]"""
    attacker = state.army[attacker]
    defender = state.army[defender]
    WS = helpers.sanitise(attacker.WS)
    S = helpers.sanitise(attacker.S)
    T = helpers.sanitise(defender.T)
    Sv = helpers.sanitise(defender.Sv)
    AP = 0
    A = helpers.sanitise(attacker.A)

    probabilities(WS, S, T, Sv, AP, A)