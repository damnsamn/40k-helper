import config
from command import *
from dice import *
import cmd
try:
    import readline
except ImportError:
    import pyreadline as readline

D2 = Dice(2)
D3 = Dice(3)
D6 = Dice(6)

# Clear screen
print("\033[H\033[2J", end="")

while config.is_active:


    cmd = input()
    if cmd:
        command(cmd)
