import re
import helpers
import saves
import state
import gameplay
from dice import Dice


class Command:
    def __init__(self, command_name, callback_function, *args, **kwargs):
        self.name = command_name
        self.args = args
        self.kwargs = kwargs
        self.callback_function = callback_function

        if self.args.count("?"):
            doc = self.callback_function.__doc__
            if doc:
                print(f'{self.name} {doc}')
            else:
                print(f'No help specified for command "{self.name}"')
            return
        else:
            self.callback_function(*self.args, **self.kwargs)


def command(input):
    input_array = input.split(" ")

    cmd = input_array[0]
    args = input_array
    args.pop(0)

    kwargs = {}

    # If arg is keyword, assign it
    for arg in args:
        if(re.search(r"=", arg)):
            key = re.search(r"(.+?)=", arg).groups(0)[0]
            value = re.search(r"=(.+)", arg).groups(0)[0]
            i = args.index(arg)
            args.pop(i)
            kwargs[key] = value

    # print(cmd, args)

    # parse commands
    match cmd:

        case "roll":
            Command(cmd, do_roll, *args, **kwargs)

        case "hits":
            Command(cmd, gameplay.hits, *args, **kwargs)

        case "wounds":
            Command(cmd, gameplay.wounds, *args, **kwargs)

        case "probabilities":
            Command(cmd, gameplay.probabilities, *args, **kwargs)

        case "save":
            Command(cmd, gameplay.save, *args, **kwargs)

        case "save_army":
            Command(cmd, saves.save_army, *args, **kwargs)

        case "load_army":
            Command(cmd, saves.load_army, *args, **kwargs)

        case "list_army":
            Command(cmd, list_army, *args, **kwargs)

        case "add_model":
            Command(cmd, state.add_model, *args, **kwargs)

        case "exit":
            state.is_active = False


def do_roll(n_dice = 6, n_rolls = 1):
    """[n_dice?] [n_rolls?]"""
    dice = Dice(int(n_dice))
    n_rolls = int(n_rolls)
    roll = dice.roll(n_rolls)

    if len(roll) == 1:
        roll = roll[0]

    print(roll)

def list_army():
    army_list = []
    for model in state.army:
        army_list.append(model.name)
    print(format(army_list))