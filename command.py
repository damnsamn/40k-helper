import config
import gameplay
from dice import Dice

class Command:
    def __init__(self, callback_function, *args):
        self.args = args
        self.callback_function = callback_function

        try:
            self.callback_function(*self.args)
        except Exception as e:
            print("Incorrect arguments:", format(e))

def command(input):
    input_array = input.split(" ")

    cmd = input_array[0]
    args = input_array
    args.pop(0)

    # print(cmd, args)

    # parse commands
    match cmd:

        case "roll":
            Command(do_roll, *args)

        case "hits":
            Command(gameplay.hits, *args)

        case "wounds":
            Command(gameplay.wounds, *args)

        case "save":
            Command(gameplay.save, *args)

        case "exit":
            config.is_active = False

    config.command_buffer.append(input)




def do_roll(n_dice = 6, n_rolls = 1):
    dice = Dice(int(n_dice))
    n_rolls = int(n_rolls)
    roll = dice.roll(n_rolls)

    if len(roll) == 1:
        roll = roll[0]

    print(roll)
