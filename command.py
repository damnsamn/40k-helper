import config
import gameplay
from dice import Dice


def command(input):
    input_array = input.split(" ")

    cmd = input_array[0]
    args = input_array
    args.pop(0)

    # print(cmd, args)

    # parse commands
    match cmd:

        case "roll":
            n_dice = int(args[0]) if len(args) > 0 else 6
            n_rolls = int(args[1]) if len(args) > 1 else 1
            do_roll(n_dice, n_rolls)

        case "hits":
            if len(args) > 0:
                n_skill = int(args[0])
            if len(args) > 1:
                n_shots = int(args[1])
            gameplay.hits(n_skill, n_shots)

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


