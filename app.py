from dice import *

D6 = Dice(6)


dice = Dice(6)
bs = int(input("Ballistic/Weapon Skill: (1-6)+\n"))
results = dice.roll(input("How many shots?\n"))

def filter_hits(input):
  return input >= bs

hits = list(filter(filter_hits, results["results"]))
print("------------")
print("Results:", len(hits))