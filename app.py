import state
from command import *
from dice import *
from helpers import style
import saves
# try:
import readline
# except ImportError:
    # import pyreadline as readline

D2 = Dice(2)
D3 = Dice(3)
D6 = Dice(6)

# Clear screen
print("\033[H\033[2J", end="")

saves.load_from_state()

while state.is_active:


    cmd = input(style.yellow("> "))
    if cmd:
        command(cmd)
