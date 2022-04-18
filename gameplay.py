
from dice import *

def hits(skill, shots):
    dice = Dice(6)
    skill = int(skill)
    results = dice.roll(int(shots))

    def filter_hits(roll):
        return roll >= skill

    hits = list(filter(filter_hits, results))

    print(f'Hits: {len(hits)} / {shots} - Success: {len(hits)/shots * 100}%')
