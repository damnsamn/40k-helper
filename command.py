from typing import Optional, Union, get_origin
import config
import gameplay
from dice import Dice


class Command:
    def __init__(self, command_name, callback_function, *args):
        self.name = command_name
        self.args = args
        self.callback_function = callback_function

        if self.args.count("?"):
            doc = self.callback_function.__doc__
            if doc:
                print(f'{self.name} {doc}')
            else:
                print(f'No help specified for command "{self.name}"')
            return
        else:
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
            Command(cmd, do_roll, *args)

        case "hits":
            Command(cmd, gameplay.hits, *args)

        case "wounds":
            Command(cmd, gameplay.wounds, *args)

        case "save":
            Command(cmd, gameplay.save, *args)

        case "exit":
            config.is_active = False

        case _:
            print(f'Command "{cmd}" not found')

    config.command_buffer.append(input)


def do_roll(n_dice = 6, n_rolls = 1):
    """[n_dice?] [n_rolls?]"""
    dice = Dice(int(n_dice))
    n_rolls = int(n_rolls)
    roll = dice.roll(n_rolls)

    if len(roll) == 1:
        roll = roll[0]

    print(roll)
