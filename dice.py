from random import randint

class Dice:
  def __init__(self, sides):
    self.sides = sides

  # Roll dice n number of times
  def roll(self, n = 1):
    n = int(n) or 1;
    i = 0
    results = []
    sum = 0
    while i < n:
      result = randint(1,self.sides)
      results.append(result)
      sum+=result
      i+=1
    return {'results': results, "average": sum/n}