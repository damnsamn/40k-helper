
from dice import *


def hits(skill, shots):
    dice = Dice(6)
    skill = int(skill)
    results = dice.roll(int(shots))

    def filter_hits(roll):
        return roll >= skill

    total_hits = list(filter(filter_hits, results))

    print(f'Hits: {len(total_hits)} / {shots} - Success: {len(total_hits)/shots * 100}%')
    return total_hits


def wounds(strength, toughness, n_hits):
    dice = Dice(6)
    strength = int(strength)
    toughness = int(toughness)

    if strength/toughness >= 2:
        compare_roll = 2
    elif strength/toughness <= 0.5:
        compare_roll = 6
    elif strength > toughness:
        compare_roll = 3
    elif strength < toughness:
        compare_roll = 5
    else:
        compare_roll = 4

    results = dice.roll(int(n_hits))

    def filter_hits(roll):
        return roll >= compare_roll

    total_wounds = list(filter(filter_hits, results))

    print(f'Wounds: {len(total_wounds)} / {n_hits} - Success: {len(total_wounds)/n_hits * 100}%')


def save(armour_save, penetration, n_wounds):
    dice = Dice(6)
    armour_save = int(armour_save) + int(penetration)
    results = dice.roll(int(n_wounds))

    def filter_hits(roll):
        return roll >= armour_save

    successful_saves = list(filter(filter_hits, results))

    print(f'Saves: {len(successful_saves)} / {n_wounds} - Success: {len(successful_saves)/n_wounds * 100}%')
    return successful_saves
