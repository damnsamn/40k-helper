
from dice import *


def roll_check(skill, shots):
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
        skill = 2
    elif strength/toughness <= 0.5:
        skill = 6
    elif strength > toughness:
        skill = 3
    elif strength < toughness:
        skill = 5
    else:
        skill = 4

    results = dice.roll(int(n_hits))

    def filter_hits(roll):
        return roll >= skill

    successful_wounds = list(filter(filter_hits, results))

    print(f'Wounds: {len(successful_wounds)} / {n_hits} - Success: {len(successful_wounds)/n_hits * 100}%')

